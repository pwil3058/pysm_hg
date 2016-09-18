### Copyright (C) 2016 Peter Williams <pwil3058@gmail.com>
###
### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; version 2 of the License only.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import os
import sys
import collections

from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GdkPixbuf

PACKAGE_NAME = "aipoed"

def find_app_icon_directory(app_name):
    # find the icons directory
    # first look in the source directory (so that we can run uninstalled)
    icon_dir_path = os.path.join(sys.path[0], "pixmaps")
    if not os.path.exists(icon_dir_path) or not os.path.isdir(icon_dir_path):
        _TAILEND = os.path.join("share", "pixmaps", app_name)
        _prefix = sys.path[0]
        while _prefix:
            icon_dir_path = os.path.join(_prefix, _TAILEND)
            if os.path.exists(icon_dir_path) and os.path.isdir(icon_dir_path):
                break
            _prefix = os.path.dirname(_prefix)
    return icon_dir_path

def find_pkg_icon_directory(pkg_name):
    # find the icons directory
    # first look in the source directory (so that we can run uninstalled)
    for path in sys.path:
        _prefix = path
        if os.path.isdir(os.path.join(path, pkg_name)):
            icon_dir_path = os.path.join(path, "pixmaps")
            if os.path.isdir(icon_dir_path):
                return icon_dir_path
            break
    _TAILEND = os.path.join("share", "pixmaps", pkg_name)
    while _prefix:
        icon_dir_path = os.path.join(_prefix, _TAILEND)
        if os.path.exists(icon_dir_path) and os.path.isdir(icon_dir_path):
            break
        _prefix = os.path.dirname(_prefix)
    return icon_dir_path

_PREFIX = PACKAGE_NAME + "_"

STOCK_FILE_REFRESHED = _PREFIX + "stock_file_refreshed"
STOCK_FILE_NEEDS_REFRESH = _PREFIX + "stock_file_needs_refresh"
STOCK_FILE_UNREFRESHABLE = _PREFIX + "stock_file_unrefreshable"
STOCK_FILE_PROBLEM = STOCK_FILE_UNREFRESHABLE
STOCK_REFRESH_PATCH = _PREFIX + "stock_refresh_patch"

_STOCK_ITEMS_OWN_PNG = [
    (STOCK_FILE_REFRESHED, _("Refreshed"), 0, 0, None),
    (STOCK_FILE_NEEDS_REFRESH, _("Needs Refresh"), 0, 0, None),
    (STOCK_FILE_UNREFRESHABLE, _("Unrefreshable"), 0, 0, None),
    (STOCK_REFRESH_PATCH, _("Refresh"), 0, 0, None),
]

def add_own_stock_icons(name, stock_item_list, find_icon_directory=find_app_icon_directory):
    LIBDIR = find_icon_directory(name)
    OFFSET = len(name) + 1
    png_file_name = lambda item_name: os.path.join(LIBDIR, item_name[OFFSET:] + os.extsep + "png")
    def make_pixbuf(name):
        return GdkPixbuf.Pixbuf.new_from_file(png_file_name(name))
    factory = Gtk.IconFactory()
    factory.add_default()
    for _item in stock_item_list:
        _name = _item[0]
        factory.add(_name, Gtk.IconSet(make_pixbuf(_name)))

add_own_stock_icons(PACKAGE_NAME, _STOCK_ITEMS_OWN_PNG, find_pkg_icon_directory)

StockAlias = collections.namedtuple("StockAlias", ["name", "alias", "text"])

def add_stock_aliases(stock_alias_list):
    factory = Gtk.IconFactory()
    factory.add_default()
    def make_pixbuf(alias):
        return Gtk.Image.new_from_stock(alias, Gtk.IconSize.MENU).get_pixbuf()
    for item in stock_alias_list:
        factory.add(item.name, Gtk.IconSet(make_pixbuf(item.alias)))

# Icons that are aliased to Gtk or other stock items
STOCK_RENAME = _PREFIX + "stock_rename"
STOCK_INSERT = _PREFIX + "_stock_insert"

# Icons that have to be designed eventually (using GtK stock in the meantime)
_STOCK_ALIAS_LIST = [
    StockAlias(name=STOCK_RENAME, alias=Gtk.STOCK_PASTE, text=""),
    StockAlias(name=STOCK_INSERT, alias=Gtk.STOCK_ADD, text=_("Insert")),
]

add_stock_aliases(_STOCK_ALIAS_LIST)
