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

# GObject
from gi import require_version
require_version("Gtk", "3.0")

from gi.repository import Gtk

# Logging
from logging import getLogger


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class GeodeGtkCommon():

    __setters__ = None

    def __init__(self, subclass, **kwargs):
        """ Constructor
        """

        if subclass is None:
            raise ValueError("Cannot use None as subclass")

        subclass.__init__(self)

        self.inner_grid = None
        self.inner_widgets = dict()

        # Uniq identifier
        self.identifier = kwargs.get("identifier", str(id(self)))
        # Widget class style
        self.current_style = None

        arguments = self.__setters__.copy() if self.__setters__ else dict()
        arguments.update(kwargs)

        for key, value in arguments.items():
            self.__set_widget(key, value)

        self.is_expandable = kwargs.get("is_expandable", False)
        self.is_fillable = kwargs.get("is_fillable", False)

    def __set_widget(self, method, value):
        """ Use Gtk widget methods if this one exists

        Parameters
        ----------
        method : str
            Setter method name
        value : object
            Object to use as setter method parameters

        Returns
        -------
        object
            Method result, None otherwise
        """

        if not method.startswith("set_"):
            return None

        if not hasattr(self, method):
            getLogger("gem").warning(
                f"Cannot found '{method}' in '{self.identifier}' widget")
            return None

        if value is None:
            return None

        if type(value) not in (list, tuple):
            value = (value, )

        return getattr(self, method)(*value)

    def do_show(self):
        """ Virtual method called when self.show() method is called
        """

        if hasattr(self, "do_show"):
            super().do_show(self)

        # Ensure to show all internal widgets
        if isinstance(self.inner_grid, Gtk.Container):
            self.inner_grid.show_all()

    def append_widget(self, widget, identifier=None):
        """ Check if a specific widget exists in internal container

        Parameters
        ----------
        widget : Gtk.Widget
            Gtk object instance
        identifier : str, optional
            Set a specific identifier to specified widget
        """

        if identifier is not None:
            setattr(widget, "identifier", identifier)

        if hasattr(widget, "identifier") and widget.identifier is not None:
            self.inner_widgets[widget.identifier] = widget

        if hasattr(widget, "inner_widgets"):
            self.inner_widgets.update(widget.inner_widgets)

    def has_widget(self, widget_key):
        """ Check if a specific widget exists in internal container

        Parameters
        ----------
        widget_key : str
            Internal widget keys, contains in self.inner_widgets

        Returns
        -------
        bool
            True if widget exists, False otherwise
        """

        return widget_key in self.inner_widgets.keys()

    def get_widget(self, widget_key):
        """ Retrieve a specific widget from internal container

        Parameters
        ----------
        widget_key : str
            Internal widget keys, contains in self.inner_widgets

        Returns
        -------
        Gtk.Widget or None
            Widget from internal container

        Raises
        ------
        KeyError
            When specified widget do not exists in widget
        """

        if not self.has_widget(widget_key):
            raise KeyError(f"Cannot found {widget_key} in {self} widgets")

        return self.inner_widgets.get(widget_key, None)

    def get_active(self, widget=None):
        """ Returns the widget active entry

        Parameters
        ----------
        widget : str, optionnal
            Internal widget keys, contains in self.inner_widgets

        Returns
        -------
        Gtk.Widget
            The activated widget from internal container
        """

        if widget is None:
            return super().get_active()

        elif self.has_widget(widget):
            return self.get_widget(widget).get_active()

        return None

    def set_active(self, value, widget=None):
        """ Set the active value for a specific widget

        Parameters
        ----------
        value : bool or int
            The new activate value for specified widget
        widget : str, optionnal
            Internal widget keys, contains in self.inner_widgets
        """

        if widget is None:
            super().set_active(value)

        elif self.has_widget(widget):
            self.get_widget(widget).set_active(value)

    def get_sensitive(self, widget=None):
        """ Returns the widget sensitivity

        Parameters
        ----------
        widget : str, optionnal
            Internal widget keys, contains in self.inner_widgets

        Returns
        -------
        bool
            True if the widget is sensitive, False otherwise
        """

        if widget is None:
            return super().get_sensitive()

        elif self.has_widget(widget):
            return self.get_widget(widget).get_sensitive()

        return True

    def set_sensitive(self, sensitive, widget=None):
        """ Set the widget sensitivity

        Parameters
        ----------
        sensitive : bool
            The new internal widget sensitive status
        widget : str, optionnal
            Internal widget keys, contains in self.inner_widgets
        """

        if widget is None:
            super().set_sensitive(sensitive)

        elif self.has_widget(widget):
            self.get_widget(widget).set_sensitive(sensitive)

    def get_visible(self, widget=None):
        """ Returns the widget sensitivity

        Parameters
        ----------
        widget : str, optionnal
            Internal widget keys, contains in self.inner_widgets

        Returns
        -------
        bool
            True if the widget is visible, False otherwise
        """

        if widget is None:
            return super().get_visible()

        elif self.has_widget(widget):
            return self.get_widget(widget).get_visible()

        return True

    def set_visible(self, visible, widget=None):
        """ Set the widget sensitivity

        Parameters
        ----------
        visible : bool
            The new internal widget visible status
        widget : str, optionnal
            Internal widget keys, contains in self.inner_widgets
        """

        if widget is None:
            super().set_visible(visible)

        elif self.has_widget(widget):
            self.get_widget(widget).set_visible(visible)

    def has_style(self, style, widget=None):
        """ Check if a specific class is available in specified widget

        Parameters
        ----------
        style : str
            Class style name
        widget : str, optionnal
            Internal widget keys, contains in self.inner_widgets

        Returns
        -------
        bool
            True if the widget has class, False otherwise
        """

        return style in self.get_style(widget=widget)

    def get_style(self, widget=None):
        """ Retrieve classes list for specified widget

        Parameters
        ----------
        widget : str, optionnal
            Internal widget keys, contains in self.inner_widgets

        Returns
        -------
        list
            Widget classes string list
        """

        if widget is not None and self.has_widget(widget):
            context = self.get_widget(widget).get_style_context()
        else:
            context = self.get_style_context()

        return context.list_classes()

    def set_style(self, style=None, widget=None):
        """ Define a specific class for specified widget

        Parameters
        ----------
        style : str, optional
            Class style name
        widget : str, optionnal
            Internal widget keys, contains in self.inner_widgets
        """

        if widget is not None and self.has_widget(widget):
            context = self.get_widget(widget).get_style_context()
        else:
            context = self.get_style_context()

        if self.current_style is not None and not self.current_style == style:
            context.remove_class(self.current_style)

        if style is not None and not self.current_style == style:
            context.add_class(style)

        self.current_style = style
