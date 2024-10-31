#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft


def create_checkbox(label: str = "", value: bool = False, **kwargs: Any) -> ft.Checkbox:
    return ft.Checkbox(label=label, value=value, **kwargs)


def create_radio_group(options: list, value: Any = None, vertical: bool = False) -> ft.RadioGroup:
    radios = [ft.Radio(value=val, label=label) for val, label in options]
    pack_cls = ft.Column if vertical else ft.Row
    kw = {} if value is None else dict(value=value)
    return ft.RadioGroup(content=pack_cls(radios), **kw)


def create_dropdown(options: list, label: str = "", **kwargs: Any) -> ft.Dropdown:
    choices = []
    for option in options:
        text, kw = "", {}
        if isinstance(option, str):
            key = option
        else:
            if len(option) == 2:
                # (key, text)
                key, text = option
            else:
                key, text, kw = option

        choices.append(ft.dropdown.Option(key, text=text, **kw))

    return ft.Dropdown(label=label, options=choices, **kwargs)
