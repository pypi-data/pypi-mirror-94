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
from geode_gem.widgets.button import GeodeGtkButton
from geode_gem.widgets.common import GeodeGtkCommon
from geode_gem.widgets.misc import GeodeGtkLabel

# GObject
from gi.repository import Gtk, Pango


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class GeodeGtkListBox(GeodeGtkCommon, Gtk.ListBox):

    __setters__ = {
        "set_selection_mode": Gtk.SelectionMode.NONE,
    }

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.ListBox, **kwargs)

        self.placeholder = GeodeGtkLabel(
            set_justify=Gtk.Justification.CENTER,
            set_line_wrap=True,
            set_single_line_mode=False,
            set_style=Gtk.STYLE_CLASS_DIM_LABEL,
            set_text=kwargs.get("placeholder", str()))

        # Properties
        self.set_placeholder(self.placeholder)

        # ------------------------------------
        #   Packing
        # ------------------------------------

        self.append_widget(self.placeholder)

        self.placeholder.show()

        for element in args:
            self.add(element)

    def add(self, child):
        """ Append a new child in container

        Parameters
        ----------
        child : Gtk.Widget
            New widget to add into container
        """

        self.append_widget(child)

        super().add(child)

    def do_row_activated(self, row):
        """ Activate inner widget for specified row

        Parameters
        ----------
        row : Gtk.ListBoxRow
            Activated row widget
        """

        if isinstance(row, GeodeGtkListBoxItem):
            row.activate()


class GeodeGtkListBoxItem(GeodeGtkCommon, Gtk.ListBoxRow):

    # Used to specified if Gtk.ListBox.do_activate works with this item
    activatable = False

    def __init__(self, label, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        """

        GeodeGtkCommon.__init__(self, Gtk.ListBoxRow, **kwargs)

        self.inner_grid = Gtk.Box.new(
            kwargs.get("orientation", Gtk.Orientation.HORIZONTAL),
            kwargs.get("spacing", 12))

        self.label_grid = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        self.label_title = Gtk.Label.new(None)
        self.label_description = Gtk.Label.new(None)

        self.set_text(label, kwargs.get("description", None))

        # ------------------------------------
        #   Properties
        # ------------------------------------

        self.set_activatable(kwargs.get("activatable", True))

        self.inner_grid.set_border_width(kwargs.get("border_width", 6))
        self.inner_grid.set_homogeneous(kwargs.get("homogeneous", False))

        self.label_grid.set_homogeneous(False)

        for widget in (self.label_title, self.label_description):
            widget.set_halign(Gtk.Align.START)
            widget.set_justify(Gtk.Justification.FILL)
            widget.set_line_wrap(True)
            widget.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)

        self.label_description.set_hexpand(True)
        self.label_description.set_use_markup(True)
        self.label_description.set_no_show_all(True)
        self.label_description.set_valign(Gtk.Align.START)
        self.label_description.get_style_context().add_class(
            Gtk.STYLE_CLASS_DIM_LABEL)

        # ------------------------------------
        #   Packing
        # ------------------------------------

        self.append_widget(self.label_grid)
        self.append_widget(self.label_title)
        self.append_widget(self.label_description)

        self.label_grid.pack_start(self.label_title, True, True, 0)
        self.label_grid.pack_start(self.label_description, True, True, 0)

        self.inner_grid.pack_start(self.label_grid, True, True, 0)

        for element in args:
            self.append_widget(element)
            self.inner_grid.pack_start(
                element,
                getattr(element, "is_fillable", False),
                getattr(element, "is_expandable", False),
                0)

        self.add(self.inner_grid)

    def set_text(self, title, description=None):
        """ Set labels item content

        Parameters
        ----------
        title : str
            Title label string
        description : str, optionnal
            Description label string
        """

        self.label_title.set_label(title)
        self.label_title.set_valign(
            Gtk.Align.END if description is not None else Gtk.Align.CENTER)

        self.label_description.set_visible(description is not None)

        if description is not None:
            self.label_description.set_markup(
                f"<span size='small'>{description}</span>")

    def do_activate(self):
        """ See Gtk.Switch.do_activate()
        """

        if self.get_activatable():
            children = self.inner_grid.get_children()

            if len(children):
                widget = children[-1]

                if isinstance(widget, Gtk.ComboBox):
                    widget.popup()

                elif isinstance(widget, Gtk.FileChooserButton):
                    widget.activate()

                elif isinstance(widget, Gtk.Switch):
                    widget.set_active(not widget.get_active())

                elif issubclass(type(widget), Gtk.Button):
                    widget.clicked()

                elif issubclass(type(widget), Gtk.Entry):
                    widget.grab_focus()

                else:
                    widget.activate()


class GeodeGtkListBoxButton(GeodeGtkListBoxItem):

    activatable = True

    def __init__(self, label, *args, **kwargs):
        """ See geode_gem.ui.widgets.listbox.GeodeGtkListBoxItem
        """

        GeodeGtkListBoxItem.__init__(self, label, *args, **kwargs)

        self.button = GeodeGtkButton(
            kwargs.get("button_label", str()),
            halign=Gtk.Align.END,
            hexpand=False,
            valign=Gtk.Align.CENTER,
            **kwargs)

        # Packing
        self.append_widget(self.button)
        self.inner_grid.pack_end(self.button, False, False, 0)

    def do_activate(self):
        """ See Gtk.Switch.do_activate()
        """

        self.button.clicked()


class GeodeGtkListBoxCheckItem(GeodeGtkListBoxItem):

    activatable = True

    def __init__(self, label, *args, **kwargs):
        """ See geode_gem.ui.widgets.listbox.GeodeGtkListBoxItem
        """

        GeodeGtkListBoxItem.__init__(self, label, *args, **kwargs)

        self.switch = Gtk.Switch.new()
        setattr(self.switch, "identifier", f"{self.identifier}_switch")

        # Properties
        self.switch.set_active(kwargs.get("activate", True))
        self.switch.set_halign(Gtk.Align.END)
        self.switch.set_hexpand(False)
        self.switch.set_valign(Gtk.Align.CENTER)

        # Packing
        self.append_widget(self.switch)

        self.inner_grid.pack_end(self.switch, False, False, 0)

    def do_activate(self):
        """ See Gtk.Switch.do_activate()
        """

        self.switch.activate()
