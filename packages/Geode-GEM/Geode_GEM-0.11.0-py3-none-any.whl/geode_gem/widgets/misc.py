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

class CommonBox(GeodeGtkCommon):

    def __init__(self, subclass, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        """

        GeodeGtkCommon.__init__(self, subclass, **kwargs)

        # Properties
        if kwargs.get("merge", False):
            Gtk.StyleContext.add_class(self.get_style_context(), "linked")

        # Packing
        method = "pack_start"
        for element in args:
            if element is None:
                method = "pack_end"
                continue

            if not hasattr(self, method):
                method = "add"

            args = [element]
            if not issubclass(type(self), Gtk.HeaderBar) \
               and method.startswith("pack_"):
                args.extend([element.is_expandable, element.is_fillable, 0])

            getattr(self, method)(*args)
            self.append_widget(element)

            element.show_all()


class GeodeGtkBox(CommonBox, Gtk.Box):

    __setters__ = {
        "set_border_width": 0,
        "set_orientation": Gtk.Orientation.HORIZONTAL,
        "set_spacing": 0,
    }

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonBox.__init__(self, Gtk.Box, *args, **kwargs)


class GeodeGtkButtonBox(CommonBox, Gtk.ButtonBox):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonBox.__init__(self, Gtk.ButtonBox, *args, **kwargs)


class GeodeGtkFrame(CommonBox, Gtk.Frame):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonBox.__init__(self, Gtk.Frame, *args, **kwargs)


class GeodeGtkHeaderBar(CommonBox, Gtk.HeaderBar):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonBox.__init__(self, Gtk.HeaderBar, *args, **kwargs)


class GeodeGtkImage(GeodeGtkCommon, Gtk.Image):

    def __init__(self, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        """

        GeodeGtkCommon.__init__(self, Gtk.Image, **kwargs)


class GeodeGtkLabel(GeodeGtkCommon, Gtk.Label):

    __setters__ = {
        "set_use_markup": True,
        "set_use_underline": True,
        "set_ellipsize": Pango.EllipsizeMode.NONE,
    }

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.Label, **kwargs)


class GeodeGtkOverlay(GeodeGtkCommon, Gtk.Overlay):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonBox.__init__(self, Gtk.Overlay, *args, **kwargs)


class GeodeGtkPopover(GeodeGtkCommon, Gtk.Popover):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonBox.__init__(self, Gtk.Popover, *args, **kwargs)


class GeodeGtkRevealer(GeodeGtkCommon, Gtk.Revealer):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonBox.__init__(self, Gtk.Revealer, *args, **kwargs)


class GeodeGtkScrolledWindow(GeodeGtkCommon, Gtk.ScrolledWindow):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonBox.__init__(self, Gtk.ScrolledWindow, *args, **kwargs)


class GeodeGtkSpinner(GeodeGtkCommon, Gtk.Spinner):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.Spinner, **kwargs)


class GeodeGtkSwitch(GeodeGtkCommon, Gtk.Switch):

    __setters__ = {
        "set_active": True,
        "set_hexpand": False,
        "set_valign": Gtk.Align.CENTER,
    }

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.Switch, **kwargs)
