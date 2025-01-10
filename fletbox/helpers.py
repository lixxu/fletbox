#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import flet as ft
from flet.security import decrypt, encrypt


def is_dark_mode(page: ft.Page) -> bool:
    return page.theme_mode == ft.ThemeMode.DARK


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
        settings.update(is_max=is_max, is_dark=is_dark_mode(page))
        if not is_max:
            settings.update(win_top=top, win_left=left, win_height=height, win_width=width)

    return settings


def restore_window(page: ft.Page, settings: Any) -> None:
    top = settings.get("win_top")
    left = settings.get("win_left")
    width = settings.get("win_width")
    height = settings.get("win_height")
    if width and height:
        page.window.width = float(width)
        page.window.height = float(height)
        try:
            top = float(top)
        except Exception:
            top = -1

        try:
            left = float(left)
        except Exception:
            left = -1

        if top < 0:
            top = 100

        if left < 0:
            left = 300

        page.window.top = float(top)  # type: ignore
        page.window.left = float(left)  # type: ignore

    if settings.get("is_max"):
        page.window.maximized = True

    if settings.get("is_dark"):
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT

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

    return not sys.argv[0].endswith(".py")


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


def validate(wgt: Any, val: Any, error_kind: str = "error_text") -> bool:
    is_ok = True
    if str(val):
        fg = None
        error_text = ""
    else:
        fg = "red"
        is_ok = False
        error_text = "不能为空"

    if error_kind == "error_text":
        if hasattr(wgt, "error_text"):
            wgt.error_text = error_text

    elif hasattr(wgt, "border_color"):
        wgt.border_color = fg

    return is_ok


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
        return self.__app_name__.lower()

    @property
    def app_org(self) -> str:
        return self.__app_org__.lower()

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

    def __init__(self, page: ft.Page) -> None:
        self.page = page

    @property
    def lv(self) -> Any:
        return self.page.lv

    def clear_controls(self) -> None:
        self.last_wgt = None
        self.kept_wgt = None
        self.lv.controls.clear()

    def append_lv_text(self, text: Any, **kwargs: Any) -> ft.Text:
        # wgt = ft.Text(f"{text}", **kwargs)
        # self.lv.controls.append(wgt)
        # return wgt

        # display line by line due to scroll bar issue
        wgts = []
        for line in f"{text or ' '}".splitlines(True):
            if bool(line):
                wgt = ft.Text(line.removesuffix("\n"), **kwargs)
                self.lv.controls.append(wgt)
                wgts.append(wgt)

        return wgts[-1]

    def append_to_row(self, text: str, **kwargs: Any) -> None:
        wgt = kwargs.pop("wgt", None)
        (wgt or self.last_wgt).spans.append(ft.TextSpan(text, ft.TextStyle(**kwargs)))

    def echo(self, text: Any, **kwargs: Any) -> None:
        if not f"{text}":
            return

        if kwargs.pop("ts", False):
            text = f"[{datetime.now()}] {text}"
        else:
            text = f"{text}"

        new_line = kwargs.pop("nl", True)
        if new_line:
            text = f"{text}\n"

        if kwargs.pop("bold", False):
            kwargs.setdefault("weight", "bold")

        if fg := kwargs.pop("fg", None):
            kwargs.setdefault("color", fg)

        if bg := kwargs.pop("bg", None):
            kwargs.setdefault("bgcolor", bg)

        # if update last control for append to last
        kwargs.pop("remeber", None)
        append_to_last = kwargs.pop("append_to_last", None)
        lines = text.splitlines(True)
        if not append_to_last:
            self.kept_wgt = None
            if self.last_wgt:
                self.append_to_row(lines[0].removesuffix("\n"), **kwargs)
                if len(lines) > 1:
                    self.last_wgt = self.append_lv_text("".join(lines[1:]), **kwargs)

            else:
                last_wgt = self.append_lv_text(text, **kwargs)
                self.last_wgt = None if new_line else last_wgt

            if new_line:
                self.last_wgt = None

        else:
            self.last_wgt = None
            if self.kept_line and not self.kept_wgt:
                self.kept_wgt = self.append_lv_text(self.kept_line)

            if self.kept_wgt:
                self.append_to_row(lines[0].removesuffix("\n"), wgt=self.kept_wgt, **kwargs)
                if len(lines) > 1:
                    self.kept_wgt = self.append_lv_text("".join(lines[1:]), **kwargs)

            else:
                self.kept_wgt = self.append_lv_text(text, **kwargs)

            self.kept_line = lines[-1]

        self.page.update()


def run_app(func: Any, log_level: int = logging.INFO, log_fmt: str = "", **kwargs: Any) -> None:
    if not is_dist():
        if not log_fmt:
            log_fmt = "%(levelname)s:%(asctime)s %(message)s"

        logging.basicConfig(level=log_level, format=log_fmt)

    ft.app(func, assets_dir=get_assets_dir(), **kwargs)
