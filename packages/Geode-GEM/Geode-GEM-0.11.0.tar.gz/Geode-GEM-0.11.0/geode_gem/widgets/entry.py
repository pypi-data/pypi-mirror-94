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
from gi.repository import GdkPixbuf, Gio, Gtk


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class CommonEntry(GeodeGtkCommon):

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

    def set_completion_data(self, identifier, *args):
        """ Set entry completion data

        Parameters
        ----------
        identifier : str
            String to identify this object in internal container
        """

        if not self.get_completion() or not self.has_widget(identifier):
            return

        widget = self.get_widget(identifier)

        widget.list_model.clear()
        for element in args:
            widget.list_model.append([element])

    def append_widget(self, widget, *args, **kwargs):
        """ See geode_gem.widgets.common.GeodeGtkCommon.append_widget

        Allow to manage completion and entry icons
        """

        super().append_widget(widget, *args, **kwargs)

        if isinstance(widget, GeodeGtkEntryCompletion):
            self.set_completion(widget)

        elif isinstance(widget, GeodeGtkEntryIcon):
            method = "set_icon_from_icon_name"

            if isinstance(widget.widget, Gio.Icon):
                method = "set_icon_from_gicon"

            elif isinstance(widget.widget, GdkPixbuf.Pixbuf):
                method = "set_icon_from_pixbuf"

            getattr(self, method)(widget.position, widget.widget)
            self.set_icon_tooltip_markup(widget.position, widget.tooltip_text)
            self.set_icon_activatable(widget.position, widget.is_activatable)


class GeodeGtkEntry(CommonEntry, Gtk.Entry):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonEntry.__init__(self, Gtk.Entry, *args, **kwargs)


class GeodeGtkEntryCompletion(GeodeGtkCommon, Gtk.EntryCompletion):

    __setters__ = {
        "set_match_func": None,
        "set_popup_completion": True,
        "set_popup_single_match": True,
    }

    def __init__(self, model, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        model : Gtk.TreeStore
            Completion model
        """

        GeodeGtkCommon.__init__(self, Gtk.EntryCompletion, **kwargs)

        self.list_model = model

        # Settings
        self.set_model(model)


class GeodeGtkEntryIcon():

    def __init__(self, position, widget, **kwargs):
        """ Constructor

        Parameters
        ----------
        position : Gtk.EntryIconPosition
            Icon position in Gtk.Entry widget
        widget : Gio.Icon or str or GdkPixbuf.Pixbuf
            Icon widget
        """

        self.position = position
        self.widget = widget

        # Properties
        self.tooltip_text = kwargs.get("tooltip", str())
        self.is_activatable = kwargs.get("is_activatable", False)


class GeodeGtkSearchEntry(CommonEntry, Gtk.SearchEntry):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonEntry.__init__(self, Gtk.SearchEntry, *args, **kwargs)
