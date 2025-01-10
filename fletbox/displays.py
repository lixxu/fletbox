#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft

from . import buttons as fbb
from . import events as fbe
from . import helpers as fbh


def svg_icon(svg: str, **kwargs: Any) -> Any:
    size = kwargs.pop("size", 24)
    kwargs.setdefault("width", size)
    kwargs.setdefault("height", size)
    # kwargs.setdefault("fit", ft.ImageFit.CONTAIN)
    return ft.Image(src=svg, **kwargs)


def markdown(text: str, **kwargs: Any) -> ft.Markdown:
    kwargs.setdefault("expand", True)
    kwargs.setdefault("selectable", False)
    kwargs.setdefault("soft_line_break", True)
    kwargs.setdefault("fit_content", False)
    # kwargs.setdefault("code_theme", ft.MarkdownCodeTheme.SOLARIZED_LIGHT)
    kwargs.setdefault("extension_set", ft.MarkdownExtensionSet.GITHUB_FLAVORED)
    return ft.Markdown(text, **kwargs)


def list_view(expand: bool = True, spacing: int = 0, padding: int = 0, **kwargs) -> ft.ListView:
    return ft.ListView(expand=expand, spacing=spacing, padding=padding, **kwargs)


def text(label: Any = "", **kwargs: Any) -> ft.Text:
    if kwargs.pop("bold", None):
        kwargs.setdefault("weight", ft.FontWeight.BOLD)

    return ft.Text(f"{label}", **kwargs)


def hr(**kwargs: Any) -> ft.Divider:
    return ft.Divider(**kwargs)


def vhr(**kwargs: Any) -> ft.VerticalDivider:
    return ft.VerticalDivider(**kwargs)


def snack(page: ft.Page, text: str, **kwargs: Any) -> None:
    kwargs.setdefault("show_close_icon", True)
    snack_bar = ft.SnackBar(ft.Text(text), **kwargs)
    snack_bar.open = True
    page.overlay.append(snack_bar)


def text_style(size: int = 15, bold: bool = True) -> ft.TextStyle:
    kw = dict(weight=ft.FontWeight.BOLD) if bold else {}
    return ft.TextStyle(size=size, **kw)


def shape(radius: int = 5) -> ft.RoundedRectangleBorder:
    return ft.RoundedRectangleBorder(radius=radius)


def expand_container(content: Any, expand: bool = True, **kwargs: Any) -> ft.Container:
    return ft.Container(expand=expand, content=content, **kwargs)


def expand_row(controls: list, **kwargs: Any) -> ft.Row:
    return pack_row(controls, expand=True, **kwargs)


def pack_row(controls_list: list, expand: bool = False, **kwargs: Any) -> ft.Row:
    controls = []
    total = len(controls_list)
    for i, item in enumerate(controls_list, 1):
        if isinstance(item, tuple):
            wgt, is_expand = item
        else:
            wgt, is_expand = item, i == total

        if is_expand or expand:
            controls.append(expand_container(wgt))
        else:
            controls.append(wgt)

    kwargs.setdefault("vertical_alignment", ft.CrossAxisAlignment.CENTER)
    return ft.Row(controls, **kwargs)


def get_icon(icon: str) -> str:
    return icon.strip().lower()


def get_icon_content(icon: Any, **kwargs: Any) -> ft.Icon:
    if isinstance(icon, str):
        return ft.Icon(getattr(ft.Icons, icon.upper()), **kwargs)

    return icon


def rail(label: str, icon: str = "", selected_icon: str = "", **kwargs: Any) -> ft.NavigationRailDestination:
    kw = dict(label=label)
    if icon:
        kw.update(icon=get_icon(icon))

    if selected_icon:
        kw.update(selected_icon=get_icon(selected_icon))

    return ft.NavigationRailDestination(**(kwargs | kw))


def markdown_code_theme(page: ft.Page, dark_name: str = "", light_name: str = "") -> Any:
    if fbh.is_dark_mode(page):
        name = dark_name.upper() or "SOLARIZED_DARK"
    else:
        name = light_name.upper() or "SOLARIZED_LIGHT"

    return getattr(ft.MarkdownCodeTheme, name)


class TitleBar(ft.Row):
    def __init__(self, title: str, icon: str = "", **kwargs: Any) -> None:
        super().__init__()
        self.expand = True
        self._title = title
        self._icon = icon
        self.tight = True
        self.text_color = kwargs.get("text_color", "indigo")

    def refresh_maximize(self) -> None:
        fbe.on_tap_max(self.page, wgt=self.max_wgt)

    def click_top(self, e: Any):
        fbe.on_tap_top(self.page, e)

    def click_min(self, e: Any):
        fbe.on_tap_min(self.page)

    def click_max(self, e: Any):
        fbe.on_tap_max(self.page, e)

    def click_close(self, e: Any) -> None:
        fbe.on_tap_close(self.page)

    def build(self) -> ft.Row:
        def on_resized(e: Any) -> Any:
            self.refresh_maximize()

        controls = []
        self.page.on_resized = on_resized
        if self._icon:
            controls.append(ft.Container(svg_icon(self._icon, size=20), margin=ft.margin.only(left=5)))

        title = ft.Text(
            self._title, color=self.text_color, theme_style=ft.TextThemeStyle.TITLE_SMALL, expand=True
        )
        controls.append(title)
        top_wgt = fbb.IconButton("push_pin_outlined", self.click_top, "窗口置顶", "push_pin")
        min_wgt = fbb.IconButton("remove", self.click_min, "最小化")
        self.max_wgt = fbb.IconButton("check_box_outline_blank", self.click_max, "最大化", "filter_none")
        close_wgt = fbb.IconButton("close", self.click_close, "退出")
        self.controls = controls + [top_wgt, min_wgt, self.max_wgt, close_wgt]


class TitleArea(ft.Container):
    def __init__(self, title: str, icon: str) -> None:
        super().__init__()
        self.padding = 0
        self.margin = 0
        self.expand = True
        self._title = title
        self._icon = icon

    def build(self) -> None:
        self.content = TitleBar(self._title, self._icon)


class ViewHelper(ft.Container):
    def __init__(self, title: str = "", icon: str = "", controls: list = [], **kwargs: Any) -> None:
        super().__init__()
        self.expand = False
        self._title = title
        self._icon = icon
        self.kwargs = kwargs
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.other_controls = controls

    def get_drag_area(self) -> ft.WindowDragArea:
        drag = ft.Column([TitleArea(self._title, self._icon), hr()])
        return ft.WindowDragArea(drag)

    def build_tabs(self) -> None:
        area = self.get_drag_area()
        st = ft.Stack(self.other_controls + [area], expand=True)
        self.content = st

    def build(self) -> None:
        controls = []
        if self.kwargs.get("title_bar_hidden", True):
            area = self.get_drag_area()
            controls.extend([area])

        c = ft.Column(controls + self.other_controls, expand=False)
        self.content = c


def top_bar(title: str = "", **kwargs: Any) -> tuple:
    bg = kwargs.get("bg")
    kw = dict(bgcolor=bg) if bg else {}
    height = kwargs.get("height", 46)
    title_kw = kwargs.get("title_kw", {})
    title_kw.setdefault("weight", ft.FontWeight.BOLD)
    bar_title = ft.Text(title, **title_kw)
    drag = ft.WindowDragArea(ft.Row([bar_title], vertical_alignment="center"))
    bar = expand_container(drag, height=height, padding=ft.padding.only(left=10), **kw)
    return bar_title, bar


def column(controls: list = [], **kwargs: Any) -> ft.Column:
    kwargs.setdefault("expand", True)
    # kwargs.setdefault("scroll", "auto")
    return ft.Column(controls, **kwargs)


# short names
icon = get_icon
textstyle = text_style
