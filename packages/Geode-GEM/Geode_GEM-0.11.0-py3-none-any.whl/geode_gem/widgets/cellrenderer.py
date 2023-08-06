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

# GObject
from gi.repository import Gtk, Pango


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class CommonCellRenderer(GeodeGtkCommon):

    # Define properties which will be used with Gtk.CellRenderer.set_property
    __properties__ = dict()

    __setters__ = {
        "set_alignment": (0.5, 0.5),
        "set_padding": (0, 0),
    }

    def __init__(self, subclass, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        subclass : Gtk.MenuItem
            Subclass widget type
        title : str
            Menu item label
        """

        GeodeGtkCommon.__init__(self, subclass, **kwargs)

        # Store cells attributes which are used by GeodeGtkTreeViewColumn
        self.attributes = kwargs.get("attributes", dict())

        # Store cells properties
        self.properties = self.__properties__.copy()
        self.properties.update(kwargs.get("properties", dict()))

        for key, value in self.properties.items():
            self.set_property(key, value)


class GeodeGtkCellRendererAccel(CommonCellRenderer, Gtk.CellRendererAccel):

    __properties__ = {
        "placeholder-text": str(),
    }

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.treeview.CommonCellRenderer
        """

        CommonCellRenderer.__init__(
            self, Gtk.CellRendererAccel, *args, **kwargs)


class GeodeGtkCellRendererPixbuf(CommonCellRenderer, Gtk.CellRendererPixbuf):

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.treeview.CommonCellRenderer
        """

        CommonCellRenderer.__init__(
            self, Gtk.CellRendererPixbuf, *args, **kwargs)


class GeodeGtkCellRendererText(CommonCellRenderer, Gtk.CellRendererText):

    __properties__ = {
        "editable": False,
        "ellipsize": Pango.EllipsizeMode.NONE,
        "placeholder-text": str(),
    }

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.treeview.CommonCellRenderer
        """

        CommonCellRenderer.__init__(
            self, Gtk.CellRendererText, *args, **kwargs)
