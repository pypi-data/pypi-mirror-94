import sys
import copy

from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QGridLayout, QSizePolicy

from Orange.data import Table
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import OWWidget, Input, Output
from skfusion import fusion
from orangecontrib.datafusion.models import Relation
from orangecontrib.datafusion.i18n_config import *

import numpy as np


def __(key):
    return i18n.t("datafusion.owsamplematrix." + key)


class SampleBy:
    ROWS = "Rows"
    COLS = "Columns"
    ROWS_COLS = 'Rows and columns'
    ENTRIES = 'Entries'
    all = [ROWS, COLS, ROWS_COLS, ENTRIES]


def hide_data(table, percentage, sampling_type):
    assert not np.ma.is_masked(table)
    np.random.seed(0)
    if sampling_type == SampleBy.ROWS_COLS:

        row_s_mask, row_oos_mask = hide_data(table, np.sqrt(percentage), SampleBy.ROWS)
        col_s_mask, col_oos_mask = hide_data(table, np.sqrt(percentage), SampleBy.COLS)

        oos_mask = np.logical_and(row_oos_mask, col_oos_mask)
        return oos_mask

    elif sampling_type == SampleBy.ROWS:
        rand = np.repeat(np.random.rand(table.X.shape[0], 1), table.X.shape[1], axis=1)
    elif sampling_type == SampleBy.COLS:
        rand = np.repeat(np.random.rand(1, table.X.shape[1]), table.X.shape[0], axis=0)
    elif sampling_type == SampleBy.ENTRIES:
        rand = np.random.rand(*table.X.shape)
    else:
        raise ValueError("Unknown sampling method.")

    oos_mask = np.logical_and(rand >= percentage, ~np.isnan(table))
    return oos_mask


class OWSampleMatrix(OWWidget):
    name = __("name")
    description = __("desc")
    priority = 60000
    icon = "icons/MatrixSampler.svg"
    want_main_area = False
    resizing_enabled = False

    class Inputs:
        data = Input('Data', Table, default=True, label=i18n.t("datafusion.common.data"))

    class Outputs:
        in_sample_data = Output("In-sample Data", Relation, label=i18n.t("datafusion.common.in_sample_data"))
        out_of_sample_data = Output("Out-of-sample Data", Relation, label=i18n.t("datafusion.common.out_sample_data"))

    percent = settings.Setting(90)
    method = settings.Setting(0)
    bools = settings.Setting([])

    def __init__(self):
        super().__init__()
        self.data = None

        form = QGridLayout()

        self.row_type = ""
        gui.lineEdit(self.controlArea, self, "row_type", __("row.row_type"), callback=self.send_output)

        self.col_type = ""
        gui.lineEdit(self.controlArea, self, "col_type", __("row.column_type"), callback=self.send_output)

        methodbox = gui.radioButtonsInBox(
            self.controlArea, self, "method", [],
            box=self.tr(__('box_sample_method')), orientation=form)

        rows = gui.appendRadioButton(methodbox, __('btn.rows'), addToLayout=False)
        form.addWidget(rows, 0, 0, Qt.AlignLeft)

        cols = gui.appendRadioButton(methodbox, __('btn.columns'), addToLayout=False)
        form.addWidget(cols, 0, 1, Qt.AlignLeft)

        rows_and_cols = gui.appendRadioButton(methodbox, __('btn.rows_columns'), addToLayout=False)
        form.addWidget(rows_and_cols, 1, 0, Qt.AlignLeft)

        entries = gui.appendRadioButton(methodbox, __('btn.entries'), addToLayout=False)
        form.addWidget(entries, 1, 1, Qt.AlignLeft)

        sample_size = gui.widgetBox(self.controlArea, __("box_data_sample_proportion"))
        gui.hSlider(sample_size, self, 'percent', minValue=1, maxValue=100, step=5, ticks=10,
                    labelFormat=" %d%%")

        gui.button(self.controlArea, self, __("btn.apply"),
                   callback=self.send_output, default=True)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.setMinimumWidth(250)
        self.send_output()

    @Inputs.data
    def set_data(self, data):
        self.data = data

        if hasattr(self.data, 'row_type'):
            self.row_type = self.data.row_type

        if hasattr(self.data, 'col_type'):
            self.col_type = self.data.col_type

        self.send_output()

    def send_output(self):
        if self.data is not None:
            relation_ = None
            if isinstance(self.data, Relation):
                relation_ = Relation(self.data.relation)
                if self.row_type:
                    relation_.relation.row_type = fusion.ObjectType(self.row_type)
                if self.col_type:
                    relation_.relation.col_type = fusion.ObjectType(self.col_type)
            else:
                relation_ = Relation.create(self.data.X,
                                            fusion.ObjectType(self.row_type or "Unknown"),
                                            fusion.ObjectType(self.col_type or "Unknown"))

            oos_mask = hide_data(relation_,
                                 self.percent / 100,
                                 SampleBy.all[self.method])

            def _mask_relation(relation, mask):
                if np.ma.is_masked(relation.data):
                    mask = np.logical_or(mask, relation.data.mask)
                data = copy.copy(relation)
                data.data = np.ma.array(data.data, mask=mask)
                return data

            oos_mask = _mask_relation(relation_.relation, oos_mask)

            self.Outputs.in_sample_data.send(Relation(oos_mask))
            self.Outputs.out_of_sample_data.send(Relation(oos_mask))


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ow = OWSampleMatrix()
    # ow.set_data(Orange.data.Table("housing.tab"))
    ow.send_output()
    ow.show()
    app.exec_()
