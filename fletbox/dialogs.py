#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft


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
            kw.update(content=ft.Text(content))
        else:
            kw.update(content=content)

    align = kwargs.get("align", ft.MainAxisAlignment.END)
    if icon:
        kw.update(icon=ft.Icon(getattr(ft.icons, icon.upper()), **icon_kw))

    return ft.AlertDialog(
        modal=kwargs.get("modal", True),
        title=ft.Text(title, **title_kw),
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
