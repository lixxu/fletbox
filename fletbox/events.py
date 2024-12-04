#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft

from . import helpers as fbh


def on_tap_mode(page: ft.Page, e: Any = None, refresh: bool = True, wgt: Any = None) -> None:
    if e:
        control = e.control
        e.control.selected = not e.control.selected
        if e.control.selected:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT

    else:
        control = wgt
        control.selected = fbh.is_dark_mode(page)

    tooltip = "退出深色模式" if fbh.is_dark_mode(page) else "进入深色模式"
    control.tooltip = tooltip
    if refresh:
        page.update()


def on_tap_top(page: ft.Page, e: Any) -> None:
    e.control.selected = not e.control.selected
    page.window.always_on_top = not page.window.always_on_top
    tooltip = "取消窗口置顶" if page.window.always_on_top else "窗口置顶"
    e.control.tooltip = tooltip
    page.update()


def on_tap_min(page: ft.Page) -> None:
    page.window.minimized = True
    page.update()


def on_tap_max(page: ft.Page, e: Any = None, wgt: Any = None) -> None:
    if e:
        page.window.maximized = not page.window.maximized

    control = e.control if e else wgt
    control.selected = page.window.maximized

    tooltip = "恢复窗口" if page.window.maximized else "最大化"
    control.tooltip = tooltip
    page.update()


def on_tap_close(page: ft.Page) -> None:
    page.visible = False
    page.window.close()
