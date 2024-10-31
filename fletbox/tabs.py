#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft


def tabs(tabs_list: list = [], **kwargs: Any) -> ft.Tabs:
    kwargs.setdefault("expand", True)
    return ft.Tabs(tabs=tabs_list, **kwargs)


def tab(text: str = "", **kwargs: Any) -> ft.Tab:
    return ft.Tab(text, **kwargs)
