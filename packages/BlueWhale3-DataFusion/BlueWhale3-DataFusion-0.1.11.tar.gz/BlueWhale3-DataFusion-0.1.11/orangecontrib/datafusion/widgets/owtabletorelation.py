from AnyQt.QtWidgets import QTableView, QGridLayout, QWidget
from AnyQt.QtCore import Qt, QSize

from Orange.data import Table, Domain
from Orange.widgets.settings import Setting, ContextSetting, PerfectDomainContextHandler
from Orange.widgets.utils.itemmodels import TableModel
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from orangecontrib.datafusion.models import Relation
from orangecontrib.datafusion.i18n_config import *
from skfusion import fusion


def __(key):
    return i18n.t("datafusion.owtabletorelation." + key)


class OWTableToRelation(OWWidget):
    name = __("name")
    description = __("desc")
    priority = 50000
    icon = "icons/TableToRelation.svg"

    class Inputs:
        data = Input('Data', Table, label=i18n.t("datafusion.common.data"))

    class Outputs:
        relation = Output('Relation', Relation, label=i18n.t("datafusion.common.relation"))

    settingsHandler = PerfectDomainContextHandler()

    data = None

    relation_name = ContextSetting("")
    transpose = ContextSetting(False)

    row_type = ContextSetting("")
    selected_meta = ContextSetting(0)
    row_names = None

    col_type = ContextSetting("")
    col_names = None

    auto_commit = Setting(True)

    def __init__(self):
        super().__init__()

        self.model = None
        self.view = None
        self.row_names_combo = None
        self.icons = gui.attributeIconDict
        self.populate_control_area()
        self.populate_main_area()

    def populate_control_area(self):
        rel = gui.widgetBox(self.controlArea, __("box.relation"))
        gui.lineEdit(rel, self, "relation_name", __("row.name"), callbackOnType=True, callback=self.apply)
        gui.checkBox(rel, self, "transpose", __("checkbox_transpose"), callback=self.apply)

        col = gui.widgetBox(self.controlArea, __("row.column"))
        gui.lineEdit(col, self, "col_type", __("row.object_type"), callbackOnType=True, callback=self.apply)

        row = gui.widgetBox(self.controlArea, __("box.row"))
        gui.lineEdit(row, self, "row_type", __("row.object_type"), callbackOnType=True, callback=self.apply)
        self.row_names_combo = gui.comboBox(row, self, "selected_meta", label=__("box.object_name"),
                                            callback=self.update_row_names)

        gui.rubber(self.controlArea)
        gui.auto_commit(self.controlArea, self, "auto_commit", __("btn_send"),
                        checkbox_label=__('row.auto_send'),
                        orientation='vertical')

    def populate_main_area(self):
        grid = QWidget()
        grid.setLayout(QGridLayout(grid))
        self.mainArea.layout().addWidget(grid)

        col_type = gui.label(None, self, '%(col_type)s')

        grid.layout().addWidget(col_type, 0, 1)
        grid.layout().setAlignment(col_type, Qt.AlignHCenter)

        row_type = gui.label(None, self, '%(row_type)s')
        grid.layout().addWidget(row_type, 1, 0)
        grid.layout().setAlignment(row_type, Qt.AlignVCenter)

        self.view = QTableView()
        self.model = None
        grid.layout().addWidget(self.view, 1, 1)

    def sizeHint(self):
        return QSize(800, 500)

    @Inputs.data
    def set_data(self, data):
        self.closeContext()
        self.data = data
        if data is not None:
            self.init_attr_values(data.domain.metas)
            self.openContext(self.data)
            self.col_names = [str(a.name) for a in data.domain.attributes]
            if hasattr(data, 'col_type'):
                self.col_type = data.col_type
        else:
            self.init_attr_values(())
        self.update_preview()
        self.update_row_names()
        self.unconditional_commit()

    def init_attr_values(self, candidates):
        self.col_type = ""
        self.col_names = None

        if candidates:
            self.row_type = candidates[0].name
            self.selected_meta = 1
        else:
            self.row_type = ""
            self.selected_meta = 0
            self.row_names = None

        self.row_names_combo.clear()
        self.row_names_combo.addItem(__('placeholder_none'))
        for var in candidates:
            self.row_names_combo.addItem(self.icons[var], var.name)
        self.row_names_combo.setCurrentIndex(self.selected_meta)

    def update_row_names(self):
        if self.selected_meta:
            self.row_names = list(self.data[:, -self.selected_meta].metas.flatten())
        else:
            self.row_names = None

        if self.model:
            self.model.headerDataChanged.emit(
                Qt.Vertical, 0, self.model.rowCount() - 1)
        self.commit()

    def update_preview(self):
        this = self

        class MyTableModel(TableModel):
            def headerData(self, section, orientation, role):
                if orientation == Qt.Vertical and role == Qt.DisplayRole:
                    if this.row_names:
                        return this.row_names[section]
                else:
                    return super().headerData(section, orientation, role)

        if self.data:
            domain = Domain(self.data.domain.attributes)
            preview_data = Table(domain, self.data)
            self.model = MyTableModel(preview_data)
        else:
            self.model = None
        self.view.setModel(self.model)

    def apply(self):
        self.commit()

    def commit(self):
        if self.data:
            domain = self.data.domain
            metadata_cols = list(domain.class_vars) + list(domain.metas)
            metadata = [{var: var.to_val(value) for var, value in zip(metadata_cols, values.list)}
                        for values in self.data[:, metadata_cols]]

            if self.transpose:
                relation = fusion.Relation(
                    self.data.X.T, name=self.relation_name,
                    row_type=fusion.ObjectType(self.col_type or 'Unknown'), row_names=self.col_names,
                    col_type=fusion.ObjectType(self.row_type or 'Unknown'), col_names=self.row_names,
                    col_metadata=metadata)
            else:
                relation = fusion.Relation(
                    self.data.X, name=self.relation_name,
                    row_type=fusion.ObjectType(self.row_type or 'Unknown'), row_names=self.row_names,
                    row_metadata=metadata,
                    col_type=fusion.ObjectType(self.col_type or 'Unknown'), col_names=self.col_names,
                )
            self.Outputs.relation.send(Relation(relation))


if __name__ == '__main__':
    from AnyQt.QtWidgets import QApplication

    app = QApplication([])
    ow = OWTableToRelation()
    ow.set_data(Table('zoo'))
    ow.show()
    app.exec()
    ow.saveSettings()
