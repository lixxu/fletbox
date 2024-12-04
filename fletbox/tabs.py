#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft


def get_tabs(tabs: list = [], **kwargs: Any) -> ft.Tabs:
    kwargs.setdefault("expand", True)
    return ft.Tabs(tabs=tabs, **kwargs)


def tab(text: str = "", **kwargs: Any) -> ft.Tab:
    return ft.Tab(text, **kwargs)


tabs = get_tabs
