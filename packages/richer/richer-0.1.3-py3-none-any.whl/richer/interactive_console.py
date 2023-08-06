import curses
from curses import wrapper

from richer.richer import PropertyRenderer, ListRenderer, Sort, Column


class InteractiveConsole:
    def __init__(self, items):
        self.items = items

        # Define color table
        colors = [
            curses.COLOR_RED,
            curses.COLOR_GREEN,
            curses.COLOR_YELLOW,
            curses.COLOR_BLUE,
            curses.COLOR_MAGENTA,
            curses.COLOR_CYAN,
            curses.COLOR_WHITE
        ]

        # Put colors into curses
        curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        for i, c in enumerate(colors):
            curses.init_pair(i + 1, c, -1)

        # http://ascii-table.com/ansi-escape-sequences.php
        self.graphic_mode = {
            '0': curses.A_NORMAL,
            '1': curses.A_BOLD,
            '30': curses.COLOR_BLACK,
            '40': curses.COLOR_BLACK
        }

        for i, c in enumerate(colors):
            self.graphic_mode['3' + str(i + 1)] = curses.color_pair(i + 1)

    def paginate(self, page, size):
        return self.items[page * size:(page + 1) * size]

    def print(self):
        wrapper(self.main)

    def main(self, stdscr):
        page = 0

        while True:
            stdscr.clear()

            from rich.console import Console
            console = Console()

            from richer.richer import ListRenderer

            # Pagination
            items = self.paginate(page, console.size.height - 5)

            # Print on buffer
            with console.capture() as capture:
                console.print(ListRenderer(items))
                # console.print("[bold red]Hello\nWorld[/]")
            output = capture.get()

            from richer.parser import parse
            tokens = parse(output)

            for t in tokens:
                mode = curses.A_NORMAL
                for a in t.attr.split(';'):
                    mode = mode | self.graphic_mode.get(a, curses.A_NORMAL)
                stdscr.addstr(t.row, t.col, t.text, mode)

            stdscr.refresh()

            while True:
                c = stdscr.getch()
                if c == ord('q'):
                    return

                elif c == curses.KEY_LEFT or c == curses.KEY_PPAGE:
                    if page > 0:
                        page -= 1
                        break

                elif c == curses.KEY_RIGHT or c == curses.KEY_NPAGE:
                    page += 1
                    break
