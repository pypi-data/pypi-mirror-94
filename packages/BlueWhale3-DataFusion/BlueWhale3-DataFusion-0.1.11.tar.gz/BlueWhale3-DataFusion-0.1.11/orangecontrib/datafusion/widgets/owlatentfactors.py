from Orange.widgets import widget, gui, settings
from Orange.widgets.utils.itemmodels import PyTableModel
from Orange.widgets.widget import Input, Output

from skfusion import fusion
from orangecontrib.datafusion.widgets.owfusiongraph import rel_shape, rel_cols
from orangecontrib.datafusion.models import Relation, FittedFusionGraph
from orangecontrib.datafusion.widgets.graphview import GraphView, Edge
from orangecontrib.datafusion.i18n_config import *


def __(key):
    return i18n.t("datafusion.owlatentfactors." + key)


def is_constraint(relation):
    """Skip constraint (Theta) relations"""
    return relation.row_type == relation.col_type


class LatentGraphView(GraphView):
    def itemClicked(self, item):
        if isinstance(item, Edge) and item.source is item.dest: return
        self.clearSelection()
        super().itemClicked(item)


class OWLatentFactors(widget.OWWidget):
    name = __('name')
    description = __('desc')
    priority = 20000
    icon = "icons/LatentFactors.svg"

    class Inputs:
        fitted_fusion_graph = Input("Fitted fusion graph", FittedFusionGraph,
                                    label=i18n.t('datafusion.common.fit_fusion_graph'))

    class Outputs:
        relation = Output('Relation', Relation, label=i18n.t('datafusion.common.relation'))

    autorun = settings.Setting(True)

    completions = settings.Setting([])
    selected_completions = settings.Setting([])
    factors = settings.Setting([])
    selected_factors = settings.Setting([])
    backbones = settings.Setting([])
    selected_backbones = settings.Setting([])

    def __init__(self):
        super().__init__()
        self.n_relations = 0
        self.n_object_types = 0
        self.graphview = LatentGraphView(self)
        self.graphview.selectionChanged.connect(self.on_graph_element_selected)
        self._create_layout()

    def on_graph_element_selected(self, selected):
        """Handle graph_element_selected signal, and update the info boxen"""
        if not selected:
            return self._populate_tables(reset=True)
        selected_is_edge = isinstance(selected[0], Edge)
        # Update the control table
        if selected_is_edge:
            nodes = self.fuser.get_selected_nodes([selected[0].source.name, selected[0].dest.name])
            backbones = [(rel, (self.fuser.backbone(rel),))
                         for rel in self.fuser.get_relations(*nodes)
                         if not is_constraint(rel)]
            self._populate_tables(backbones=backbones)
            self.table_backbones.selectRow(0)
        else:
            node = self.fuser.get_selected_nodes([selected[0].name])[0]
            self._populate_tables(factors=[(node, (self.fuser.factor(node),))])
            self.table_factors.selectRow(0)

    def _create_layout(self):
        self.mainArea.layout().addWidget(self.graphview)
        info = gui.widgetBox(self.controlArea, __('box.info'))
        gui.label(info, self, __('label.object_type'))
        gui.label(info, self, __('label.relation'))

        class TableView(gui.TableView):
            def __init__(self, parent, bold_columns):
                super().__init__(parent,
                                 selectionMode=self.SingleSelection)
                self.horizontalHeader().setVisible(False)
                self.bold_font = self.BoldFontDelegate(self)  # member because PyQt sometimes unrefs too early
                for col in bold_columns:
                    self.setItemDelegateForColumn(col, self.bold_font)

        box = gui.widgetBox(self.controlArea, __('box.recipe_factor'))
        table = self.table_factors = TableView(self, (2,))
        model = self.model_factors = PyTableModel(parent=self)
        table.setModel(model)
        box.layout().addWidget(table)

        box = gui.widgetBox(self.controlArea, __('box.backbone_factor'))
        table = self.table_backbones = TableView(self, (2, 4))
        model = self.model_backbones = PyTableModel(parent=self)
        table.setModel(model)
        box.layout().addWidget(table)

        box = gui.widgetBox(self.controlArea, __('box.complete_relation'))
        table = self.table_completions = TableView(self, (2, 4))
        model = self.model_completions = PyTableModel(parent=self)
        table.setModel(model)
        box.layout().addWidget(table)

        self.controlArea.layout().addStretch(1)

        def _on_selected_factor(item):
            self.table_completions.clearSelection()
            self.table_backbones.clearSelection()

        def _on_selected_backbone(item):
            self.table_completions.clearSelection()
            self.table_factors.clearSelection()

        def _on_selected_completion(item):
            self.table_factors.clearSelection()
            self.table_backbones.clearSelection()

        def on_selection_changed(table, model, itemChanged_handler):
            def _f(selected, deselected):
                gui.TableView.selectionChanged(table, selected, deselected)
                if not selected:
                    return self.commit(None)
                item = model[selected[0].top()][0]
                itemChanged_handler(item)
                self.commit(item)

            return _f

        self.table_factors.selectionChanged = on_selection_changed(
            self.table_factors, self.model_factors, _on_selected_factor)
        self.table_backbones.selectionChanged = on_selection_changed(
            self.table_backbones, self.model_backbones, _on_selected_backbone)
        self.table_completions.selectionChanged = on_selection_changed(
            self.table_completions, self.model_completions, _on_selected_completion)

    def commit(self, item):
        data = Relation.create(*item, graph=self.fuser) if item else None
        self.Outputs.relation.send(data)

    def _populate_tables(self, factors=None, backbones=None, reset=False):
        if not self.fuser: return
        self.model_factors.clear()
        self.model_backbones.clear()
        self.Outputs.relation.send(None)
        if factors or reset:
            for otype, matrices in factors or self.fuser.factors_.items():
                M = matrices[0]
                self.model_factors.append([(M, otype, None), rel_shape(M.data), otype.name])
            self.table_factors.hideColumn(0)
        if backbones or reset:
            for relation, matrices in backbones or self.fuser.backbones_.items():
                M = matrices[0]
                self.model_backbones.append([(M, None, None), rel_shape(M.data)] + rel_cols(relation))
            self.table_backbones.hideColumn(0)
        if reset:
            self.model_completions.clear()
            for rel, matrices in self.fuser.backbones_.items():
                M = self.fuser.complete(rel)
                self.model_completions.append([(M, rel.row_type, rel.col_type), rel_shape(M.data)] + rel_cols(rel))
            self.table_completions.hideColumn(0)

    @Inputs.fitted_fusion_graph
    def on_fuser_change(self, fuser):
        self.fuser = fuser
        self._populate_tables(reset=True)
        self.graphview.fromFusionFit(fuser)
        # this ensures gui.label-s get updated
        self.n_object_types = fuser.n_object_types if fuser else 0
        self.n_relations = fuser.n_relations if fuser else 0


def main():
    # example from https://github.com/marinkaz/scikit-fusion
    import numpy as np
    from AnyQt.QtWidgets import QApplication
    R12 = np.random.rand(50, 100)
    R32 = np.random.rand(150, 100)
    R33 = np.random.rand(150, 150)
    t1 = fusion.ObjectType(i18n.t('datafusion.object.user'), 10)
    t2 = fusion.ObjectType(i18n.t('datafusion.object.movie'), 30)
    t3 = fusion.ObjectType(i18n.t('datafusion.object.actor'), 40)
    relations = [fusion.Relation(R12, t1, t2, name=i18n.t('datafusion.relation.like')),
                 fusion.Relation(R12, t1, t2, name=i18n.t('datafusion.relation.dislike')),
                 fusion.Relation(R33, t3, t3, name=i18n.t('datafusion.relation.marry_to')),
                 fusion.Relation(R32, t3, t2, name=i18n.t('datafusion.relation.play_in'))]
    G = fusion.FusionGraph()
    for rel in relations:
        G.add_relation(rel)
    fuser = fusion.Dfmf()
    fuser.fuse(G)
    app = QApplication([])
    w = OWLatentFactors()
    w.on_fuser_change(FittedFusionGraph(fuser))
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
