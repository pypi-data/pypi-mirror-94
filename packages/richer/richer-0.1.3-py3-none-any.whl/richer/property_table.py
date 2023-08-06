
from dataclasses import dataclass, fields
from typing import Any

from rich import box
from rich.table import Table


@dataclass
class PropertyTable:
    item: Any
    inner: bool = False

    def __rich__(self) -> Table:
        show_edge = not self.inner
        __table = Table(box=box.SQUARE, show_edge=show_edge,
                        show_header=False, show_lines=True)

        for f in fields(self.item):
            __table.add_row(style(f.name), cell(getattr(self.item, f.name)))

        return __table
