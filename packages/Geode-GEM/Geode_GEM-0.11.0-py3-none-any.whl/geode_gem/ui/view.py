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

# Datetime
from datetime import timedelta

# Geode
from geode_gem.ui.data import Columns
from geode_gem.ui.utils import string_from_date, string_from_time
from geode_gem.ui.placeholder import GeodeGEMPlaceholder
from geode_gem.widgets import GeodeGtk
from geode_gem.widgets.common import GeodeGtkCommon

# GObject
from gi.repository import Gdk, GdkPixbuf, Gtk, Pango

# Python
from enum import Enum

# Translation
from gettext import gettext as _


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class CommonGamesView(GeodeGtkCommon, Gtk.ScrolledWindow):

    def __init__(self, interface, view, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        interface : geode_gem.ui.interface.MainWindow
            Main interface instance
        view : geode_gem.ui.view.CommonGamesView
            View instance
        """

        GeodeGtkCommon.__init__(self, Gtk.ScrolledWindow, **kwargs)

        self.interface = interface
        self.view = view

        self.storage = dict()

        # ------------------------------------
        #   Packing
        # ------------------------------------

        self.add(self.view)
        self.append_widget(self.view)

    def clear(self):
        """ Remove all items from games view
        """

        self.view.unselect_all()
        self.view.clear()

        self.storage.clear()

    def append_item(self, identifier, data):
        """ Append a new item in games view

        Parameters
        ----------
        identifier : str
            Treeiter identifier
        data : list
            Data structure for specific view
        """

        self.storage[identifier] = self.view.append(data)

        return self.storage.get(identifier)

    def has_item(self, identifier):
        """ Check if a specific identifier exists in main storage

        Parameters
        ----------
        identifier : str
            Item identifier used in main storage

        Returns
        -------
        bool
            True if item exists in main storage, False otherwise
        """

        return identifier in self.storage

    def remove_item(self, identifier):
        """ Remove an item from games view

        Parameters
        ----------
        identifier : str
            Treeiter identifier
        """

        if identifier in self.storage:
            self.view.remove(self.storage.get(identifier))

            del self.storage[identifier]

    def get_treeiter(self, identifier):
        """ Retrieve an item from main storage for a specific identifier

        Parameters
        ----------
        identifier : str
            Item identifier used in main storage

        Returns
        -------
        Gtk.TreeIter
            Item instance is found, None otherwise
        """

        return self.storage.get(identifier, None)


class GeodeGEMViews(GeodeGtkCommon, Gtk.Box):

    __target__ = [
        Gtk.TargetEntry.new("text/uri-list", 0, 1337)
    ]

    class Name(Enum):

        LIST = "list"
        GRID = "grid"

    def __init__(self, interface, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        interface : geode_gem.ui.interface.MainWindow
            Main interface instance
        """

        GeodeGtkCommon.__init__(self, Gtk.Box, **kwargs)

        self.interface = interface
        self.logger = interface.logger

        self.games_identifier_storage = list()

        self.visible_view = None

        # ------------------------------------
        #   Properties
        # ------------------------------------

        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(0)

        # ------------------------------------
        #   Widgets
        # ------------------------------------

        self.view_placeholder = GeodeGEMPlaceholder(self.interface)
        self.view_list = GeodeGEMTreeView(self.interface)
        self.view_grid = GeodeGEMIconView(self.interface)

        # ------------------------------------
        #   Drag and drop
        # ------------------------------------

        self.drag_dest_set(Gtk.DestDefaults.MOTION | Gtk.DestDefaults.DROP,
                           self.__target__,
                           Gdk.DragAction.COPY)

        self.view_list.view.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK,
            self.__target__,
            Gdk.DragAction.COPY)

        self.view_grid.view.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK,
            self.__target__,
            Gdk.DragAction.COPY)

        # ------------------------------------
        #   Signals
        # ------------------------------------

        self.connect(
            "drag-data-received", interface.on_drag_data_to_main_interface)

        # ------------------------------------
        #   Packing
        # ------------------------------------

        self.pack_start(self.view_placeholder, True, True, 0)

        self.pack_start(self.view_list, True, True, 0)
        self.append_widget(self.view_list)

        self.pack_start(self.view_grid, True, True, 0)
        self.append_widget(self.view_grid)

    @property
    def iconview(self):
        """ Retrieve iconview instance

        Returns
        -------
        GeodeGtk.IconView
            Iconview instance
        """

        return self.view_grid.view

    @property
    def placeholder(self):
        """ Retrieve placeholder instance

        Returns
        -------
        GeodeGEM.Placeholder
            Placeholder instance
        """

        return self.view_placeholder

    @property
    def treeview(self):
        """ Retrieve treeview instance

        Returns
        -------
        GeodeGtk.TreeView
            Treeview instance
        """

        return self.view_list.view

    def clear(self):
        """ Clear views and lists storages
        """

        self.games_identifier_storage.clear()

        self.logger.debug("Clear games treeview content")
        self.view_list.clear()

        self.logger.debug("Clear games iconview content")
        self.view_grid.clear()

    def append_games(self, console, games):
        """ Append games in both views

        Parameters
        ----------
        console : geode_gem.engine.console.Console
            Console instance
        games : list
            Games object list
        """

        self.treeview.freeze_child_notify()

        for index, game in enumerate(games, start=1):
            self.append_game(console, game)

            self.treeview.thaw_child_notify()
            yield index, game
            self.treeview.freeze_child_notify()

        self.treeview.thaw_child_notify()

    def append_game(self, console, game):
        """ Append a game to games views

        Parameters
        ----------
        console : geode_gem.engine.console.Console
            Console instance
        game : geode_gem.engine.game.Game
            Game instance
        """

        self.view_grid.append_item(console, game)
        self.view_list.append_item(console, game)

        self.games_identifier_storage.append(game.id)

    def get_selected_game(self):
        """ Retrieve selected game from visible view

        Returns
        -------
        Gtk.TreeIter
            Selected game if found, None otherwise
        """

        treeiter = None

        if self.visible_view == GeodeGEMViews.Name.LIST:
            model = self.treeview.get_model()
            treeiter = self.treeview.get_selected_treeiter()

            if treeiter is not None:
                return model.get_value(treeiter, Columns.List.OBJECT)

        elif self.visible_view == GeodeGEMViews.Name.GRID:
            model = self.iconview.get_model()
            treeiter = self.iconview.get_selected_treeiter()

            if treeiter is not None:
                return model.get_value(treeiter, Columns.Grid.OBJECT)

        return None

    def get_iter_from_key(self, identifier):
        """ Retrieve views iters for a specific game identifier

        Parameters
        ----------
        identifier : str
            Game identifier
        """

        return [getattr(self, f"view_{key}").get_treeiter(identifier)
                for key in ("list", "grid")]

    def has_game(self, identifier):
        """ Check if a specific identifier exists in main storage

        Parameters
        ----------
        identifier : str
            Game identifier used in main storage

        Returns
        -------
        bool
            True if game exists in main storage, False otherwise
        """

        return identifier in self.games_identifier_storage

    def refilter(self):
        """ Refilter games views
        """

        self.treeview.refilter()
        self.iconview.refilter()

    def remove_game(self, identifier):
        """ Remove a game from games views

        Parameters
        ----------
        identifier : str
            Game identifier
        """

        if identifier in self.games_identifier_storage:
            self.games_identifier_storage.remove(identifier)

        self.view_list.remove_item(identifier)
        self.view_grid.remove_item(identifier)

    def set_placeholder_visibility(self, is_visible):
        """ Define placeholder visibility

        Parameters
        ----------
        is_visible : bool
            Placeholder visibility status
        """

        if is_visible:
            self.view_list.hide()
            self.view_grid.hide()
            self.view_placeholder.show_all()

        else:
            self.set_view(self.visible_view)
            self.view_placeholder.hide()

        self.view_placeholder.set_visible(is_visible)

    def set_view(self, identifier, show=True):
        """ Set the games view to show

        Parameters
        ----------
        identifier : str
            View identifier
        show : boolean, optional
            Show the specified view when set as visible_view
        """

        if not isinstance(identifier, GeodeGEMViews.Name):
            raise KeyError(
                f"Cannot found '{identifier}' in GeodeGEMViews.Name")

        for key in GeodeGEMViews.Name:
            widget = getattr(self, f"view_{key.value}")

            widget.set_visible(key is identifier and show)
            if widget.get_visible():
                widget.show_all()

        self.visible_view = identifier

    def unselect_all(self):
        """ Unselect selections from both games views
        """

        self.logger.debug("Unselect games on both views")
        self.iconview.unselect_all()
        self.treeview.unselect_all()


class GeodeGEMTreeView(CommonGamesView):

    def __init__(self, interface, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        interface : geode_gem.ui.interface.MainWindow
            Main interface instance
        """

        CommonGamesView.__init__(
            self,
            interface,
            GeodeGtk.TreeView(
                Gtk.ListStore(
                    str,                # Favorite icon
                    str,                # Multiplayer icon
                    str,                # Finish icon
                    str,                # Name
                    int,                # Played
                    str,                # Last play
                    str,                # Last time play
                    str,                # Time play
                    int,                # Score
                    str,                # Installed
                    str,                # Custom parameters
                    str,                # Screenshots
                    str,                # Save states
                    object,             # Game object
                    GdkPixbuf.Pixbuf    # Thumbnail
                ),
                GeodeGtk.TreeViewColumn(
                    None,
                    GeodeGtk.CellRendererPixbuf(
                        attributes={
                            "icon-name": Columns.List.FAVORITE,
                        },
                        set_padding=(4, 0),
                    ),
                    identifier="favorite",
                    set_resizable=False,
                    set_sizing=Gtk.TreeViewColumnSizing.FIXED,
                    sort_column_id=Columns.List.FAVORITE,
                ),
                GeodeGtk.TreeViewColumn(
                    None,
                    GeodeGtk.CellRendererPixbuf(
                        attributes={
                            "icon-name": Columns.List.MULTIPLAYER,
                        },
                        set_padding=(4, 0),
                    ),
                    identifier="multiplayer",
                    set_resizable=False,
                    set_sizing=Gtk.TreeViewColumnSizing.FIXED,
                    sort_column_id=Columns.List.MULTIPLAYER,
                ),
                GeodeGtk.TreeViewColumn(
                    None,
                    GeodeGtk.CellRendererPixbuf(
                        attributes={
                            "icon-name": Columns.List.FINISH,
                        },
                        set_padding=(4, 0),
                    ),
                    identifier="finish",
                    set_resizable=False,
                    set_sizing=Gtk.TreeViewColumnSizing.FIXED,
                    sort_column_id=Columns.List.FINISH,
                ),
                GeodeGtk.TreeViewColumn(
                    _("Name"),
                    GeodeGtk.CellRendererPixbuf(
                        attributes={
                            "pixbuf": Columns.List.THUMBNAIL,
                        },
                        set_padding=(2, 0),
                    ),
                    GeodeGtk.CellRendererText(
                        attributes={
                            "text": Columns.List.NAME,
                        },
                        properties={
                            "ellipsize": Pango.EllipsizeMode.END
                        },
                        is_expandable=True,
                        set_alignment=(0, 0.5),
                        set_padding=(4, 4),
                    ),
                    identifier="name",
                    set_alignment=0,
                    set_expand=True,
                    set_min_width=100,
                    set_fixed_width=300,
                    sort_column_id=Columns.List.NAME,
                ),
                GeodeGtk.TreeViewColumn(
                    _("Launch"),
                    GeodeGtk.CellRendererText(
                        attributes={
                            "text": Columns.List.PLAYED,
                        },
                        set_padding=(4, 4),
                    ),
                    identifier="play",
                    sort_column_id=Columns.List.PLAYED,
                ),
                GeodeGtk.TreeViewColumn(
                    _("Last launch"),
                    GeodeGtk.CellRendererText(
                        attributes={
                            "text": Columns.List.LAST_PLAY,
                        },
                        set_alignment=(0, .5),
                        set_padding=(4, 0),
                    ),
                    GeodeGtk.CellRendererText(
                        attributes={
                            "text": Columns.List.LAST_TIME_PLAY,
                        },
                        set_alignment=(1, .5),
                        set_padding=(4, 0),
                    ),
                    identifier="last_play",
                    sort_column_id=Columns.List.LAST_PLAY,
                ),
                GeodeGtk.TreeViewColumn(
                    _("Play time"),
                    GeodeGtk.CellRendererText(
                        attributes={
                            "text": Columns.List.TIME_PLAY,
                        },
                        set_padding=(4, 0),
                    ),
                    identifier="play_time",
                    sort_column_id=Columns.List.TIME_PLAY,
                ),
                GeodeGtk.TreeViewColumn(
                    _("Score"),
                    *[
                        GeodeGtk.CellRendererPixbuf(
                            identifier=f"cell_score_{index}",
                            is_expandable=True,
                            set_padding=(2, 0),
                        ) for index in range(1, 6)
                    ],
                    identifier="score",
                    cell_data_func=self.on_update_cells,
                    sort_column_id=Columns.List.SCORE,
                ),
                GeodeGtk.TreeViewColumn(
                    _("Installed"),
                    GeodeGtk.CellRendererText(
                        attributes={
                            "text": Columns.List.INSTALLED,
                        },
                        set_padding=(4, 0),
                    ),
                    identifier="installed",
                    sort_column_id=Columns.List.INSTALLED,
                ),
                GeodeGtk.TreeViewColumn(
                    _("Flags"),
                    GeodeGtk.CellRendererPixbuf(
                        attributes={
                            "icon-name": Columns.List.PARAMETER,
                        },
                        is_expandable=True,
                        set_padding=(2, 0),
                    ),
                    GeodeGtk.CellRendererPixbuf(
                        attributes={
                            "icon-name": Columns.List.SCREENSHOT,
                        },
                        is_expandable=True,
                        set_padding=(2, 0),
                    ),
                    GeodeGtk.CellRendererPixbuf(
                        attributes={
                            "icon-name": Columns.List.SAVESTATE,
                        },
                        is_expandable=True,
                        set_padding=(2, 0),
                    ),
                    identifier="flags",
                ),
                identifier="games",
                filterable=True,
                sorterable=True,
                set_enable_search=False,
                set_has_tooltip=True,
                set_search_column=Columns.List.NAME,
                set_show_expanders=False,
                sort_func=interface.on_sort_games_treeview,
                visible_func=interface.check_game_is_visible,
            ),
            identifier="treeview",
            **kwargs
        )

    def append_item(self, console, game):
        """ See geode_gem.ui.view.CommonGamesView.append_item

        Parameters
        ----------
        console : geode_gem.engine.console.Console
            Console instance
        game : geode_gem.engine.game.Game
            Game instance
        """

        thumbnail = self.interface.get_pixbuf_from_cache(
            "games", 22, game.id, game.cover)
        if not thumbnail or (game.cover and not game.cover.exists()):
            thumbnail = self.interface.icons_games_views.get("treeview")

        row_data = [
            self.interface.get_ui_icon(
                Columns.List.FAVORITE, game.favorite),
            self.interface.get_ui_icon(
                Columns.List.MULTIPLAYER, game.multiplayer),
            self.interface.get_ui_icon(
                Columns.List.FINISH, game.finish),
            game.name,
            game.played,
            (string_from_date(game.last_launch_date)
                if not game.last_launch_date.strftime("%d%m%y") == "010101"
                else None),
            (string_from_time(game.last_launch_time)
                if not game.last_launch_time == timedelta() else None),
            (string_from_time(game.play_time)
                if not game.play_time == timedelta() else None),
            game.score,
            string_from_date(game.installed) if game.installed else None,
            self.interface.get_ui_icon(
                Columns.List.PARAMETER,
                not game.emulator == console.emulator or game.default),
            self.interface.get_ui_icon(
                Columns.List.SCREENSHOT, game.screenshots),
            self.interface.get_ui_icon(
                Columns.List.SAVESTATE, game.savestates),
            game,
            thumbnail,
        ]

        return super().append_item(game.id, row_data)

    def on_update_cells(self, column, cell, model, treeiter, *args):
        """ Manage specific columns behavior during games adding

        Parameters
        ----------
        column : Gtk.TreeViewColumn
            Treeview column which contains cell
        cell : Gtk.CellRenderer
            Cell that is being rendered by column
        model : Gtk.TreeModel
            Rendered model
        treeiter : Gtk.TreeIter
            Rendered row
        """

        if not column.get_visible():
            return

        if cell.identifier.startswith("cell_score"):
            score = model.get_value(treeiter, Columns.List.SCORE)

            for index in range(1, 6):
                widget = self.view.get_widget(f"cell_score_{index}")

                icon_name = self.interface.get_ui_icon(
                    Columns.List.SCORE, score >= index)

                widget.set_sensitive(score >= index)
                widget.set_property("icon-name", icon_name)


class GeodeGEMIconView(CommonGamesView):

    def __init__(self, interface, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        interface : geode_gem.ui.interface.MainWindow
            Main interface instance
        """

        CommonGamesView.__init__(
            self,
            interface,
            GeodeGtk.IconView(
                Gtk.ListStore(
                    GdkPixbuf.Pixbuf,   # Cover icon
                    str,                # Name
                    object              # Game object
                ),
                identifier="games",
                filterable=True,
                sorterable=True,
                set_pixbuf_column=0,
                set_text_column=1,
                set_item_width=96,
                set_spacing=6,
                set_has_tooltip=True,
                sort_func=interface.on_sort_games_iconview,
                visible_func=interface.check_game_is_visible,
            ),
            identifier="iconview",
            **kwargs
        )

    def append_item(self, console, game):
        """ See geode_gem.ui.view.CommonGamesView.append_item

        Parameters
        ----------
        console : geode_gem.engine.console.Console
            Console instance
        game : geode_gem.engine.game.Game
            Game instance
        """

        thumbnail = self.interface.get_pixbuf_from_cache(
            "games", 96, game.id, game.cover)
        if not thumbnail or (game.cover and not game.cover.exists()):
            thumbnail = self.interface.icons_games_views.get("iconview")

        return super().append_item(game.id, [thumbnail, game.name, game])
