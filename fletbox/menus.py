#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft

from . import helpers as fbh


def menu_bar(**kwargs: Any) -> ft.MenuBar:
    kwargs.setdefault("expand", True)
    return ft.MenuBar(**kwargs)


def submenu(**kwargs: Any) -> ft.SubmenuButton:
    pass


def menu_item(content: Any, **kwargs: Any) -> ft.MenuItemButton:
    return ft.MenuItemButton(content=content, **kwargs)
