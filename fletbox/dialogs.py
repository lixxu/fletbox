#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft

from . import buttons as fbb


def get_dialog(
    title: str,
    content: Any = "",
    icon: str = "",
    buttons: list = [],
    title_kw: dict = {},
    icon_kw: dict = {},
    **kwargs: Any,
) -> ft.AlertDialog:
    kw = {}
    if content:
        if isinstance(content, str):
            kw.update(content=ft.SelectionArea(ft.Text(content)))
        else:
            kw.update(content=ft.SelectionArea(content))

    align = kwargs.get("align", ft.MainAxisAlignment.END)
    if icon:
        kw.update(icon=ft.Icon(getattr(ft.icons, icon.upper()), **icon_kw))

    return ft.AlertDialog(
        modal=kwargs.get("modal", True),
        title=ft.WindowDragArea(ft.Container(ft.Text(title, **title_kw), expand=True)),
        actions_alignment=align,
        shape=ft.RoundedRectangleBorder(radius=2.0),
        actions=buttons,
        **kw,
    )


def get_confirm_dialog(buttons: list = [], **kwargs: Any) -> ft.AlertDialog:
    title = kwargs.pop("title", "确定要退出吗?")
    kwargs.setdefault("icon", "warning")
    kwargs.setdefault("title_kw", dict(color="red"))
    kwargs.setdefault("icon_kw", dict(color="red", size=36))
    kwargs.update(buttons=buttons)
    return get_dialog(title, **kwargs)


def warning(title: str, page: ft.Page, **kwargs: Any) -> None:
    if not (buttons := kwargs.get("buttons")):

        def clicked(e: Any) -> None:
            page.close(dlg)
            if extra_func := kwargs.get("extra_func"):
                extra_func(e)

        buttons = [fbb.ok(func=clicked)]

    kwargs.setdefault("icon", "warning")
    kwargs.setdefault("title_kw", dict(color="red"))
    kwargs.setdefault("icon_kw", dict(color="red", size=36))
    kwargs.update(buttons=buttons)
    dlg = get_dialog(title, **kwargs)
    page.open(dlg)
    page.update()
    return dlg


def confirm(title: str, page: ft.Page, **kwargs: Any) -> None:
    if not (buttons := kwargs.get("buttons")):

        def clicked(e: Any) -> None:
            page.close(dlg)
            if extra_func := kwargs.get("extra_func"):
                extra_func(e)

        buttons = [fbb.yes(func=clicked), fbb.no(func=clicked)]

    kwargs.setdefault("icon", "question")
    # kwargs.setdefault("title_kw", dict(color="red"))
    # kwargs.setdefault("icon_kw", dict(color="red", size=36))
    kwargs.update(buttons=buttons)
    dlg = get_dialog(title, **kwargs)
    page.open(dlg)
    page.update()
    return dlg


def banner(content: Any, **kwargs: Any) -> ft.Banner:
    if isinstance(content, str):
        content = ft.Text(content)

    return ft.Banner(content=content, **kwargs)
