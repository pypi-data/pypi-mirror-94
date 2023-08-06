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
from geode_gem.widgets.misc import GeodeGtkBox

# GObject
from gi.repository import Gtk


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class GeodeGtkToolbar(GeodeGtkBox):

    __setters__ = {
        "set_spacing": 0,
        "set_border_width": 0,
        "set_orientation": Gtk.Orientation.HORIZONTAL,
    }

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkBox.__init__(self, **kwargs)

        # ------------------------------------
        #   Packing
        # ------------------------------------

        for index, widget in enumerate(args):
            expand = False

            if widget is None:
                widget = Gtk.SeparatorToolItem.new()
                widget.set_expand(True)
                widget.set_draw(False)

                setattr(widget,
                        "identifier",
                        f"{self.identifier}_separator_{index}")

                expand = True

            elif len(args) == 1:
                expand = True

            self.append_widget(widget)
            self.pack_start(widget, expand, expand, 0)


class GeodeGtkToolbarBox(GeodeGtkBox):

    __setters__ = {
        "set_spacing": 0,
        "set_border_width": 0,
        "set_orientation": Gtk.Orientation.HORIZONTAL,
    }

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkBox.__init__(self, **kwargs)

        # ------------------------------------
        #   Packing
        # ------------------------------------

        method = "get_hexpand"
        if self.get_orientation() == Gtk.Orientation.VERTICAL:
            method = "get_vexpand"

        for widget in args:
            expand = False
            if hasattr(widget, method):
                expand = getattr(widget, method)()

            self.append_widget(widget)
            self.pack_start(widget, expand, expand, 0)


class GeodeGtkToolbarSwitch(GeodeGtkToolbarBox):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkToolbarBox.__init__(self, *args, **kwargs)

        # Current toggled button
        self.toggled_identifier = kwargs.get("default", None)

        if self.has_widget(self.toggled_identifier):
            self.get_widget(self.toggled_identifier).set_active(True)

    def switch_to(self, widget_key):
        """ Toggled a specific widget

        Parameters
        ----------
        widget_key : str
            Internal widget keys, contains in self.inner_widgets
        """

        widget_activated = self.get_widget(widget_key)

        # Update buttons state
        for widget in self.inner_widgets.values():
            if isinstance(widget, Gtk.Button):
                widget.set_active(widget == widget_activated)

                # Store current toggled widget identifier
                self.toggled_identifier = widget.identifier

    def get_toggled_widget(self):
        """ Retrieve current toggled widget

        Returns
        -------
        Gtk.Button or None
            Toggled widget if founded, None otherwise
        """

        if self.has_widget(self.toggled_identifier):
            return self.get_widget(self.toggled_identifier)

        return None
