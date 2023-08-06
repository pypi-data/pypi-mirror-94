# ------------------------------------------------------------------------------
#  Copyleft 2015-2021  PacMiam
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
# ------------------------------------------------------------------------------

# Geode
from geode_gem.widgets.view import CommonView

# GObject
from gi.repository import Gtk


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class GeodeGtkIconView(CommonView, Gtk.IconView):

    __setters__ = {
        "set_column_spacing": 0,
        "set_has_tooltip": False,
        "set_item_width": 32,
        "set_row_spacing": 0,
        "set_selection_mode": Gtk.SelectionMode.SINGLE,
        "set_spacing": 0,
    }

    def __init__(self, model, **kwargs):
        """ Constructor

        Parameters
        ----------
        """

        CommonView.__init__(self, Gtk.IconView, model, **kwargs)

        # Settings
        self.set_model(self.inner_model)

    def get_selected_treeiter(self):
        """ See geode_gem.widgets.view.CommonView.get_selected_treeiter
        """

        items_list = self.get_selected_items()

        if items_list:
            return self.inner_model.get_iter(items_list[0])

        return None

    def select_path_and_scroll(self, treepath, **kwargs):
        """ See geode_gem.widgets.view.CommonView.select_path_and_scroll
        """

        self.select_path(treepath)

        self.scroll_to_path(treepath,
                            kwargs.get("use_align", True),
                            kwargs.get("row_align", 0.5),
                            kwargs.get("col_align", 0.5))
