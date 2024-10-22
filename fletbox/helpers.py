#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import flet as ft
from flet.security import decrypt, encrypt


def clear_splash() -> None:
    try:
        import pyi_splash

        pyi_splash.close()
    except Exception:
        pass


def encrypt_text(text: str, secret_key: str) -> str:
    return encrypt(text, secret_key)


def decrypt_text(hashed_text: str, secret_key: str) -> str:
    try:
        return decrypt(hashed_text, secret_key)
    except Exception:
        return hashed_text


def save_window(page: ft.Page) -> dict:
    settings = {}
    top = page.window.top
    left = page.window.left
    width = page.window.width
    height = page.window.height
    if height and width:
        is_max = page.window.maximized
        settings.update(is_max=is_max)
        if not is_max:
            settings.update(win_top=top, win_left=left, win_height=height, win_width=width)

    return settings


def restore_window(page: ft.Page, settings: Any) -> None:
    top = settings.get("win_top")
    left = settings.get("win_left")
    width = settings.get("win_width")
    height = settings.get("win_height")
    is_max = settings.get("is_max")
    if width and height:
        page.window.width = float(width)
        page.window.height = float(height)
        try:
            page.window.top = float(top)  # type: ignore
            page.window.left = float(left)  # type: ignore
        except Exception:
            pass

    if is_max:
        page.window.maximized = True

    page.update()


def save_window_ui(page: ft.Page, key: str = "win_pos") -> None:
    helper = BaseStorage(page)
    helper.set_key(save_window(page), key)


def load_window_ui(page: ft.Page, key: str = "win_pos") -> dict:
    helper = BaseStorage(page)
    return helper.get_key(key) or {}


def is_dist() -> bool:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return True

    return False


def remember_control(page: ft.Page, name: str, control: Any) -> None:
    if hasattr(page, "wgts"):
        page.wgts[name] = control


def get_assets_dir(current_dir: str = ".") -> str:
    for fp in Path(current_dir).iterdir():
        if fp.is_dir():
            if fp.name == "assets":
                return fp.name

            for ffp in fp.iterdir():
                if ffp.is_dir() and ffp.name == "assets":
                    return str(ffp).replace("\\", "/")

    return "assets"


def get_text_field(label: str, value: Any = "", **kwargs: Any) -> ft.TextField:
    return ft.TextField(label=label, value=value, **kwargs)


def get_list_view(expand: bool = True, spacing: int = 0, padding: int = 0, **kwargs) -> ft.ListView:
    return ft.ListView(expand=expand, spacing=spacing, padding=padding, **kwargs)


def get_button(text: str, func: Any, style_kw: dict = {}, **kwargs: Any) -> ft.OutlinedButton:
    style_kw.setdefault("shape", ft.RoundedRectangleBorder(radius=2))
    return ft.OutlinedButton(text, on_click=func, style=ft.ButtonStyle(**style_kw), **kwargs)


def get_markdown(text: str, **kwargs: Any) -> ft.Markdown:
    kwargs.setdefault("expand", True)
    kwargs.setdefault("selectable", False)
    kwargs.setdefault("soft_line_break", True)
    kwargs.setdefault("extension_set", ft.MarkdownExtensionSet.GITHUB_WEB)
    return ft.Markdown(text, **kwargs)


def get_column(controls: list = [], **kwargs: Any) -> ft.Column:
    kwargs.setdefault("expand", True)
    kwargs.setdefault("scroll", "auto")
    return ft.Column(controls, **kwargs)


def get_btn_shape(radius: int = 5) -> ft.RoundedRectangleBorder:
    return ft.RoundedRectangleBorder(radius=radius)


def get_text_style(size: int = 15, bold: bool = True) -> ft.TextStyle:
    kw = dict(weight=ft.FontWeight.BOLD) if bold else {}
    return ft.TextStyle(size=size, **kw)


def get_expand_container(content: Any, expand: bool = True, **kwargs: Any) -> ft.Container:
    return ft.Container(expand=expand, content=content, **kwargs)


def get_expand_row(controls: list, **kwargs: Any) -> ft.Row:
    return pack_row(controls, expand=True, **kwargs)


def get_icon(icon: str) -> str:
    return icon.lower()


def show_snack(page: ft.Page, text: str, **kwargs: Any) -> None:
    page.snack_bar = ft.SnackBar(ft.Text(text), **kwargs)
    page.snack_bar.open = True


def get_rail(
    label: str, icon: str = "", selected_icon: str = "", **kwargs: Any
) -> ft.NavigationRailDestination:
    kw = dict(label=label)
    if icon:
        kw.update(icon=get_icon(icon))

    if selected_icon:
        kw.update(selected_icon=get_icon(selected_icon))

    return ft.NavigationRailDestination(**(kwargs | kw))


def create_top_button(text: str, data: str, func: Any, **kwargs: Any) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=text,
        data=data,
        on_click=func,
        style=ft.ButtonStyle(shape=get_btn_shape(), padding=5, text_style=get_text_style()),
        **kwargs,
    )


def pack_row(controls_list: list, expand: bool = False, **kwargs: Any) -> ft.Row:
    controls = []
    total = len(controls_list)
    for i, item in enumerate(controls_list, 1):
        if isinstance(item, tuple):
            wgt, is_expand = item
        else:
            wgt, is_expand = item, i == total

        if is_expand or expand:
            controls.append(get_expand_container(wgt))
        else:
            controls.append(wgt)

    return ft.Row(controls, **kwargs)


class IconButton(ft.IconButton):
    def __init__(self, icon: str, func: Any, tooltip: str = "", selected_icon: str = "") -> None:
        super().__init__()
        self.on_click = func
        self.tooltip = tooltip
        self.icon = get_icon(icon)
        self.selected_icon = get_icon(selected_icon)
        self.style = ft.ButtonStyle(shape=get_btn_shape(radius=0))


class TitleArea(ft.Container):
    def __init__(self, title: str, icon: str) -> None:
        super().__init__()
        # self.height = 20
        # self.bgcolor = "indigo300"
        self.padding = 0
        self.margin = 0
        self.expand = True
        self._title = title
        self._icon = icon

    def build(self) -> None:
        self.content = TitleBar(self._title, self._icon)


class TitleBar(ft.Row):
    def __init__(self, title: str, icon: str = "", **kwargs: Any) -> None:
        super().__init__()
        self.expand = True
        self._title = title
        self._icon = icon
        self.tight = True
        self.text_color = kwargs.get("text_color", "indigo")

    def refresh_maximize(self) -> None:
        tooltip = "恢复窗口" if self.page.window.maximized else "最大化"
        self.max_wgt.tooltip = tooltip
        self.page.update()

    def click_top(self, e: Any):
        e.control.selected = not e.control.selected
        self.page.window.always_on_top = not self.page.window.always_on_top
        tooltip = "取消置于顶层" if self.page.window.always_on_top else "置于顶层"
        e.control.tooltip = tooltip
        self.page.update()

    def click_min(self, e: Any):
        self.page.window.minimized = True
        self.page.update()

    def click_max(self, e: Any):
        e.control.selected = not e.control.selected
        self.page.window.maximized = not self.page.window.maximized
        self.refresh_maximize()

    def click_close(self, e: Any) -> None:
        self.page.visible = False
        self.page.window.close()

    def build(self) -> ft.Row:
        def on_resize(e: Any) -> Any:
            self.refresh_maximize()

        controls = []
        self.page.on_resize = on_resize
        if self._icon:
            controls.append(ft.Image(src=self._icon, width=20, height=20, fit=ft.ImageFit.CONTAIN))

        title = ft.Text(
            self._title, color=self.text_color, theme_style=ft.TextThemeStyle.TITLE_SMALL, expand=True
        )
        controls.append(title)
        top_wgt = IconButton("push_pin_outlined", self.click_top, "置于顶层", "push_pin")
        min_wgt = IconButton("remove", self.click_min, "最小化")
        self.max_wgt = IconButton("check_box_outline_blank", self.click_max, "最大化", "filter_none")
        close_wgt = IconButton("close", self.click_close, "退出")
        self.controls = controls + [top_wgt, min_wgt, self.max_wgt, close_wgt]


class ViewHelper(ft.Container):
    def __init__(self, title: str = "", icon: str = "", controls: list = [], **kwargs: Any) -> None:
        super().__init__()
        self.expand = False
        self._title = title
        self._icon = icon
        self.kwargs = kwargs
        self.other_controls = controls

    def get_drag_area(self) -> ft.WindowDragArea:
        drag = ft.Row([TitleArea(self._title, self._icon)])
        return ft.WindowDragArea(drag)

    def build_tabs(self) -> None:
        area = self.get_drag_area()
        st = ft.Stack(self.other_controls + [area], expand=True)
        self.content = st

    def build(self) -> None:
        controls = []
        if self.kwargs.get("title_bar_hidden", True):
            area = self.get_drag_area()
            controls.extend([area, ft.Divider()])

        c = ft.Column(controls + self.other_controls, spacing=0, expand=False)
        self.content = c


class StorageHelper:
    __secret_key__ = ""
    __app_name__ = "flet"
    __app_org__ = "flet-dev"
    __app_client_key__ = "flet-dev-client"

    @property
    def app_client_key(self) -> str:
        return self.__app_client_key__

    @property
    def app_name(self) -> str:
        return self.__app_name__

    @property
    def app_org(self) -> str:
        return self.__app_org__

    @property
    def secret_key(self) -> str:
        return self.__secret_key__

    def init_page(self, page: ft.Page) -> None:
        self.page = page
        self.__app_org__ = page.__app_org__
        self.__app_name__ = page.__app_name__
        self.__app_client_key__ = page.__app_client_key__
        self.__secret_key__ = page.__secret_key__

    def get_client_key(self, key: str = "") -> str:
        return f"{self.app_org}.{self.app_name}.{key or self.app_client_key}"

    def set_key(self, val: Any, key: str = "") -> None:
        self.page.client_storage.set(self.get_client_key(key), val)

    def get_key(self, key: str = "") -> Any:
        return self.page.client_storage.get(self.get_client_key(key))

    def encrypt(self, text: str) -> str:
        return encrypt_text(text, self.secret_key)

    def decrypt(self, text: str) -> str:
        return decrypt_text(text, self.secret_key)


class BaseStorage(StorageHelper):
    def __init__(self, page: ft.Page) -> None:
        self.init_page(page)


class EchoHelper:
    page = None
    kept_line = ""
    last_wgt = None
    kept_wgt = None
    kept_style = {}

    def __init__(self, page: ft.Page) -> None:
        self.page = page

    def clear_controls(self) -> None:
        self.last_wgt = None
        self.kept_wgt = None
        self.page.lv.controls.clear()

    def append_lv_text(self, text: Any, **kwargs: Any) -> ft.Text:
        wgt = ft.Text(f"{text}", **kwargs)
        self.page.lv.controls.append(wgt)
        return wgt

    def echo(self, text: Any, **kwargs: Any) -> None:
        if kwargs.pop("ts", False):
            text = f"[{datetime.now()}] {text}"
        else:
            text = f"{text}"

        if kwargs.pop("bold", False):
            kwargs.setdefault("weight", "bold")

        if fg := kwargs.pop("fg", None):
            kwargs.setdefault("color", fg)

        if bg := kwargs.pop("bg", None):
            kwargs.setdefault("bgcolor", bg)

        # if update last control for append to last
        remeber = kwargs.pop("remeber", None)
        append_to_last = kwargs.pop("append_to_last", None)
        if not append_to_last:
            self.last_wgt = self.append_lv_text(text, **kwargs)
        else:
            lines = text.lstrip().splitlines()
            if lines:
                start_idx = 0
                if self.last_wgt:
                    start_idx = 1
                    if self.last_wgt == self.kept_wgt:
                        self.last_wgt.value = f"{self.last_wgt.value}{lines[0]}"
                    else:
                        self.append_lv_text(f"{self.kept_line}{lines[0]}", **self.kept_style)

                    self.kept_line = ""
                    self.kept_style.clear()
                elif self.kept_line:
                    start_idx = 1
                    self.kept_wgt = None
                    self.append_lv_text(f"{self.kept_line}{lines[0]}", **self.kept_style)

                if left_text := lines[start_idx:-1]:
                    self.append_lv_text("\n".join(left_text), **kwargs)

                # show last line
                self.last_wgt = self.append_lv_text(lines[-1], **kwargs)
                if remeber:
                    self.kept_line = lines[-1]
                    self.kept_wgt = self.last_wgt
                    self.kept_style = dict(**kwargs)

        self.page.update()


def run_app(func: Any, log_level: int = logging.INFO, log_fmt: str = "") -> None:
    if not is_dist():
        if not log_fmt:
            log_fmt = "%(levelname)s:%(asctime)s %(message)s"

        logging.basicConfig(level=log_level, format=log_fmt)

    ft.app(func, assets_dir=get_assets_dir())
