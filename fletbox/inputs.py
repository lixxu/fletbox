#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft


def text_field(label: str, value: Any = "", **kwargs: Any) -> ft.TextField:
    return ft.TextField(label=label, value=value, **kwargs)
