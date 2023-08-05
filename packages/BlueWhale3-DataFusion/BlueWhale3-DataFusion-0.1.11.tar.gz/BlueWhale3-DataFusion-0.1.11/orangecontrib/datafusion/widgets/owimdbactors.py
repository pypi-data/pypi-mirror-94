import sys

from AnyQt.QtWidgets import QSizePolicy

from orangecontrib.datafusion.models import Relation
from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import OWWidget, Input, Output
from orangecontrib.datafusion import movielens
from orangecontrib.datafusion.i18n_config import *

from skfusion import fusion


def __(key):
    return i18n.t("datafusion.owimdbactors." + key)


class OWIMDbActors(OWWidget):
    name = __("name")
    description = __('desc')
    priority = 80000
    icon = "icons/IMDbActors.svg"
    want_main_area = False
    resizing_enabled = False

    class Inputs:
        filter = Input('Filter', Relation, label=i18n.t("datafusion.common.filter"))

    class Outputs:
        movie_actors = Output("Movie Actors", Relation, label=i18n.t("datafusion.common.movie_actor"))
        actors_actors = Output("Costarring Actors", Relation, label=i18n.t("datafusion.common.costar_actor"))

    percent = settings.Setting(10)

    def __init__(self):
        super().__init__()
        self.movies = None
        self.infobox = gui.widgetBox(self.controlArea, __('box_select_actor'))

        percent = gui.hSlider(
            gui.indentedBox(self.infobox), self, "percent",
            minValue=1, maxValue=100, step=1, ticks=10, labelFormat="%d %%")

        gui.button(self.controlArea, self, __("btn_apply"),
                   callback=self.send_output, default=True)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.setMinimumWidth(250)
        self.setMaximumWidth(250)

        self.movies = None

    @Inputs.filter
    def set_data(self, relation):
        if relation is not None:
            assert isinstance(relation, Relation)
            if relation.col_type == movielens.ObjectType.Movies:
                self.movies = relation.relation.col_names
            elif relation.row_type == movielens.ObjectType.Movies:
                self.movies = relation.relation.row_names
            else:
                self.error(1, "Only relations with ObjectType Movies can be used to filter actors.")

            self.send_output()

    def send_output(self):
        if self.movies is not None:
            movie_actor_mat, actors = movielens.movie_concept_matrix(self.movies, concept="actor",
                                                                     actors=self.percent)
            actor_actor_mat = movielens.actor_matrix(movie_actor_mat)

            movies_actors = fusion.Relation(movie_actor_mat.T, name='play in',
                                            row_type=movielens.ObjectType.Actors, row_names=actors,
                                            col_type=movielens.ObjectType.Movies, col_names=self.movies)
            self.Outputs.movie_actors.send(Relation(movies_actors))

            actors_actors = fusion.Relation(actor_actor_mat, name='costar with',
                                            row_type=movielens.ObjectType.Actors, row_names=actors,
                                            col_type=movielens.ObjectType.Actors, col_names=actors)
            self.Outputs.actors_actors.send(Relation(actors_actors))


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ow = OWIMDbActors()
    # ow.set_data(movies_users)
    ow.show()
    app.exec_()
