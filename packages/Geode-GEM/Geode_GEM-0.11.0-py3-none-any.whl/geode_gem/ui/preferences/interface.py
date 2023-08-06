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

# Filesystem
from pathlib import Path

# GEM
from geode_gem.engine.api import GEM
from geode_gem.engine.utils import get_binary_path
from geode_gem.engine.console import Console
from geode_gem.engine.emulator import Emulator

from geode_gem.ui.data import Icons
from geode_gem.ui.dialog.question import QuestionDialog
from geode_gem.ui.widgets.window import CommonWindow
from geode_gem.ui.preferences.console import ConsolePreferences
from geode_gem.ui.preferences.emulator import EmulatorPreferences
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import Gdk, GdkPixbuf, GLib, Gtk, Pango

# Translation
from gettext import gettext as _


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class Manager(object):
    CONSOLE = 0
    EMULATOR = 1


class PreferencesWindow(CommonWindow):

    def __init__(self, api, parent):
        """ Constructor

        Parameters
        ----------
        api : gem.engine.api.GEM
            GEM API instance
        parent : Gtk.Window or None, optional
            Parent window for transient mode (default: None)

        Raises
        ------
        TypeError
            if api type is not gem.engine.api.GEM
        """

        if type(api) is not GEM:
            raise TypeError("Wrong type for api, expected gem.engine.api.GEM")

        CommonWindow.__init__(self,
                              parent,
                              _("Preferences"),
                              Icons.Symbolic.PREFERENCES,
                              parent.use_classic_theme)

        # ------------------------------------
        #   Initialize variables
        # ------------------------------------

        # API instance
        self.api = parent.api
        # Main configuration files
        self.config = parent.config
        # Main logger
        self.logger = self.api.logger

        self.shortcuts_data = {
            _("Interface"): {
                "fullscreen": [
                    _("Switch between fullscreen modes"), "F11"],
                "sidebar": [
                    _("Show sidebar"), "F9"],
                "statusbar": [
                    _("Show statusbar"), "<Control>F9"],
                "gem": [
                    _("Open main log"), "<Control>L"],
                "preferences": [
                    _("Open preferences"), "<Control>P"],
                "quit": [
                    _("Quit application"), "<Control>Q"]
            },
            _("Game"): {
                "start": [
                    _("Launch a game"), "<Control>Return"],
                "favorite": [
                    _("Mark a game as favorite"), "F3"],
                "multiplayer": [
                    _("Mark a game as multiplayer"), "F4"],
                "finish": [
                    _("Mark a game as finished"), "<Control>F3"],
                "snapshots": [
                    _("Show a game screenshots"), "F5"],
                "log": [
                    _("Open a game log"), "F6"],
                "notes": [
                    _("Open a game notes"), "F7"],
                "memory": [
                    _("Generate a backup memory file"), "F8"]
            },
            _("Score"): {
                "score-up": [
                    _("Increase selected game score"), "<Control>Page_Up"],
                "score-down": [
                    _("Decrease selected game score"), "<Control>Page_Down"],
                "score-0": [
                    _("Set selected game score as 0"), "<Primary>0"],
                "score-1": [
                    _("Set selected game score as 1"), "<Primary>1"],
                "score-2": [
                    _("Set selected game score as 2"), "<Primary>2"],
                "score-3": [
                    _("Set selected game score as 3"), "<Primary>3"],
                "score-4": [
                    _("Set selected game score as 4"), "<Primary>4"],
                "score-5": [
                    _("Set selected game score as 5"), "<Primary>5"]
            },
            _("Edit"): {
                "maintenance": [
                    _("Open a game maintenance dialog"), "<Control>D"],
                "delete": [
                    _("Remove a game from disk"), "<Control>Delete"],
                "rename": [
                    _("Rename a game"), "F2"],
                "duplicate": [
                    _("Duplicate a game"), "<Control>U"],
                "cover": [
                    _("Set a game thumbnail"), "<Control>I"],
                "exceptions": [
                    _("Set specific arguments for a game"), "F12"],
                "edit-file": [
                    _("Edit a game file"), "<Control>M"],
                "open": [
                    _("Open selected game directory"), "<Control>O"],
                "copy": [
                    _("Copy selected game path"), "<Control>C"],
                "desktop": [
                    _("Generate desktop entry for a game"), "<Control>G"]
            }
        }

        self.lines_data = {
            _("None"): "none",
            _("Horizontal"): "horizontal",
            _("Vertical"): "vertical",
            _("Both"): "both"
        }

        self.sidebar_data = {
            _("Right"): "horizontal",
            _("Bottom"): "vertical"
        }

        self.toolbar_data = {
            _("Menu"): "menu",
            _("Small Toolbar"): "small-toolbar",
            _("Large Toolbar"): "large-toolbar",
            _("Button"): "button",
            _("Drag and Drop"): "dnd",
            _("Dialog"): "dialog"
        }

        self.tooltips_data = {
            _("Display screenshot or thumbnail"): "both",
            _("Display screenshot only"): "screenshot",
            _("Display thumbnail only"): "cover",
            _("Hide"): "none"
        }

        self.storages = {
            "consoles": {
                "rows": dict(),
                "objects": dict()
            },
            "emulators": {
                "rows": dict(),
                "objects": dict()
            },
        }

        self.threads = {
            "consoles": int(),
            "emulators": int(),
        }

        # ------------------------------------
        #   Prepare interface
        # ------------------------------------

        # Init widgets
        self.__init_widgets()

        # Init packing
        self.__init_packing()

        # Init signals
        self.__init_signals()

        # Start interface
        self.__start_interface()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.set_resizable(True)

        self.set_border_width(6)
        self.set_spacing(6)

        self.button_cancel = self.add_button(
            _("Close"), Gtk.ResponseType.CLOSE)

        self.button_save = self.add_button(
            _("Accept"), Gtk.ResponseType.APPLY, Gtk.Align.END)

        # ------------------------------------
        #   Sidebar stack
        # ------------------------------------

        self.sidebar = GeodeGtk.StackSidebar(
            GeodeGtk.StackView(
                _("General"),
                GeodeGtk.StackSection(
                    _("Behavior"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Restore last console"),
                                GeodeGtk.Switch(
                                    identifier="restore_last_console",
                                ),
                                description=_("Restore the last selected "
                                              "console on starting"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Restore sorted column"),
                                GeodeGtk.Switch(
                                    identifier="restore_sorted_column",
                                ),
                                description=_("Restore the last sorted column "
                                              "on starting"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Hide empty consoles"),
                                GeodeGtk.Switch(
                                    identifier="hide_empty_console",
                                ),
                                description=_("Hide consoles without games"),
                            ),
                        ),
                    ),
                ),
                GeodeGtk.StackSection(
                    _("Editor"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Line numbers"),
                                GeodeGtk.Switch(
                                    identifier="textview_line_numbers",
                                ),
                                description=_("Show line number at beginning "
                                              "of each line"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Tab width"),
                                GeodeGtk.SpinButton(
                                    identifier="textview_tab_width",
                                    set_range=(1.0, 40.0),
                                    set_increments=(1, 4),
                                    set_numeric=True,
                                    set_digits=0,
                                ),
                                description=_("Width of a tab character in "
                                              "spaces"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Color scheme"),
                                GeodeGtk.ComboBox(
                                    Gtk.ListStore(str, str),
                                    GeodeGtk.CellRendererText(
                                        attributes={
                                            "text": 1,
                                        },
                                        set_alignment=(0, 0.5),
                                    ),
                                    identifier="textview_color_scheme",
                                    is_expandable=True,
                                    is_fillable=True,
                                    set_id_column=1,
                                ),
                                homogeneous=True,
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Font"),
                                GeodeGtk.FontButton(
                                    identifier="textview_font",
                                    is_expandable=True,
                                    is_fillable=True,
                                    use_ellipsize=True,
                                ),
                                homogeneous=True,
                            ),
                        ),
                    ),
                    identifier="textview_section",
                ),
                GeodeGtk.StackSection(
                    _("Screenshots viewer"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Enable alternative application"),
                                GeodeGtk.Switch(
                                    identifier="enable_alternative_viewer",
                                ),
                                description=_("Allow to use an alternative "
                                              "screenshots viewer"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Executable"),
                                GeodeGtk.FileChooserButton(
                                    identifier="viewer_executable",
                                    is_expandable=True,
                                    is_fillable=True,
                                ),
                                identifier="listbox_item_executable",
                                homogeneous=True,
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Arguments"),
                                GeodeGtk.SearchEntry(
                                    GeodeGtk.EntryIcon(
                                        Gtk.EntryIconPosition.PRIMARY,
                                        Icons.Symbolic.TERMINAL,
                                    ),
                                    identifier="viewer_arguments",
                                    is_expandable=True,
                                    is_fillable=True,
                                ),
                                identifier="listbox_item_arguments",
                                homogeneous=True,
                            ),
                        ),
                    ),
                ),
            ),
            GeodeGtk.StackView(
                _("Interface"),
                GeodeGtk.StackSection(
                    _("Appearance"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Switch to classic theme"),
                                GeodeGtk.Switch(
                                    identifier="enable_classic_theme",
                                ),
                                description=_("Use a GTK+2 like appearance "
                                              "(Restart application is "
                                              "needed)"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Enable close buttons"),
                                GeodeGtk.Switch(
                                    identifier="enable_close_buttons",
                                ),
                                identifier="listbox_item_header_buttons",
                                description=_("Display headerbar close "
                                              "buttons"),
                            ),
                        ),
                    ),
                ),
                GeodeGtk.StackSection(
                    _("Toolbar"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Icons size"),
                                GeodeGtk.ComboBox(
                                    Gtk.ListStore(str, str),
                                    GeodeGtk.CellRendererText(
                                        attributes={
                                            "text": 1,
                                        },
                                        set_alignment=(0, 0.5),
                                    ),
                                    identifier="toolbar_icons_size",
                                    is_expandable=True,
                                    is_fillable=True,
                                    set_id_column=0,
                                ),
                                description=_("Set the toolbar icons size"),
                                homogeneous=True,
                            ),
                        ),
                    ),
                ),
                GeodeGtk.StackSection(
                    _("Sidebar"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Enable sidebar"),
                                GeodeGtk.Switch(
                                    identifier="enable_sidebar",
                                ),
                                description=_("Display a sidebar next to "
                                              "games view"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Position"),
                                GeodeGtk.ComboBox(
                                    Gtk.ListStore(str, str),
                                    GeodeGtk.CellRendererText(
                                        attributes={
                                            "text": 1,
                                        },
                                        set_alignment=(0, 0.5),
                                    ),
                                    identifier="sidebar_position",
                                    is_expandable=True,
                                    is_fillable=True,
                                    set_id_column=0,
                                ),
                                identifier="listbox_item_position",
                                description=_("Set sidebar position as for "
                                              "games view"),
                                homogeneous=True,
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Enable randomize screenshot"),
                                GeodeGtk.Switch(
                                    identifier="enable_sidebar_random_image",
                                ),
                                identifier="listbox_item_randomize",
                                description=_("Use a random game screenshot "
                                              "instead of latest"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Enable ellipsize title mode"),
                                GeodeGtk.Switch(
                                    identifier="enable_sidebar_ellipsize",
                                ),
                                identifier="listbox_item_ellipsize",
                                description=_("Add an ellipsis to title when "
                                              "there is not enough space"),
                            ),
                        ),
                    ),
                ),
                GeodeGtk.StackSection(
                    _("Date"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Date format"),
                                GeodeGtk.SearchEntry(
                                    GeodeGtk.EntryIcon(
                                        Gtk.EntryIconPosition.PRIMARY,
                                        Icons.Symbolic.CALENDAR,
                                    ),
                                    identifier="date_format",
                                    is_expandable=True,
                                    is_fillable=True,
                                ),
                                description=_("String representation for date "
                                              "value"),
                                homogeneous=True,
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Datetime format"),
                                GeodeGtk.SearchEntry(
                                    GeodeGtk.EntryIcon(
                                        Gtk.EntryIconPosition.PRIMARY,
                                        Icons.Symbolic.CALENDAR,
                                    ),
                                    identifier="datetime_format",
                                    is_expandable=True,
                                    is_fillable=True,
                                ),
                                description=_("String representation for date "
                                              "with time value"),
                                homogeneous=True,
                            ),
                        ),
                    ),
                    Gtk.LinkButton.new_with_label(
                        "https://docs.python.org/3/library/datetime.html"
                        "#strftime-and-strptime-format-codes",
                        _("More information about datetime string format")),
                ),
            ),
            GeodeGtk.StackView(
                _("Games"),
                GeodeGtk.StackSection(
                    _("List view"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Grid lines"),
                                GeodeGtk.ComboBox(
                                    Gtk.ListStore(str, str),
                                    GeodeGtk.CellRendererText(
                                        attributes={
                                            "text": 1,
                                        },
                                        set_alignment=(0, 0.5),
                                    ),
                                    identifier="treeview_lines",
                                    is_expandable=True,
                                    is_fillable=True,
                                    set_id_column=0,
                                ),
                                description=_("Display background lines in "
                                              "games list view"),
                                homogeneous=True,
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Enable symbolic icons"),
                                GeodeGtk.Switch(
                                    identifier="enable_symbolic_icons",
                                ),
                                description=_("Display monochrome icons in "
                                              "games views instead of colored "
                                              "ones"),
                            ),
                        ),
                    ),
                ),
                GeodeGtk.StackSection(
                    _("Tooltip"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Enable tooltip"),
                                GeodeGtk.Switch(
                                    identifier="enable_tooltip",
                                ),
                                description=_("Display a tooltip when the "
                                              "mouse hovers a game"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Tooltip image"),
                                GeodeGtk.ComboBox(
                                    Gtk.ListStore(str, str),
                                    GeodeGtk.CellRendererText(
                                        attributes={
                                            "text": 1,
                                        },
                                        set_alignment=(0, 0.5),
                                    ),
                                    identifier="display_tooltip_image",
                                    is_expandable=True,
                                    is_fillable=True,
                                    set_id_column=0,
                                ),
                                identifier="listbox_item_tooltip_image",
                                description=_("Display an image in game "
                                              "tooltip"),
                                homogeneous=True,
                            ),
                        ),
                    ),
                ),
                GeodeGtk.StackSection(
                    _("Columns visibility"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Favorite"),
                                GeodeGtk.Switch(
                                    identifier="column_favorite",
                                ),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Multiplayer"),
                                GeodeGtk.Switch(
                                    identifier="column_multiplayer",
                                ),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Finish"),
                                GeodeGtk.Switch(
                                    identifier="column_finish",
                                ),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Launch number"),
                                GeodeGtk.Switch(
                                    identifier="column_played",
                                ),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Last launch date"),
                                GeodeGtk.Switch(
                                    identifier="column_last_launch",
                                ),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Play time"),
                                GeodeGtk.Switch(
                                    identifier="column_play_time",
                                ),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Score"),
                                GeodeGtk.Switch(
                                    identifier="column_score",
                                ),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Installed date"),
                                GeodeGtk.Switch(
                                    identifier="column_installed",
                                ),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Emulator flags"),
                                GeodeGtk.Switch(
                                    identifier="column_flags",
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            GeodeGtk.StackView(
                _("Shortcuts"),
                GeodeGtk.Box(
                    GeodeGtk.Label(
                        set_halign=Gtk.Align.START,
                        set_justify=Gtk.Justification.FILL,
                        set_line_wrap=True,
                        set_line_wrap_mode=Pango.WrapMode.WORD,
                        set_text=("You can edit interface shortcuts for some "
                                  "actions. Click on a shortcut and insert "
                                  "wanted shortcut with your keyboard."),
                    ),
                    GeodeGtk.Frame(
                        GeodeGtk.ScrolledWindow(
                            GeodeGtk.TreeView(
                                Gtk.TreeStore(str, str, str, bool),
                                GeodeGtk.TreeViewColumn(
                                    _("Action"),
                                    GeodeGtk.CellRendererText(
                                        attributes={
                                            "text": 0,
                                        },
                                        is_expandable=True,
                                        set_alignment=(0, 0.5),
                                        set_padding=(4, 0),
                                    ),
                                    set_expand=True,
                                ),
                                GeodeGtk.TreeViewColumn(
                                    _("Shortcut"),
                                    GeodeGtk.CellRendererAccel(
                                        attributes={
                                            "text": 1,
                                            "sensitive": 3,
                                        },
                                        properties={
                                            "editable": True,
                                        },
                                        identifier="cell_shortcut_key",
                                        is_expandable=True,
                                        set_alignment=(0, 0.5),
                                        set_padding=(4, 0),
                                    ),
                                    set_expand=True,
                                ),
                                identifier="shortcuts",
                                set_headers_clickable=False,
                            ),
                        ),
                        is_expandable=True,
                        is_fillable=True,
                    ),
                    is_expandable=True,
                    is_fillable=True,
                    set_orientation=Gtk.Orientation.VERTICAL,
                    set_spacing=12,
                ),
            ),
            GeodeGtk.StackView(
                _("Consoles"),
                GeodeGtk.Box(
                    GeodeGtk.Box(
                        GeodeGtk.Box(
                            GeodeGtk.Button(
                                _("Add a new console"),
                                icon_name=Icons.Symbolic.ADD,
                                identifier="button_consoles_add",
                            ),
                            GeodeGtk.Button(
                                _("Modify selected console"),
                                icon_name=Icons.Symbolic.EDIT,
                                identifier="button_consoles_modify",
                                set_sensitive=False,
                            ),
                            GeodeGtk.Button(
                                _("Remove selected console"),
                                icon_name=Icons.Symbolic.REMOVE,
                                identifier="button_consoles_remove",
                                set_sensitive=False,
                            ),
                            merge=True,
                        ),
                        None,
                        GeodeGtk.SearchEntry(
                            identifier="entry_consoles",
                            set_placeholder_text=_("Filter..."),
                        ),
                    ),
                    GeodeGtk.Frame(
                        GeodeGtk.ScrolledWindow(
                            GeodeGtk.TreeView(
                                Gtk.ListStore(
                                    GdkPixbuf.Pixbuf,   # Console icon
                                    str,                # Console name
                                    str,                # Console path status
                                    object              # Console object
                                ),
                                GeodeGtk.TreeViewColumn(
                                    _("Console"),
                                    GeodeGtk.CellRendererPixbuf(
                                        attributes={
                                            "pixbuf": 0,
                                        },
                                        set_padding=(6, 6),
                                    ),
                                    GeodeGtk.CellRendererText(
                                        attributes={
                                            "markup": 1,
                                        },
                                        is_expandable=True,
                                        set_alignment=(0, 0.5),
                                        set_padding=(6, 6),
                                    ),
                                    GeodeGtk.CellRendererPixbuf(
                                        attributes={
                                            "icon-name": 2,
                                        },
                                        set_padding=(6, 6),
                                    ),
                                    set_expand=True,
                                    sort_column_id=1,
                                ),
                                identifier="consoles",
                                filterable=True,
                                sorterable=True,
                                set_headers_clickable=False,
                                set_headers_visible=False,
                                visible_func=self.check_item_is_visible,
                            ),
                        ),
                        is_expandable=True,
                        is_fillable=True,
                    ),
                    is_expandable=True,
                    is_fillable=True,
                    set_orientation=Gtk.Orientation.VERTICAL,
                    set_spacing=12,
                ),
            ),
            GeodeGtk.StackView(
                _("Emulators"),
                GeodeGtk.Box(
                    GeodeGtk.Box(
                        GeodeGtk.Box(
                            GeodeGtk.Button(
                                _("Add a new emulator"),
                                icon_name=Icons.Symbolic.ADD,
                                identifier="button_emulators_add",
                            ),
                            GeodeGtk.Button(
                                _("Modify selected emulator"),
                                icon_name=Icons.Symbolic.EDIT,
                                identifier="button_emulators_modify",
                                set_sensitive=False,
                            ),
                            GeodeGtk.Button(
                                _("Remove selected emulator"),
                                icon_name=Icons.Symbolic.REMOVE,
                                identifier="button_emulators_remove",
                                set_sensitive=False,
                            ),
                            merge=True,
                        ),
                        None,
                        GeodeGtk.SearchEntry(
                            identifier="entry_emulators",
                            set_placeholder_text=_("Filter..."),
                        ),
                    ),
                    GeodeGtk.Frame(
                        GeodeGtk.ScrolledWindow(
                            GeodeGtk.TreeView(
                                Gtk.ListStore(
                                    GdkPixbuf.Pixbuf,   # Emulator icon
                                    str,                # Emulator name
                                    str,                # Emulator binary status
                                    object              # Emulator object
                                ),
                                GeodeGtk.TreeViewColumn(
                                    _("Emulator"),
                                    GeodeGtk.CellRendererPixbuf(
                                        attributes={
                                            "pixbuf": 0,
                                        },
                                        set_padding=(6, 6),
                                    ),
                                    GeodeGtk.CellRendererText(
                                        attributes={
                                            "markup": 1,
                                        },
                                        is_expandable=True,
                                        set_alignment=(0, 0.5),
                                        set_padding=(6, 6),
                                    ),
                                    GeodeGtk.CellRendererPixbuf(
                                        attributes={
                                            "icon-name": 2,
                                        },
                                        set_padding=(6, 6),
                                    ),
                                    set_expand=True,
                                    sort_column_id=1,
                                ),
                                identifier="emulators",
                                filterable=True,
                                sorterable=True,
                                set_headers_clickable=False,
                                set_headers_visible=False,
                                visible_func=self.check_item_is_visible,
                            ),
                        ),
                        is_expandable=True,
                        is_fillable=True,
                    ),
                    is_expandable=True,
                    is_fillable=True,
                    set_orientation=Gtk.Orientation.VERTICAL,
                    set_spacing=12,
                ),
            ),
            is_expandable=True,
            is_fillable=True,
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        # Main widgets
        self.pack_start(self.sidebar, True, True)

    def __init_signals(self):
        """ Initialize widgets signals
        """

        self.logger.info("Associate signals to preferences dialog")

        signals = {
            self.window: {
                "delete-event": [
                    {"method": self.__stop_interface},
                ],
            },
            self.button_cancel: {
                "clicked": [
                    {"method": self.__stop_interface},
                ],
            },
            self.button_save: {
                "clicked": [
                    {"method": self.__stop_interface},
                ],
            },
            self.sidebar: {
                "state-set": [
                    {
                        "method": self.__on_check_native_viewer,
                        "widget": "enable_alternative_viewer",
                    },
                    {
                        "method": self.__on_check_classic_theme,
                        "widget": "enable_classic_theme",
                    },
                    {
                        "method": self.__on_check_sidebar,
                        "widget": "enable_sidebar",
                    },
                    {
                        "method": self.__on_check_tooltip,
                        "widget": "enable_tooltip",
                    },
                ],
                "accel-cleared": [
                    {
                        "method": self.__clear_keys,
                        "widget": "cell_shortcut_key",
                    }
                ],
                "accel-edited": [
                    {
                        "method": self.__edit_keys,
                        "widget": "cell_shortcut_key",
                    }
                ],
                "changed": [
                    {
                        "method": self.on_refilter_treeiters,
                        "args": ("consoles",),
                        "widget": "entry_consoles",
                    },
                    {
                        "method": self.on_refilter_treeiters,
                        "args": ("emulators",),
                        "widget": "entry_emulators",
                    },
                ],
                "clicked": [
                    {
                        "method": self.__on_append_item,
                        "widget": "button_consoles_add",
                    },
                    {
                        "method": self.__on_modify_item,
                        "widget": "button_consoles_modify",
                    },
                    {
                        "method": self.__on_remove_item,
                        "widget": "button_consoles_remove",
                    },
                    {
                        "method": self.__on_append_item,
                        "widget": "button_emulators_add",
                    },
                    {
                        "method": self.__on_modify_item,
                        "widget": "button_emulators_modify",
                    },
                    {
                        "method": self.__on_remove_item,
                        "widget": "button_emulators_remove",
                    },
                ],
                "cursor-changed": [
                    {
                        "method": self.__on_selected_treeview,
                        "widget": "consoles",
                    },
                    {
                        "method": self.__on_selected_treeview,
                        "widget": "emulators",
                    },
                ],
                "row-activated": [
                    {
                        "method": self.__on_modify_item,
                        "widget": "consoles",
                    },
                    {
                        "method": self.__on_modify_item,
                        "widget": "emulators",
                    },
                ],
            },
        }

        # Connect widgets
        self.main_parent.load_signals(signals)
        # Remove signals storage from memory
        del signals

    def __start_interface(self):
        """ Load data and start interface
        """

        self.widgets = {

            # ------------------------------------
            #   General - Behavior
            # ------------------------------------

            "restore_last_console": {
                "type": Gtk.Switch,
                "section": "gem",
                "option": "load_console_startup",
                "fallback": True
            },
            "restore_sorted_column": {
                "type": Gtk.Switch,
                "section": "gem",
                "option": "load_sort_column_startup",
                "fallback": True
            },
            "hide_empty_console": {
                "type": Gtk.Switch,
                "section": "gem",
                "option": "hide_empty_console",
                "fallback": False
            },

            # ------------------------------------
            #   General - Editor
            # ------------------------------------

            "textview_line_numbers": {
                "type": Gtk.Switch,
                "section": "editor",
                "option": "lines",
                "fallback": True
            },
            "textview_tab_width": {
                "type": Gtk.SpinButton,
                "section": "editor",
                "option": "tab",
                "fallback": 4
            },
            "textview_color_scheme": {
                "type": Gtk.ComboBox,
                "section": "editor",
                "option": "colorscheme",
                "fallback": "classic"
            },
            "textview_font": {
                "type": Gtk.FontButton,
                "section": "editor",
                "option": "font",
                "fallback": "Sans 12"
            },

            # ------------------------------------
            #   General - Viewer
            # ------------------------------------

            "enable_alternative_viewer": {
                "type": Gtk.Switch,
                "section": "viewer",
                "option": "native",
                "fallback": True,
                "reverse": True
            },
            "viewer_executable": {
                "type": Gtk.FileChooserButton,
                "section": "viewer",
                "option": "binary",
                "fallback": "/usr/bin/feh"
            },
            "viewer_arguments": {
                "type": Gtk.Entry,
                "section": "viewer",
                "option": "options",
                "fallback": "-x -d --force-aliasing -Z -q -g 700x600 -B black"
            },

            # ------------------------------------
            #   Interface - Appearance
            # ------------------------------------

            "enable_classic_theme": {
                "type": Gtk.Switch,
                "section": "gem",
                "option": "use_classic_theme",
                "fallback": True
            },
            "enable_close_buttons": {
                "type": Gtk.Switch,
                "section": "gem",
                "option": "show_header",
                "fallback": True
            },

            # ------------------------------------
            #   Interface - Toolbar
            # ------------------------------------

            "toolbar_icons_size": {
                "type": Gtk.ComboBox,
                "section": "gem",
                "option": "toolbar_icons_size",
                "fallback": "small-toolbar"
            },

            # ------------------------------------
            #   Interface - Sidebar
            # ------------------------------------

            "enable_sidebar": {
                "type": Gtk.Switch,
                "section": "gem",
                "option": "show_sidebar",
                "fallback": True
            },
            "sidebar_position": {
                "type": Gtk.ComboBox,
                "section": "gem",
                "option": "sidebar_orientation",
                "fallback": "vertical"
            },
            "enable_sidebar_random_image": {
                "type": Gtk.Switch,
                "section": "gem",
                "option": "show_random_screenshot",
                "fallback": True
            },
            "enable_sidebar_ellipsize": {
                "type": Gtk.Switch,
                "section": "gem",
                "option": "sidebar_title_ellipsize",
                "fallback": True
            },

            # ------------------------------------
            #   Interface - Date format
            # ------------------------------------

            "date_format": {
                "type": Gtk.Entry,
                "section": "date",
                "option": "date_format",
                "fallback": "%x"
            },
            "datetime_format": {
                "type": Gtk.Entry,
                "section": "date",
                "option": "datetime_format",
                "fallback": "%x %X"
            },

            # ------------------------------------
            #   Games - List view
            # ------------------------------------

            "treeview_lines": {
                "type": Gtk.ComboBox,
                "section": "gem",
                "option": "games_treeview_lines",
                "fallback": "none"
            },
            "enable_symbolic_icons": {
                "type": Gtk.Switch,
                "section": "treeview",
                "option": "use_symbolic_icon",
                "fallback": False
            },

            # ------------------------------------
            #   Games - Tooltip
            # ------------------------------------

            "enable_tooltip": {
                "type": Gtk.Switch,
                "section": "gem",
                "option": "show_tooltip",
                "fallback": True
            },
            "display_tooltip_image": {
                "type": Gtk.ComboBox,
                "section": "gem",
                "option": "tooltip_image_type",
                "fallback": "screenshot"
            },

            # ------------------------------------
            #   Games - Columns
            # ------------------------------------

            "column_favorite": {
                "type": Gtk.Switch,
                "section": "columns",
                "option": "favorite",
                "fallback": True
            },
            "column_multiplayer": {
                "type": Gtk.Switch,
                "section": "columns",
                "option": "multiplayer",
                "fallback": True
            },
            "column_finish": {
                "type": Gtk.Switch,
                "section": "columns",
                "option": "finish",
                "fallback": True
            },
            "column_played": {
                "type": Gtk.Switch,
                "section": "columns",
                "option": "play",
                "fallback": True
            },
            "column_last_launch": {
                "type": Gtk.Switch,
                "section": "columns",
                "option": "last_play",
                "fallback": True
            },
            "column_play_time": {
                "type": Gtk.Switch,
                "section": "columns",
                "option": "play_time",
                "fallback": True
            },
            "column_score": {
                "type": Gtk.Switch,
                "section": "columns",
                "option": "score",
                "fallback": True
            },
            "column_installed": {
                "type": Gtk.Switch,
                "section": "columns",
                "option": "installed",
                "fallback": True
            },
            "column_flags": {
                "type": Gtk.Switch,
                "section": "columns",
                "option": "flags",
                "fallback": True
            }
        }

        self.load_configuration()

        # ------------------------------------
        #   Window size
        # ------------------------------------

        width, height = self.main_parent.get_window_size_from_configuration(
            "preferences", 800, 600)

        window_size = Gdk.Geometry()
        window_size.min_width = 640
        window_size.min_height = 480
        window_size.base_width = width
        window_size.base_height = height

        self.window.resize(width, height)

        self.window.set_geometry_hints(
            self.window,
            window_size,
            Gdk.WindowHints.MIN_SIZE | Gdk.WindowHints.BASE_SIZE)

        self.set_size(window_size.base_width, window_size.base_height)

        # ------------------------------------
        #   Widgets
        # ------------------------------------

        self.show_all()
        self.sidebar.show_all()

        # Update widget sensitive status
        self.__on_check_classic_theme()
        self.__on_check_native_viewer()
        self.__on_check_sidebar()
        self.__on_check_tooltip()

        # Sort elements by name
        for key in ("consoles", "emulators"):
            self.sidebar.get_widget(key).sorted_model.set_sort_column_id(
                1, Gtk.SortType.ASCENDING)

        self.button_save.set_sensitive(False)

        # Avoid to remove console or emulator when games are launched
        if self.main_parent and self.main_parent.threads:
            for key in ("button_consoles_remove", "button_emulators_remove"):
                self.sidebar.get_widget(key).set_sensitive(False)

    def __stop_interface(self, widget=None, *args):
        """ Save data and stop interface

        Other Parameters
        ----------------
        widget : Gtk.Widget, optional
            Object which receive signal (Default: None)
        """

        for key, thread_id in self.threads.items():
            if not thread_id == 0:
                self.logger.debug(f"Remove {key} thread ID {thread_id}")
                GLib.source_remove(thread_id)

        self.window.hide()

        self.config.modify("windows", "preferences", "%dx%d" % self.get_size())
        self.config.update()

    def check_item_is_visible(self, model, row, *args):
        """ Check if a game is visible in both views based on user filters

        Parameters
        ----------
        model : Gtk.TreeModel
            Treeview model which receive signal
        row : Gtk.TreeModelRow
            Treeview current row
        """

        if model == self.sidebar.get_widget("consoles").list_model:
            entry = self.sidebar.get_widget("entry_consoles")
        elif model == self.sidebar.get_widget("emulators").list_model:
            entry = self.sidebar.get_widget("entry_emulators")

        text = entry.get_text().lower()
        if not len(text):
            return True

        return text in model.get_value(row, 3).name.lower()

    def save_configuration(self):
        """ Load configuration files and fill widgets
        """

        # Remove consoles
        for console in self.api.get_consoles():
            if console.id not in self.storages["consoles"]["objects"].keys():
                self.api.delete_console(console.id)

        # Update consoles
        for console in self.storages["consoles"]["objects"].values():
            self.api.update_console(console)

        # Remove emulators
        for emulator in self.api.get_emulators():
            if emulator.id not in self.storages["emulators"]["objects"].keys():
                self.api.delete_emulator(emulator.id)

        # Update emulators
        for emulator in self.storages["emulators"]["objects"].values():
            self.api.update_emulator(emulator)

        # Write emulators and consoles data
        self.api.write_data(GEM.Consoles, GEM.Emulators)

        for key, data in self.widgets.items():
            widget = self.sidebar.get_widget(key)

            if data["type"] == Gtk.ComboBox:
                value = widget.get_active_id()

            elif data["type"] == Gtk.Entry:
                value = widget.get_text()

            elif data["type"] == Gtk.FileChooserButton:
                value = widget.get_filename()

            elif data["type"] == Gtk.FontButton:
                value = widget.get_font()

            elif data["type"] == Gtk.SpinButton:
                value = int(widget.get_value())

            elif data["type"] == Gtk.Switch:
                value = widget.get_active()

                if "reverse" in data and data["reverse"]:
                    value = not value

            self.config.modify(data["section"], data["option"], value)

        # ------------------------------------
        #   Shortcuts
        # ------------------------------------

        model = self.sidebar.get_widget("shortcuts").get_model()

        root = model.get_iter_first()
        for line in self.__on_list_shortcuts(root):
            key, value = model.get_value(line, 2), model.get_value(line, 1)
            if key and value:
                self.config.modify("keys", key, value)

        # ------------------------------------
        #   Save data
        # ------------------------------------

        self.config.update()

    def load_configuration(self):
        """ Load configuration files and fill widgets
        """

        combobox_models = {
            "toolbar_icons_size": self.toolbar_data,
            "sidebar_position": self.sidebar_data,
            "treeview_lines": self.lines_data,
            "display_tooltip_image": self.tooltips_data,
        }

        for key, data in combobox_models.items():
            widget = self.sidebar.get_widget(key)
            if widget is None:
                continue

            self.logger.debug(f"Appends model data to '{key}' combobox")

            model = widget.get_model()
            for key, value in data.items():
                model.append([value, key])

        del combobox_models

        # ------------------------------------
        #   Editor
        # ------------------------------------

        visible_widget = False

        try:
            from gi import require_version
            require_version("GtkSource", "4")

            from gi.repository.GtkSource import StyleSchemeManager

            widget = self.sidebar.get_widget("textview_color_scheme")

            model = widget.get_model()
            for path in StyleSchemeManager().get_search_path():
                self.logger.debug(
                    f"Check {path} directory for colorscheme file")

                scheme_path = Path(path).expanduser().resolve()
                for element in sorted(scheme_path.glob("*.xml")):
                    model.append([str(element), element.stem])

            widget.set_active_id(
                self.config.item("editor", "colorscheme", "classic"))

            visible_widget = True

        # Causing by require_version
        except ValueError:
            self.logger.warning("Cannot found GtkSource module")

        # Causing by importing GtkSource
        except ImportError:
            self.logger.warning("Cannot found GtkSource module")

        except Exception:
            self.logger.exception("Cannot retrieve style schemes")

        if not visible_widget:
            self.sidebar.get_widget("textview_section").hide()

        # ------------------------------------
        #   Configuration file
        # ------------------------------------

        for key, data in self.widgets.items():
            widget = self.sidebar.get_widget(key)

            if data["type"] == Gtk.ComboBox:
                widget.set_active_id(
                    self.config.get(
                        data["section"],
                        data["option"],
                        fallback=data["fallback"]))

            elif data["type"] == Gtk.Entry:
                widget.set_text(
                    self.config.get(
                        data["section"],
                        data["option"],
                        fallback=data["fallback"]))

            elif data["type"] == Gtk.FileChooserButton:
                widget.set_filename(
                    self.config.get(
                        data["section"],
                        data["option"],
                        fallback=data["fallback"]))

            elif data["type"] == Gtk.FontButton:
                widget.set_font(
                    self.config.get(
                        data["section"],
                        data["option"],
                        fallback=data["fallback"]))

            elif data["type"] == Gtk.SpinButton:
                widget.set_value(
                    self.config.getint(
                        data["section"],
                        data["option"],
                        fallback=data["fallback"]))

            elif data["type"] == Gtk.Switch:
                value = self.config.getboolean(
                    data["section"],
                    data["option"],
                    fallback=data["fallback"])

                if "reverse" in data and data["reverse"]:
                    value = not value

                widget.set_active(value)

        # ------------------------------------
        #   Shortcuts
        # ------------------------------------

        widget = self.sidebar.get_widget("shortcuts")

        model = widget.get_model()
        for key in self.shortcuts_data.keys():
            key_iter = model.append(None, [key, None, None, False])

            for option, (string, default) in self.shortcuts_data[key].items():
                value = self.config.item("keys", option, default)

                model.append(key_iter, [string, value, option, True])

        widget.expand_all()

        # ------------------------------------
        #   Load API objects
        # ------------------------------------

        self.threads["consoles"] = GLib.idle_add(
            self.on_load_elements("consoles").__next__)
        self.threads["emulators"] = GLib.idle_add(
            self.on_load_elements("emulators").__next__)

    def on_load_elements(self, key):
        """ Load elements for a specific API object (console or emulator)

        Parameters
        ----------
        key : str
            Storage key name
        """

        # Get current thread id
        current_thread_id = self.threads[key]

        storage_rows = self.storages[key]["rows"]
        storage_rows.clear()

        storage_objects = self.storages[key]["objects"]
        storage_objects.clear()

        model = self.sidebar.get_widget(key).list_model
        model.clear()

        for element in getattr(self.api, key).values():

            # Another thread has been called by user, close this one
            if not current_thread_id == self.threads[key]:
                yield False

            treeiter = model.append(self.__on_generate_row(element))

            storage_rows[element.id] = treeiter
            storage_objects[element.id] = element

            yield True

        self.threads[key] = int()

        # Shown 'save' button only when all the objects (consoles and emulators)
        # have been loaded into treeviews
        if not any(self.threads.values()):
            self.button_save.set_sensitive(True)

        yield False

    def on_refilter_treeiters(self, widget, widget_key, *args):
        """ Refilter items list to update visible rows

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        self.sidebar.get_widget(widget_key).refilter()

    def on_update_treeview_buttons_sensitivity(self, treeview, value):
        """ Update buttons sensitivity for specified treeview

        Parameters
        ----------
        treeview : GeodeGtk.TreeView
            Object which receive signal
        value : bool
            Sensitivity status

        Raises
        ------
        AttributeError
            When specified treeview do not have identifier attribute
        """

        if not hasattr(treeview, "identifier"):
            raise AttributeError(
                f"Cannot find 'identifier' attribute for {treeview}")

        for action in ("modify", "remove"):
            self.sidebar.set_sensitive(
                value, widget=f"button_{treeview.identifier}_{action}")

    def __on_generate_row(self, data):
        """ Generate consoles data from an object

        Parameters
        ----------
        data : object
            Console or Emulator instance
        """

        status = str()

        if isinstance(data, Console):
            folder = "consoles"

            path = data.path.expanduser().resolve()

            # Show a warning icon if the games directory not exists
            if not path.exists():
                status = Icons.Symbolic.WARNING

        elif isinstance(data, Emulator):
            folder = "emulators"

            path = data.binary.expanduser()

            # Show a warning icon if the binary not exists
            if not path.exists() and len(get_binary_path(str(path))) == 0:
                status = Icons.Symbolic.WARNING

        icon = self.main_parent.get_pixbuf_from_cache(
            folder, 48, data.id, data.icon, use_cache=False)
        if icon is None:
            icon = self.main_parent.icons_blank.get(48)

        return (icon,
                "<b>%s</b>\n<small>%s</small>" % (data.name, path),
                status,
                data)

    def __edit_keys(self, widget, path, key, mods, hwcode):
        """ Edit a shortcut

        Parameters
        ----------
        widget : Gtk.CellRendererAccel
            Object which receive signal
        path : str
            Path identifying the row of the edited cell
        key : int
            New accelerator keyval
        mods : Gdk.ModifierType
            New acclerator modifier mask
        hwcode : int
            Keycode of the new accelerator
        """

        model = self.sidebar.get_widget("shortcuts").get_model()

        treeiter = model.get_iter(path)
        if model.iter_parent(treeiter) is not None:
            if Gtk.accelerator_valid(key, mods):
                model.set_value(treeiter, 1, Gtk.accelerator_name(key, mods))

    def __clear_keys(self, widget, path):
        """ Clear a shortcut

        Parameters
        ----------
        widget : Gtk.CellRendererAccel
            Object which receive signal
        path : str
            Path identifying the row of the edited cell
        """

        model = self.sidebar.get_widget("shortcuts").get_model()

        treeiter = model.get_iter(path)
        if model.iter_parent(treeiter) is not None:
            model.set_value(treeiter, 1, None)

    def __on_list_shortcuts(self, treeiter):
        """ List treeiter from shortcuts treestore

        Parameters
        ----------
        treeiter : Gtk.TreeIter
            Current iter

        Returns
        -------
        list
            Treeiter list
        """

        model = self.sidebar.get_widget("shortcuts").get_model()

        results = list()
        while treeiter is not None:
            results.append(treeiter)

            # Check if current iter has child
            if model.iter_has_child(treeiter):
                childiter = model.iter_children(treeiter)

                results.extend(self.__on_list_shortcuts(childiter))

            treeiter = model.iter_next(treeiter)

        return results

    def __on_selected_treeview(self, treeview):
        """ Select an item in specified treeview

        Parameters
        ----------
        treeview : Gtk.TreeView
            Object which receive signal
        """

        selection = treeview.get_selection()

        if selection is not None:
            model, treeiter = selection.get_selected()

            self.on_update_treeview_buttons_sensitivity(
                treeview, treeiter is not None)

    def __on_check_classic_theme(self, widget=None, state=None):
        """ Update native viewer widget from checkbutton state

        Parameters
        ----------
        widget : Gtk.Widget, optional
            Object which receive signal (Default: None)
        state : bool or None, optional
            New status for current widget (Default: None)
        """

        widget = self.sidebar.get_widget("enable_classic_theme")

        status = not widget.get_active()
        for key in ("listbox_item_header_buttons", ):
            self.sidebar.get_widget(key).set_sensitive(status)

    def __on_check_native_viewer(self, widget=None, state=None):
        """ Update native viewer widget from checkbutton state

        Parameters
        ----------
        widget : Gtk.Widget, optional
            Object which receive signal (Default: None)
        state : bool or None, optional
            New status for current widget (Default: None)
        """

        widget = self.sidebar.get_widget("enable_alternative_viewer")

        status = widget.get_active()
        for key in ("listbox_item_executable", "listbox_item_arguments"):
            self.sidebar.get_widget(key).set_sensitive(status)

    def __on_check_sidebar(self, widget=None, state=None):
        """ Update sidebar widget from checkbutton state

        Parameters
        ----------
        widget : Gtk.Widget, optional
            Object which receive signal (Default: None)
        state : bool or None, optional
            New status for current widget (Default: None)
        """

        widget = self.sidebar.get_widget("enable_sidebar")

        status = widget.get_active()
        for key in ("listbox_item_position", "listbox_item_randomize",
                    "listbox_item_ellipsize"):
            self.sidebar.get_widget(key).set_sensitive(status)

    def __on_check_tooltip(self, widget=None, state=None):
        """ Update tooltip widget from checkbutton state

        Parameters
        ----------
        widget : Gtk.Widget, optional
            Object which receive signal (Default: None)
        state : bool or None, optional
            New status for current widget (Default: None)
        """

        widget = self.sidebar.get_widget("enable_tooltip")

        status = widget.get_active()
        for key in ("listbox_item_tooltip_image", ):
            self.sidebar.get_widget(key).set_sensitive(status)

    def __on_append_item(self, widget, *args):
        """ Append an item in the treeview

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        arguments = list()

        if widget.identifier == "button_consoles_add":
            arguments.append(self.storages["consoles"]["objects"])

            dialog_object, key = ConsolePreferences, "consoles"

        elif widget.identifier == "button_emulators_add":
            dialog_object, key = EmulatorPreferences, "emulators"

        arguments.append(self.storages["emulators"]["objects"])

        dialog = dialog_object(self, None, *arguments)
        dialog_response = dialog.run()
        data = dialog.save()

        if dialog_response == Gtk.ResponseType.APPLY and data is not None:
            storage_rows = self.storages[key]["rows"]
            storage_objects = self.storages[key]["objects"]

            if widget.identifier == "button_consoles_add":
                element = Console(self.api, **data)

                # Specified emulator not exists for the moment
                if element.emulator is None:
                    identifier = dialog.combo_emulators.get_active_id()

                    if identifier in storage_objects:
                        element.emulator = storage_objects[identifier]

            elif widget.identifier == "button_emulators_add":
                element = Emulator(**data)

            model = self.sidebar.get_widget(key).list_model
            storage_rows[element.id] = \
                model.append(self.__on_generate_row(element))
            storage_objects[element.id] = element

        dialog.destroy()

    def __on_modify_item(self, widget, *args):
        """ Modify an item in the treeview

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        if widget.identifier in ("consoles", "button_consoles_modify"):
            treeview = self.sidebar.get_widget("consoles")

        elif widget.identifier in ("emulators", "button_emulators_modify"):
            treeview = self.sidebar.get_widget("emulators")

        treeiter = treeview.get_selected_treeiter()
        if treeiter is None:
            return False

        element = treeview.inner_model.get_value(treeiter, 3)
        if element is None:
            return False

        previous_id = element.id

        # ----------------------------------------
        #   Launch dialog
        # ----------------------------------------

        if isinstance(element, Console):
            dialog = ConsolePreferences(self,
                                        element,
                                        self.storages["consoles"]["objects"],
                                        self.storages["emulators"]["objects"])

        elif isinstance(element, Emulator):
            dialog = EmulatorPreferences(
                self, element, self.storages["emulators"]["objects"])

        dialog_response = dialog.run()
        data = dialog.save()

        dialog.destroy()

        if not dialog_response == Gtk.ResponseType.APPLY or not len(data):
            return False

        if isinstance(element, Console):
            storage = self.storages["consoles"]

        elif isinstance(element, Emulator):
            storage = self.storages["emulators"]

        for key, value in data.items():
            setattr(element, key, value)

        row = self.__on_generate_row(element)
        if not previous_id == element.id:
            storage["objects"][element.id] = storage["objects"][previous_id]
            storage["rows"][element.id] = storage["rows"][previous_id]

            del storage["objects"][previous_id]
            del storage["rows"][previous_id]

        for item in row:
            treeview.set_value(
                storage["rows"][element.id], row.index(item), item)

        return True

    def __on_remove_item(self, widget):
        """ Remove an item in the treeview

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        if widget.identifier == "button_consoles_remove":
            treeview = self.sidebar.get_widget("consoles")

        elif widget.identifier == "button_emulators_remove":
            treeview = self.sidebar.get_widget("emulators")

        treeiter = treeview.get_selected_treeiter()
        if treeiter is None:
            return False

        element = treeview.get_model().get_value(treeiter, 3)
        if element is None:
            return False

        dialog = QuestionDialog(
            self, element.name, _("Do you really want to remove this entry ?"))
        dialog_response = dialog.run()
        dialog.destroy()

        if dialog_response == Gtk.ResponseType.YES:
            storage = self.storages[treeview.identifier]

            treeview.remove(storage["rows"][element.id])

            del storage["objects"][element.id]
            del storage["rows"][element.id]

        return True
