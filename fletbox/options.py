#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft

from . import dialogs as fbd
from . import helpers as fbh


def setup_alignment(page: ft.Page, w: str = "", v: str = "center", h: str = "center") -> None:
    if w:
        # if set window alignment, saved positions will not work
        page.window.alignment = getattr(ft.alignment, w.lower())

    page.vertical_alignment = getattr(ft.MainAxisAlignment, v.upper())
    page.horizontal_alignment = getattr(ft.CrossAxisAlignment, h.upper())


def setup_fonts(page: ft.Page) -> None:
    page.fonts = {"AlibabaPuHuiTi": "/fonts/AlibabaPuHuiTi-3-55-Regular.ttf"}


def setup_options(page: ft.Page, icon: str = "/logo.ico", align_kw: dict = {}, **kwargs: Any) -> None:
    if min_w := kwargs.get("min_width"):
        page.window.min_width = min_w

    if min_h := kwargs.get("min_height"):
        page.window.min_height = min_h

    if scroll := kwargs.get("scroll"):
        page.scroll = scroll

    if icon:
        page.window.icon = icon

    if theme := kwargs.get("theme_mode", "system"):
        page.theme_mode = getattr(ft.ThemeMode, theme.upper())

    if kwargs.get("title_bar_hidden", True):
        page.window.title_bar_hidden = True

    if kwargs.get("title_bar_buttons_hidden", True):
        page.window.title_bar_buttons_hidden = True

    setup_alignment(page, **align_kw)
    setup_fonts(page)
    theme_kw = {}
    if font := kwargs.get("font", "AlibabaPuHuiTi"):
        theme_kw.update(font_family=font)

    if theme_color := kwargs.get("them_color"):
        theme_kw.update(color_scheme_seed=theme_color)

    page.theme = ft.Theme(**theme_kw)
    page.on_error = lambda e: print("Page error:", e.data)


def page_teardown(teardowns: list) -> None:
    for t in teardowns:
        args = ()
        kargs = {}
        if isinstance(t, tuple):
            # (func, args, {})
            if len(t) == 3:
                func, args, kargs = t
            elif len(t) == 2:
                func, args = t
            else:
                func = t[0]

        else:
            func = t

        try:
            func(*args, **kargs)
        except Exception:
            pass


def setup_events(page: ft.Page, **kwargs: Any) -> None:
    def really_quit(dlg: Any = None):
        if dlg:
            page.close(dlg)

        page_teardown(getattr(page, "teardowns", []))
        page.window.visible = False
        page.window.prevent_close = False
        page.window.close()
        # destroy() takes too long time, disable it until bug fixed
        # page.window.destroy()

    def do_quit() -> None:
        if getattr(page, "quit_confirm", None):
            page.open(confirm_dialog)
        else:
            really_quit()

    def window_event(e):
        if e.data == "close":
            if hasattr(page, "can_quit"):
                if page.can_quit:
                    do_quit()
                else:
                    page.open(running_dialog)

            else:
                do_quit()

    page.window.prevent_close = True
    page.window.on_event = window_event

    def clicked(e: Any) -> None:
        data = e.control.data
        page.close(dlgs[data])
        if data == "yes":
            really_quit()

    yes_btn = fbh.get_button(kwargs.get("yes_label", "退出"), clicked, data="yes")
    no_btn = fbh.get_button(kwargs.get("no_label", "取消"), clicked, data="no")
    ok_btn = fbh.get_button(kwargs.get("ok_label", "确定"), clicked, data="running")

    confirm_kw = kwargs.get("confirm_kw", {})
    confirm_kw.setdefault("icon", "warning")
    confirm_kw.setdefault("title_kw", dict(color="red"))
    confirm_kw.setdefault("icon_kw", dict(color="red", size=36))
    confirm_dialog = fbd.get_confirm_dialog(
        [yes_btn, no_btn], title=kwargs.get("confirm_title", "确定要退出吗?"), **confirm_kw
    )
    running_dialog = fbd.get_confirm_dialog(
        [ok_btn], title=kwargs.get("running_notice", "有正在运行的任务, 无法退出!"), **confirm_kw
    )
    dlgs = dict(yes=confirm_dialog, no=confirm_dialog, running=running_dialog)
