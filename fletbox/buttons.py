#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

from . import helpers as fbh


def ok(**kwargs: Any) -> Any:
    return fbh.get_button(
        kwargs.pop("label", "确定"), kwargs.pop("func", None), icon=kwargs.pop("icon", "check"), **kwargs
    )


def save(**kwargs: Any) -> Any:
    return fbh.get_button(
        kwargs.pop("label", "保存"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "save"),
        icon=kwargs.pop("icon", "save"),
        **kwargs,
    )


def cancel(**kwargs: Any) -> Any:
    return fbh.get_button(
        kwargs.pop("label", "取消"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "cancel"),
        icon=kwargs.pop("icon", "close"),
        **kwargs,
    )


def yes(**kwargs: Any) -> Any:
    return fbh.get_button(
        kwargs.pop("label", "是"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "yes"),
        icon=kwargs.pop("icon", "check"),
        **kwargs,
    )


def no(**kwargs: Any) -> Any:
    return fbh.get_button(
        kwargs.pop("label", "否"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "no"),
        icon=kwargs.pop("icon", "close"),
        **kwargs,
    )


def add(**kwargs: Any) -> Any:
    return fbh.get_button(
        kwargs.pop("label", "添加"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "add"),
        icon=kwargs.pop("icon", "add"),
        **kwargs,
    )


def edit(**kwargs: Any) -> Any:
    return fbh.get_button(
        kwargs.pop("label", "修改"),
        kwargs.pop("func", None),
        data=kwargs.pop("data", "edit"),
        icon=kwargs.pop("icon", "mode_edit_outlined"),
        **kwargs,
    )


def delete(**kwargs: Any) -> Any:
    return fbh.create_top_button(
        kwargs.pop("label", "删除"),
        data=kwargs.pop("data", "delete"),
        func=kwargs.pop("func", None),
        icon=kwargs.pop("icon", "delete"),
        color=kwargs.pop("color", "red"),
        **kwargs,
    )
