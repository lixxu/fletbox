#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft

from . import buttons as fbb
from . import displays as fbdp
from . import inputs as fbi


def get_dialog(
    title: str,
    content: Any = "",
    icon: str = "",
    buttons: list = [],
    title_kw: dict = {},
    icon_kw: dict = {},
    **kwargs: Any,
) -> ft.AlertDialog:
    kw = {}
    if content:
        if isinstance(content, str):
            kw.update(content=ft.SelectionArea(ft.Text(content)))
        else:
            kw.update(content=ft.SelectionArea(content))

    align = kwargs.get("align", ft.MainAxisAlignment.END)
    if icon:
        kw.update(icon=ft.Icon(getattr(ft.Icons, icon.upper()), **icon_kw))

    return ft.AlertDialog(
        modal=kwargs.get("modal", True),
        title=ft.WindowDragArea(fbdp.expand_container(fbdp.text(title, **title_kw))),
        actions_alignment=align,
        shape=fbdp.shape(2),
        actions=buttons,
        **kw,
    )


def confirm_dialog(buttons: list = [], **kwargs: Any) -> ft.AlertDialog:
    title = kwargs.pop("title", "确定要退出吗?")
    kwargs.setdefault("icon", "warning")
    kwargs.setdefault("title_kw", dict(color="red"))
    kwargs.setdefault("icon_kw", dict(color="red", size=36))
    kwargs.update(buttons=buttons)
    return get_dialog(title, **kwargs)


def warning(title: str, page: ft.Page, **kwargs: Any) -> None:
    if not (buttons := kwargs.get("buttons")):

        def clicked(e: Any) -> None:
            page.close(dlg)
            if extra_func := kwargs.get("extra_func"):
                extra_func(e)

        buttons = [fbb.ok(func=clicked, autofocus=True)]

    kwargs.setdefault("icon", "warning")
    kwargs.setdefault("title_kw", dict(color="red"))
    kwargs.setdefault("icon_kw", dict(color="red", size=36))
    kwargs.update(buttons=buttons)
    dlg = get_dialog(title, **kwargs)
    page.open(dlg)
    page.update()
    return dlg


def confirm(title: str, page: ft.Page, **kwargs: Any) -> None:
    if not (buttons := kwargs.get("buttons")):

        def clicked(e: Any) -> None:
            page.close(dlg)
            if extra_func := kwargs.get("extra_func"):
                extra_func(e)

        buttons = [fbb.yes(func=clicked), fbb.no(func=clicked, autofocus=True)]

    kwargs.setdefault("icon", "question_mark")
    kwargs.setdefault("title_kw", dict(color="blue"))
    kwargs.setdefault("icon_kw", dict(color="blue", size=36))
    kwargs.update(buttons=buttons)
    dlg = get_dialog(title, **kwargs)
    page.open(dlg)
    page.update()
    return dlg


def banner(content: Any, **kwargs: Any) -> ft.Banner:
    if isinstance(content, str):
        content = fbdp.text(content)

    return ft.Banner(content=content, **kwargs)


class PathPicker:
    def __init__(self, label: str = "", value: str = "", kind: str = "dir", **kwargs: Any) -> None:
        button_kw = kwargs.pop("button_kw", {})
        button_label = kwargs.pop("button_label", "浏览...")
        if kind == "dir":
            kwargs.setdefault("dialog_title", "请选择目录...")
            icon = kwargs.pop("icon", "folder")
        else:
            kwargs.setdefault("dialog_title", "请选择文件...")
            if kind in ("save", "save_as"):
                icon = kwargs.pop("icon", "save")
            else:
                icon = kwargs.pop("icon", "upload_file")

        fp_text = fbi.text_field(
            label, value=value, expand=True, multiline=True, **(kwargs.pop("text_kw", {}))
        )

        picker_kw = kwargs.copy()

        def get_dir_picker(func: Any, **kwargs: Any) -> ft.FilePicker:
            return ft.FilePicker(on_result=func, **kwargs)

        def pick_result(e: ft.FilePickerResultEvent) -> None:
            if kind in ("dir", "save", "save_as"):
                if e.path:
                    fp_text.value = e.path

            else:
                paths = []
                for f in e.files or []:
                    if f.path:
                        paths.append(f.path)
                    else:
                        paths.append(f.name)

                fp_text.value = "\n".join(paths)

            fp_text.update()

        def open_dir_dlg(e: Any) -> Any:
            return fp.get_directory_path(**picker_kw)

        def open_files_dlg(e: Any) -> Any:
            return fp.pick_files(**picker_kw)

        def open_save_dlg(e: Any) -> Any:
            return fp.save_file(**picker_kw)

        def get_fp_button(func: Any) -> Any:
            return fbb.browse(label=button_label, func=func, style_kw=button_kw, icon=icon)

        if kind == "dir":
            dlg_func = open_dir_dlg
        elif kind in ("save", "save_as"):
            dlg_func = open_save_dlg
        else:
            dlg_func = open_files_dlg

        fp = get_dir_picker(pick_result)
        self.fp = fp
        self.fp_btn = get_fp_button(dlg_func)
        self.fp_text = fp_text


def dir_picker(label: str = "", value: str = "", **kwargs: Any) -> Any:
    return PathPicker(label, value, kind="dir", **kwargs)


def file_picker(label: str = "", value: str = "", **kwargs: Any) -> Any:
    return PathPicker(label, value, kind="file", **kwargs)


def save_picker(label: str = "", value: str = "", **kwargs: Any) -> Any:
    return PathPicker(label, value, kind="save", **kwargs)


dialog = get_dialog
