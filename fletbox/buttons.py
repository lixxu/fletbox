#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft

from . import displays as fbdp
from . import events as fbe


def button(text: str, func: Any, style_kw: dict = {}, **kwargs: Any) -> ft.OutlinedButton:
    style_kw.setdefault("shape", fbdp.shape(2))
    kwargs.setdefault("style", ft.ButtonStyle(**style_kw))
    return ft.OutlinedButton(text, on_click=func, **kwargs)


def top_button(text: str, data: str = "", func: Any = None, **kwargs: Any) -> ft.ElevatedButton:
    style = ft.ButtonStyle(shape=fbdp.shape(), padding=5, text_style=fbdp.text_style())
    kwargs.setdefault("style", style)
    return ft.ElevatedButton(text=text, data=data, on_click=func, **kwargs)


def segmented(segments: list = [], **kwargs: Any) -> ft.SegmentedButton:
    selected_icon = kwargs.get("selected_icon", "check")
    kwargs.update(selected_icon=fbdp.get_icon_content(selected_icon))
    kwargs.setdefault("allow_multiple_selection", True)
    kwargs.setdefault("on_change", lambda e: print(e))
    selected = kwargs.get("selected") or []
    kwargs.update(selected=set(selected))
    style = ft.ButtonStyle(shape=fbdp.shape(), padding=5)
    kwargs.setdefault("style", style)
    return ft.SegmentedButton(segments=prepare_segments(segments), **kwargs)


def prepare_segments(segments: list = []) -> list:
    segs = []
    for seg in segments:
        if isinstance(seg, str):
            segs.append(get_segment(seg))
        else:
            if len(seg) == 2:
                segs.append(get_segment(*seg))
            else:
                segs.append(get_segment(seg[0], seg[1], **seg[2]))

    return segs


def get_segment(value: str, label: str = "", **kwargs: Any) -> ft.Segment:
    if icon_name := kwargs.get("icon"):
        if isinstance(icon_name, str):
            icon = fbdp.get_icon_content(icon_name)
            kwargs.update(icon=icon)

    if not label:
        label = str(value)

    if isinstance(label, str):
        label = ft.Text(label)

    return ft.Segment(value=value, label=label, **kwargs)


def ok(**kwargs: Any) -> Any:
    kwargs.setdefault("autofocus", True)
    return button(
        kwargs.pop("label", "确定"), kwargs.pop("func", None), icon=kwargs.pop("icon", "check"), **kwargs
    )


def save(**kwargs: Any) -> Any:
    return button(
        kwargs.pop("label", "保存"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "save"),
        icon=kwargs.pop("icon", "save"),
        **kwargs,
    )


def cancel(**kwargs: Any) -> Any:
    return button(
        kwargs.pop("label", "取消"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "cancel"),
        icon=kwargs.pop("icon", "close"),
        **kwargs,
    )


def yes(**kwargs: Any) -> Any:
    return button(
        kwargs.pop("label", "是"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "yes"),
        icon=kwargs.pop("icon", "check"),
        **kwargs,
    )


def no(**kwargs: Any) -> Any:
    return button(
        kwargs.pop("label", "否"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "no"),
        icon=kwargs.pop("icon", "close"),
        **kwargs,
    )


def add(**kwargs: Any) -> Any:
    return button(
        kwargs.pop("label", "添加"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "add"),
        icon=kwargs.pop("icon", "add"),
        **kwargs,
    )


def edit(**kwargs: Any) -> Any:
    return button(
        kwargs.pop("label", "修改"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "edit"),
        icon=kwargs.pop("icon", "mode_edit_outlined"),
        **kwargs,
    )


def delete(**kwargs: Any) -> Any:
    return top_button(
        kwargs.pop("label", "删除"),
        data=kwargs.pop("data", "delete"),
        func=kwargs.pop("func", None),
        icon=kwargs.pop("icon", "delete"),
        color=kwargs.pop("color", "red"),
        **kwargs,
    )


def browse(**kwargs: Any) -> Any:
    return button(
        kwargs.pop("label", "浏览..."),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "browse"),
        icon=kwargs.pop("icon", ""),
        **kwargs,
    )


class IconButton(ft.IconButton):
    def __init__(
        self, icon: str, func: Any, tooltip: str = "", selected_icon: str = "", **kwargs: Any
    ) -> None:
        super().__init__()
        self.on_click = func
        self.tooltip = tooltip
        self.icon = fbdp.icon(icon)
        self.selected_icon = fbdp.icon(selected_icon)
        self.style = ft.ButtonStyle(shape=fbdp.shape(0))
        [setattr(self, k, v) for k, v in kwargs.items()]


def icon_pack(wgt: IconButton, **kwargs: Any) -> ft.Container:
    return ft.Container(wgt, **kwargs)


def top_icon_buttons(page: ft.Page, **kwargs: Any) -> dict:
    icons = {}
    kwargs.setdefault("width", 44)
    kwargs.setdefault("height", 46)
    ignores = kwargs.pop("ignores", [])
    mode_callback = kwargs.pop("mode_callback", None)
    if "mode" not in ignores:
        icons.update(
            mode=IconButton("dark_mode_outlined", mode_callback, "进入深色模式", "light_mode_outlined")
        )
        icons.update(mode_pack=icon_pack(icons["mode"], **kwargs))

    if "top" not in ignores:
        icons.update(
            top=IconButton("push_pin_outlined", lambda e: fbe.on_tap_top(page, e), "窗口置顶", "push_pin")
        )
        icons.update(top_pack=icon_pack(icons["top"], **kwargs))

    if "min" not in ignores:
        icons.update(min=IconButton("remove", lambda _: fbe.on_tap_min(page), "最小化"))
        icons.update(min_pack=icon_pack(icons["min"], **kwargs))

    if "max" not in ignores:
        wgt = IconButton(
            "check_box_outline_blank", lambda e: fbe.on_tap_max(page, e), "最大化", "filter_none"
        )
        icons.update(max=wgt)
        icons.update(max_pack=icon_pack(icons["max"], **kwargs))

    if "close" not in ignores:
        icons.update(close=IconButton("close", lambda _: fbe.on_tap_close(page), "关闭", hover_color="red"))
        icons.update(close_pack=icon_pack(icons["close"], **kwargs))

    return icons


segment = get_segment
