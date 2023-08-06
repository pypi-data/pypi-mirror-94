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
from geode_gem.widgets.misc import GeodeGtkLabel

# GObject
from gi.repository import Gtk


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class GeodeGtkStackSidebar(GeodeGtkCommon, Gtk.Box):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.StackSidebar, **kwargs)

        self.sidebar = Gtk.StackSidebar.new()

        self.stack = kwargs.get("use_stack", Gtk.Stack())
        self.stack.set_transition_type(Gtk.StackTransitionType.NONE)

        self.sidebar.set_stack(self.stack)

        for element in args:
            self.append_widget(element)
            self.stack.add_titled(element, element.identifier, element.title)

        self.pack_start(self.sidebar, False, False, 0)
        self.pack_start(self.stack, True, True, 0)


class GeodeGtkStackView(GeodeGtkCommon, Gtk.ScrolledWindow):

    def __init__(self, title, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.ScrolledWindow, **kwargs)

        self.inner_viewport = Gtk.Viewport.new(None, None)
        self.inner_grid = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)

        self.title = title

        # ------------------------------------
        #   Properties
        # ------------------------------------

        self.inner_grid.set_border_width(16)

        # ------------------------------------
        #   Packing
        # ------------------------------------

        for element in args:
            self.append_widget(element)
            self.inner_grid.pack_start(
                element,
                getattr(element, "is_fillable", False),
                getattr(element, "is_expandable", False),
                0)

        self.add(self.inner_viewport)
        self.inner_viewport.add(self.inner_grid)


class GeodeGtkStackSection(GeodeGtkCommon, Gtk.Box):

    __setters__ = {
        "set_orientation": Gtk.Orientation.VERTICAL,
        "set_homogeneous": False,
        "set_margin_bottom": 12,
        "set_spacing": 6,
    }

    def __init__(self, title, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.Box, **kwargs)

        label_title = GeodeGtkLabel(identifier="title",
                                    set_markup=f"<b>{title}</b>",
                                    set_style=Gtk.STYLE_CLASS_DIM_LABEL)

        # Packing
        self.pack_start(label_title, False, False, 0)

        for element in args:
            self.append_widget(element)
            self.pack_start(element, True, True, 0)


class GeodeGtkStackOption(GeodeGtkCommon, Gtk.Box):

    __setters__ = {
        "set_orientation": Gtk.Orientation.HORIZONTAL,
        "set_homogeneous": False,
        "set_spacing": 12,
    }

    def __init__(self, label, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.Box, **kwargs)

        label_option = GeodeGtkLabel(identifier="label",
                                     set_alignment=(1, 0.5),
                                     set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                                     set_text=f"{label}")

        # Packing
        self.pack_start(label_option, False, False, 0)

        for element in args:
            self.append_widget(element)
            self.pack_start(element, True, True, 0)
