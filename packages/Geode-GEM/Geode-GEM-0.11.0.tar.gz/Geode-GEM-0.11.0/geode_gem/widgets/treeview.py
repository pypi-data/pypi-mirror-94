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
from geode_gem.widgets.common import GeodeGtkCommon
from geode_gem.widgets.view import CommonView

# GObject
from gi.repository import Gtk


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class GeodeGtkTreeView(CommonView, Gtk.TreeView):

    __setters__ = {
        "set_enable_search": True,
        "set_has_tooltip": False,
        "set_headers_clickable": True,
        "set_headers_visible": True,
        "set_search_column": -1,
        "set_show_expanders": True,
    }

    def __init__(self, model, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        """

        CommonView.__init__(self, Gtk.TreeView, model, *args, **kwargs)

        # ------------------------------------
        #   Packing
        # ------------------------------------

        for element in args:
            # Only manage TreeViewColumn objects
            if not isinstance(element, Gtk.TreeViewColumn):
                continue

            if self.is_sorterable and element.sort_column_id is not None:
                element.set_sort_column_id(element.sort_column_id)

                if self.sort_func is not None:
                    self.sorted_model.set_sort_func(
                        element.sort_column_id, self.sort_func, element)

            cells = element.get_cells()
            if cells and element.cell_data_func is not None:
                element.set_cell_data_func(cells[0], element.cell_data_func)

            self.append_widget(element)
            self.append_column(element)

        # ------------------------------------
        #   Settings
        # ------------------------------------

        self.set_model(self.inner_model)

    def get_selected_treeiter(self):
        """ See geode_gem.widgets.view.CommonView.get_selected_treeiter
        """

        selection = self.get_selection()

        if selection is not None:
            return selection.get_selected()[1]

        return None

    def select_path_and_scroll(self, treepath, **kwargs):
        """ See geode_gem.widgets.view.CommonView.select_path_and_scroll
        """

        self.set_cursor(treepath, None, kwargs.get("start_editing", False))

        self.scroll_to_cell(treepath,
                            None,
                            kwargs.get("use_align", True),
                            kwargs.get("row_align", 0.5),
                            kwargs.get("col_align", 0.5))

    def set_columns_order(self, *columns):
        """ Set columns order based on column widget keys

        Parameters
        ----------
        columns : list
            Columns widget key list
        """

        for index, key in enumerate(columns):
            if not self.has_widget(key):
                continue

            column_widget = self.get_widget(key)
            self.remove_column(column_widget)
            self.insert_column(column_widget, index)

    def unselect_all(self):
        """ Unselect any selected row from treeview widget
        """

        selection = self.get_selection()

        if selection is not None:
            selection.unselect_all()


class GeodeGtkTreeViewColumn(GeodeGtkCommon, Gtk.TreeViewColumn):

    __setters__ = {
        "set_alignment": 0.5,
        "set_expand": False,
        "set_fixed_width": -1,
        "set_max_width": -1,
        "set_min_width": -1,
        "set_resizable": True,
        "set_reorderable": True,
        "set_sizing": Gtk.TreeViewColumnSizing.GROW_ONLY,
    }

    def __init__(self, title, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        """

        GeodeGtkCommon.__init__(self, Gtk.TreeViewColumn, **kwargs)

        self.sort_column_id = kwargs.get("sort_column_id", None)

        self.cell_data_func = kwargs.get("cell_data_func", None)

        # ------------------------------------
        #   Properties
        # ------------------------------------

        if title is not None:
            self.set_title(title)

        # ------------------------------------
        #   Packing
        # ------------------------------------

        for element in args:
            self.pack_start(element, element.is_expandable)

            for attribute, value in element.attributes.items():
                self.add_attribute(element, attribute, value)

            self.append_widget(element)
