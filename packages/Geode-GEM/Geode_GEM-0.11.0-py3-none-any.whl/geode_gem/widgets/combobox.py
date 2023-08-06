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
from gi.repository import Gtk


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class CommonComboBox(GeodeGtkCommon):

    def __init__(self, subclass, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        subclass : Gtk.Entry
            Subclass widget type
        """

        GeodeGtkCommon.__init__(self, subclass, **kwargs)

        # Packing
        for element in args:
            self.append_widget(element)

    def append_widget(self, widget, *args, **kwargs):
        """ See geode_gem.widgets.common.GeodeGtkCommon.append_widget
        """

        super().append_widget(widget, *args, **kwargs)

        if isinstance(widget, Gtk.TreeModel):
            self.set_model(widget)

        elif isinstance(widget, Gtk.CellRenderer):
            self.pack_start(widget, widget.is_expandable)

            for attribute, value in widget.attributes.items():
                self.add_attribute(widget, attribute, value)


class GeodeGtkComboBox(CommonComboBox, Gtk.ComboBox):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonComboBox.__init__(self, Gtk.ComboBox, *args, **kwargs)


class GeodeGtkComboBoxText(CommonComboBox, Gtk.ComboBoxText):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonComboBox.__init__(self, Gtk.ComboBoxText, *args, **kwargs)
