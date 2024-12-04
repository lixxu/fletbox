#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft


def checkbox(label: str = "", value: bool = False, **kwargs: Any) -> ft.Checkbox:
    return ft.Checkbox(label=label, value=value, **kwargs)


def radio_group(options: list, value: Any = None, vertical: bool = False) -> ft.RadioGroup:
    pack_cls = ft.Column if vertical else ft.Row
    kw = {} if value is None else dict(value=value)
    radios = [ft.Radio(value=val, label=label) for val, label in options]
    return ft.RadioGroup(content=pack_cls(radios), **kw)


def dropdown(options: list = [], label: str = "", **kwargs: Any) -> ft.Dropdown:
    choices = []
    for option in options:
        text, kw = "", {}
        if isinstance(option, str):
            key = option
        else:
            if len(option) == 2:  # (key, text)
                key, text = option
            else:
                key, text, kw = option

        choices.append(dropdown_option(key, text=text, **kw))

    return ft.Dropdown(label=label, options=choices, **kwargs)


def dropdown_option(key: str, **kwargs: Any) -> ft.dropdown.Option:
    return ft.dropdown.Option(key, **kwargs)


def switch(label: str, value: bool, **kwargs: Any) -> ft.Switch:
    return ft.Switch(label=label, value=value, **kwargs)
