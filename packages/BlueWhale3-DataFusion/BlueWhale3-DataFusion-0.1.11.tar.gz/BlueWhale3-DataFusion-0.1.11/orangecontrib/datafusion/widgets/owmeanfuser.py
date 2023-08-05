from collections import defaultdict

from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.itemmodels import PyTableModel
from Orange.widgets.widget import Input, Output

from skfusion import fusion
from orangecontrib.datafusion.models import Relation, FusionGraph, RelationCompleter
from orangecontrib.datafusion.widgets.owfusiongraph import rel_shape, rel_cols
from orangecontrib.datafusion.i18n_config import *

import numpy as np


def __(key):
    return i18n.t("datafusion.owmeanfuser." + key)


class MeanBy:
    ROWS = __('gbox.rows')
    COLUMNS = __('gbox.columns')
    VALUES = __('gbox.all_values')
    all = (COLUMNS, ROWS, VALUES)


class MeanFuser(RelationCompleter):
    def __init__(self, mean_by):
        self.axis = {
            MeanBy.ROWS: 1,
            MeanBy.COLUMNS: 0,
            MeanBy.VALUES: None}[MeanBy.all[mean_by]]
        self.mean_by = mean_by

    @property
    def name(self):
        return 'Mean by ' + MeanBy.all[self.mean_by].lower()

    def __getattr__(self, attr):
        return self

    def retrain(self):
        """Mean is deterministic, return the same Completer."""
        return self

    def can_complete(self, relation):
        """MeanFuser can complete any relation."""
        return True

    def complete(self, relation):
        """Mock ``skfusion.fusion.FusionFit.complete()``"""
        assert isinstance(relation, fusion.Relation)
        A = relation.data.copy()
        if not np.ma.is_masked(A):
            return A
        mean_value = np.nanmean(A, axis=None)
        if self.axis is None:
            # Replace the mask with mean of the matrix
            A[A.mask] = mean_value
        else:
            # Replace the mask with mean by axes
            mean = np.nanmean(A, axis=self.axis)
            # Replace any NaNs in mean with mean of the matrix
            mean[np.isnan(mean)] = mean_value
            A[A.mask] = np.take(mean, A.mask.nonzero()[not self.axis])
        return A


class OWMeanFuser(widget.OWWidget):
    name = __('name')
    priority = 55000
    icon = 'icons/MeanFuser.svg'

    class Inputs:
        fusion_graph = Input('Fusion Graph', FusionGraph, label=i18n.t('datafusion.common.fusion_graph'))
        relation = Input('Relation', Relation, multiple=True, label=i18n.t('datafusion.common.relation'))

    class Outputs:
        fuser = Output('Mean-fitted fusion graph', MeanFuser, default=True,
                       label=i18n.t('datafusion.common.mean_fit_fusion_graph'))
        relation = Output('Relation', Relation, label=i18n.t('datafusion.common.relation'))

    want_main_area = False

    mean_by = settings.Setting(0)
    selected_relation = settings.Setting(0)

    def __init__(self):
        super().__init__()
        self.relations = defaultdict(int)
        self.id_relations = {}
        self.graph = None
        self._create_layout()
        self.commit()

    def _create_layout(self):
        self.controlArea.layout().addWidget(
            gui.comboBox(self.controlArea, self, 'mean_by',
                         box=__('box.mean_fuser'),
                         label=__('label.masked_value_mean'),
                         items=MeanBy.all, callback=self.commit))
        box = gui.widgetBox(self.controlArea, __('box.output_completed_relation'))

        class TableView(gui.TableView):
            def __init__(self, parent):
                super().__init__(parent, selectionMode=self.SingleSelection)
                self._parent = parent
                self.bold_font = self.BoldFontDelegate(self)  # member because PyQt sometimes unrefs too early
                self.setItemDelegateForColumn(2, self.bold_font)
                self.setItemDelegateForColumn(4, self.bold_font)
                self.horizontalHeader().setVisible(False)

            def selectionChanged(self, *args):
                super().selectionChanged(*args)
                self._parent.commit()

        table = self.table = TableView(self)
        model = self.model = PyTableModel(parent=self)
        table.setModel(model)
        box.layout().addWidget(table)
        self.controlArea.layout().addStretch(1)

    def commit(self, item=None):
        self.fuser = MeanFuser(self.mean_by)
        self.Outputs.fuser.send(self.fuser)
        rows = [i.row() for i in self.table.selectionModel().selectedRows()]
        if self.model.rowCount() and rows:
            relation = self.model[rows[0]][0]
            data = Relation.create(self.fuser.complete(relation),
                                   relation.row_type,
                                   relation.col_type,
                                   self.graph)
        else:
            data = None
        self.Outputs.relation.send(data)

    def update_table(self):
        self.model.wrap([([rel, rel_shape(rel.data)] +
                          rel_cols(rel) +
                          [__('label.not_mask') if not np.ma.is_masked(rel.data) else ''])
                         for rel in self.relations])
        self.table.hideColumn(0)

    def _add_relation(self, relation):
        self.relations[relation] += 1

    def _remove_relation(self, relation):
        self.relations[relation] -= 1
        if not self.relations[relation]:
            del self.relations[relation]

    @Inputs.fusion_graph
    def on_fusion_graph_change(self, graph):
        if graph:
            self.graph = graph
            for rel in graph.relations:
                self._add_relation(rel)
        else:
            self.graph = None
            for rel in self.graph.relations:
                self._remove_relation(rel)
        self.update_table()
        self.commit()

    @Inputs.relation
    def on_relation_change(self, relation, id):
        try:
            self._remove_relation(self.id_relations.pop(id))
        except KeyError:
            pass
        if relation:
            self.id_relations[id] = relation.relation
            self._add_relation(relation.relation)
        self.update_table()
        self.commit()


def main():
    from AnyQt.QtWidgets import QApplication
    t1 = fusion.ObjectType(i18n.t('datafusion.object.user'), 10)
    t2 = fusion.ObjectType(i18n.t('datafusion.object.movie'), 30)
    t3 = fusion.ObjectType(i18n.t('datafusion.object.actor'), 40)

    # test that MeanFuser completes correctly
    R = np.ma.array([[1, 1, 0],
                     [3, 0, 0]], mask=[[0, 0, 1],
                                       [0, 1, 1]], dtype=float)
    rel = fusion.Relation(R, t1, t2)
    assert (MeanFuser(0).complete(rel) == [[1, 1, 5 / 3],
                                           [3, 1, 5 / 3]]).all()
    assert (MeanFuser(1).complete(rel) == [[1, 1, 1],
                                           [3, 3, 3]]).all()
    assert (MeanFuser(2).complete(rel) == [[1, 1, 5 / 3],
                                           [3, 5 / 3, 5 / 3]]).all()

    R1 = np.ma.array(np.random.random((20, 20)))
    R2 = np.ma.array(np.random.random((40, 40)),
                     mask=np.random.random((40, 40)) > .8)
    relations = [
        fusion.Relation(R1, t1, t2, name=i18n.t('datafusion.relation.like')),
        fusion.Relation(R2, t3, t2, name=i18n.t('datafusion.relation.feature_in')),
    ]
    G = fusion.FusionGraph()
    G.add_relations_from(relations)
    app = QApplication([])
    w = OWMeanFuser()
    w.on_fusion_graph_change(G)
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
