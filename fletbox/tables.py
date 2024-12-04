#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from typing import Any

import flet as ft

from . import displays as fbdp


def table(
    columns: list = [], rows: list = [], columns_kw: dict = {}, rows_kw: dict = {}, **kwargs: Any
) -> ft.DataTable:
    """columns like: ['text', ft.Control(...), ('text', kwargs)]
    rows: [['text', ft.Control(...), ('text', kwargs)]]
    """
    cols = get_columns(columns, **columns_kw)
    row_list = get_rows(rows, **rows_kw)
    return ft.DataTable(columns=cols, rows=row_list, **kwargs)


def get_columns(headers: list = [], **kwargs: Any) -> list:
    cols = []
    for col in headers:
        if isinstance(col, (tuple, list)):
            cols.append(get_column(col[0], col[1], **kwargs))
        else:
            cols.append(get_column(col, **kwargs))

    return cols


def get_rows(rows: list = [], **kwargs: Any) -> list:
    return [get_row(row, **kwargs) for row in rows]


def get_cell(data: Any, **kwargs: Any) -> Any:
    if isinstance(data, ft.Control):
        return data

    return fbdp.text(data, **kwargs)


def get_column(col: Any, kw: dict = {}, **kwargs: Any) -> ft.DataColumn:
    kw.setdefault("bold", True)
    return ft.DataColumn(get_cell(col, **kw), **kwargs)


def get_row(values: list = [], cell_kw: dict = {}, **kwargs: Any) -> ft.DataRow:
    cells = []
    for c in values:
        if isinstance(c, (tuple, list)):
            cells.append(ft.DataCell(get_cell(c[0], **c[1]), **cell_kw))
        else:
            cells.append(ft.DataCell(get_cell(c), **cell_kw))

    return ft.DataRow(cells, **kwargs)
