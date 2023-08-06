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
from geode_gem.ui.data import Icons
from geode_gem.widgets.common import GeodeGtkCommon
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import Gtk

# Translation
from gettext import gettext as _


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class GeodeGEMPlaceholder(GeodeGtkCommon, Gtk.ScrolledWindow):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.ScrolledWindow, **kwargs)

        self.inner_grid = GeodeGtk.Box(
            GeodeGtk.Image(
                is_expandable=True,
                is_fillable=True,
                set_from_icon_name=(Icons.Symbolic.GAMING,
                                    Gtk.IconSize.DIALOG),
                set_halign=Gtk.Align.CENTER,
                set_pixel_size=256,
                set_valign=Gtk.Align.END,
                set_style=Gtk.STYLE_CLASS_DIM_LABEL,
            ),
            GeodeGtk.Label(
                is_expandable=True,
                is_fillable=True,
                set_halign=Gtk.Align.CENTER,
                set_valign=Gtk.Align.START,
                set_text=_("Start to play by drag & drop some files into "
                           "interface"),
            ),
            set_border_width=18,
            set_orientation=Gtk.Orientation.VERTICAL,
            set_spacing=12,
        )

        # Packing
        self.add(self.inner_grid)
