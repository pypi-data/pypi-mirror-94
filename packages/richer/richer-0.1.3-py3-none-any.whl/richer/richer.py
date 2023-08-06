from datetime import datetime
from dataclasses import dataclass, is_dataclass,
from typing import Any, List


def cell(value):
    if value is None:
        return '-'
    elif isinstance(value, str):
        if not value:
            return '-'
        return value
    elif isinstance(value, int):
        return f'{value:,}'  # ex) 9,999
    elif isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, Table):
        return value
    elif isinstance(value, List):
        return ListRenderer(value, inner=True)
    elif is_dataclass(value):
        return PropertyRenderer(value, inner=True)
    else:
        return value


@dataclass
class Sort:
    key: str
    order: str


@dataclass
class PropertyRenderer:
    item: Any
    inner: bool = False

    def __rich__(self) -> Table:
        show_edge = not self.inner
        __table = Table(box=box.SQUARE, show_edge=show_edge,
                        show_header=False, show_lines=True)

        for f in fields(self.item):
            __table.add_row(style(f.name), cell(getattr(self.item, f.name)))

        return __table
