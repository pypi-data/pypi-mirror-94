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
from geode_gem.widgets.menu import GeodeGtkMenu

# GObject
from gi.repository import Gtk, Pango


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class CommonButton(GeodeGtkCommon):

    def __init__(self, subclass, label, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        subclass : Gtk.Button
            Subclass widget type
        label : str
            String use as button label
        """

        GeodeGtkCommon.__init__(self, subclass, **kwargs)

        # Inner widgets
        self.image = None
        # Button image icon name
        self.icon_name = kwargs.get("icon_name", None)

        # ------------------------------------
        #   Properties
        # ------------------------------------

        if self.icon_name is None:
            self.set_label(label)

        else:
            self.set_tooltip_text(label)

            self.image = Gtk.Image.new_from_icon_name(self.icon_name,
                                                      Gtk.IconSize.BUTTON)
            setattr(self.image, "identifier", f"{self.identifier}_image")

        # ------------------------------------
        #   Packing
        # ------------------------------------

        if self.image is not None:
            self.append_widget(self.image)
            self.add(self.image)


class GeodeGtkButton(CommonButton, Gtk.Button):

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.button.CommonButton
        """

        CommonButton.__init__(self, Gtk.Button, *args, **kwargs)


class GeodeGtkFileChooserButton(GeodeGtkCommon, Gtk.FileChooserButton):

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.button.CommonButton
        """

        GeodeGtkCommon.__init__(self, Gtk.FileChooserButton, **kwargs)


class GeodeGtkFontButton(GeodeGtkCommon, Gtk.FontButton):

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.button.CommonButton
        """

        GeodeGtkCommon.__init__(self, Gtk.FontButton, **kwargs)

        # HACK: Set an ellipsize mode for the label inside FontButton
        if kwargs.get("use_ellipsize", False):
            for child in self.get_child():
                if type(child) == Gtk.Label:
                    child.set_ellipsize(Pango.EllipsizeMode.END)


class GeodeGtkMenuButton(CommonButton, Gtk.MenuButton):

    __setters__ = {
        "set_use_popover": False,
    }

    def __init__(self, label, *args, **kwargs):
        """ See geode_gem.ui.widgets.button.CommonButton
        """

        CommonButton.__init__(self, Gtk.MenuButton, label, *args, **kwargs)

        # Inner widgets
        self.submenu = None

        # Properties
        if args:
            self.submenu = GeodeGtkMenu(*args)
            self.append_widget(self.submenu)

        # Packing
        if self.submenu is not None:
            self.set_popup(self.submenu)
            self.submenu.show_all()


class GeodeGtkSpinButton(GeodeGtkCommon, Gtk.SpinButton):

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.button.CommonButton
        """

        GeodeGtkCommon.__init__(self, Gtk.SpinButton, **kwargs)


class GeodeGtkToggleButton(CommonButton, Gtk.ToggleButton):

    def __init__(self, *args, **kwargs):
        """ See geode_gem.ui.widgets.button.CommonButton
        """

        CommonButton.__init__(self, Gtk.ToggleButton, *args, **kwargs)
