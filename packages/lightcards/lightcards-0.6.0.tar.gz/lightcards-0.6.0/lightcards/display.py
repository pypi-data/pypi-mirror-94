# Display card output and retreive input
# Armaan Bhojwani 2021

import curses
import curses.panel
import os
from random import shuffle
import sys
import textwrap
import time

from . import runner, progress, parse


def panel_create(x, y):
    """Create popup panels to a certain scale"""
    win = curses.newwin(x, y)
    panel = curses.panel.new_panel(win)
    win.erase()
    return (win, panel)


class CursesError(BaseException):
    def __init__(self, message="lightcards: Curses error!"):
        self.message = message
        print(self.message)
        sys.exit(3)


class Help:
    def __init__(self, outer, mlines=20, mcols=52):
        """Initialize help screen"""
        self.outer = outer
        (self.win, self.panel) = panel_create(mlines, mcols)
        self.panel.top()
        self.panel.hide()

        text = [
            "Welcome to runner. Here are some keybindings",
            "to get you started:",
            "",
            "h, left          previous card",
            "l, right         next card",
            "j, k, up, down   flip card",
            "i, /             star card",
            "0, ^, home       go to the start of the deck",
            "$, end           go to the end of the deck",
            "H, ?             open this screen",
            "m                open the control menu",
            "1, 2, 3          switch views",
            "",
            "More information can be found in the man page, or",
            "by running `lightcards --help`.",
            "",
            "Press [H], or [?] to go back.",
        ]

        self.win.addstr(
            1,
            int(mcols / 2) - 8,
            "LIGHTCARDS HELP",
            curses.color_pair(1) + curses.A_BOLD,
        )
        self.win.hline(2, 1, curses.ACS_HLINE, mcols)

        for t in enumerate(text):
            self.win.addstr(t[0] + 3, 1, t[1])

        self.win.box()

    def disp(self):
        """Display help screen"""
        (mlines, mcols) = self.outer.win.getmaxyx()
        self.win.mvwin(int(mlines / 2) - 10, int(mcols / 2) - 25)
        self.panel.show()

        while True:
            key = self.win.getkey()
            if key == "q":
                self.outer.leave()
            elif key in ["H", "?"]:
                self.panel.hide()
                self.outer.get_key()


class Menu:
    def __init__(self, outer, mlines=17, mcols=44):
        """Initialize the menu with content"""
        self.outer = outer
        (self.win, self.panel) = panel_create(mlines, mcols)
        self.panel.top()
        self.panel.hide()

        self.win.addstr(
            1,
            int(mcols / 2) - 8,
            "LIGHTCARDS MENU",
            curses.color_pair(1) + curses.A_BOLD,
        )
        self.win.hline(2, 1, curses.ACS_HLINE, mcols)
        text = [
            "[y]: reset stack to original state",
            "[a]: alphabetize stack",
            "[z]: shuffle stack",
            "[t]: reverse stack order",
            "[u]: unstar all",
            "[d]: star all",
            "[s]: update stack to include starred only",
            "[e]: open the input file in $EDITOR",
            "",
            "[r]: restart",
            "[m]: close menu",
        ]

        for t in enumerate(text):
            self.win.addstr(t[0] + 3, 1, t[1])

        self.win.box()

    def menu_print(self, string, err=False):
        """Print messages on the menu screen"""
        if err:
            color = curses.color_pair(2)
        else:
            color = curses.color_pair(1)

        self.win.addstr(15, 1, string, color)
        self.menu_grab()

    def menu_grab(self):
        """Grab keypresses on the menu screen"""
        while True:
            key = self.win.getkey()
            if key in ["r", "m"]:
                self.panel.hide()
                self.outer.get_key()
            elif key == "q":
                self.outer.leave()
            elif key == "y":
                self.outer.stack = runner.get_orig()[1]
                self.menu_print("Stack reset!")
            elif key == "a":
                self.outer.stack.sort(key=lambda x: x.front)
                self.menu_print("Stack alphabetized!")
            elif key == "u":
                [x.unStar() for x in self.outer.stack]
                self.menu_print("All unstarred!")
            elif key == "d":
                [x.star() for x in self.outer.stack]
                self.menu_print("All starred!")
            elif key == "t":
                self.outer.stack.reverse()
                self.menu_print("Stack reversed!")
            elif key == "z":
                shuffle(self.outer.stack)
                self.menu_print("Stack shuffled!")
            elif key == "e":
                curses.endwin()
                os.system(f"$EDITOR {self.outer.input_file}"),
                (self.outer.headers, self.outer.stack) = parse.parse_html(
                    parse.md2html(self.outer.input_file)
                )
                self.outer.get_key()
            elif key == "s":
                # Check if there are any starred cards before proceeding, and
                # if not, don't allow to proceed and show an error message
                cont = False
                for x in self.outer.stack:
                    if x.starred:
                        cont = True
                        break

                if cont:
                    self.outer.stack = [
                        x for x in self.outer.stack if x.starred
                    ]
                    self.menu_print("Stars only!")
                else:
                    self.menu_print("ERR: None are starred!", err=True)
            elif key == "r":
                self.outer.obj.index = 0
                self.outer.get_key()

    def disp(self):
        """
        Display a menu offering multiple options on how to manipulate the deck
        and to continue
        """
        for i in range(42):
            self.win.addch(14, i + 1, " ")

        (mlines, mcols) = self.outer.win.getmaxyx()
        self.win.mvwin(int(mlines / 2) - 8, int(mcols / 2) - 22)
        self.panel.show()

        self.menu_grab()


class Display:
    def __init__(self, stack, headers, obj, view, input_file):
        self.stack = stack
        self.headers = headers
        self.obj = obj
        self.view = view
        self.input_file = input_file

    def run(self, stdscr):
        """Set important options that require stdscr before starting"""
        self.win = stdscr
        curses.curs_set(0)  # Hide cursor
        curses.use_default_colors()  # Allow transparency
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)

        self.main_panel = curses.panel.new_panel(self.win)
        self.menu_obj = Menu(self)
        self.help_obj = Help(self)

        self.get_key()

    def check_size(self):
        (mlines, mcols) = self.win.getmaxyx()

        while mlines < 24 or mcols < 60:
            self.win.clear()
            self.win.addstr(
                0,
                0,
                textwrap.fill(
                    "Terminal too small! Min size 60x24", width=mcols
                ),
            )
            self.win.refresh()
            (mlines, mcols) = self.win.getmaxyx()
            time.sleep(0.1)
        else:
            self.disp_card()

    def leave(self):
        """Pickle stack before quitting"""
        if self.obj.index + 1 == len(self.stack):
            self.obj.index = 0

        progress.dump(self.stack, runner.get_orig()[1])
        sys.exit(0)

    def nstarred(self):
        """Get total number of starred cards"""
        return [card for card in self.stack if card.starred]

    def disp_bar(self):
        """
        Display the statusbar at the bottom of the screen with progress, star
        status, and card side.
        """
        (mlines, mcols) = self.win.getmaxyx()
        self.win.hline(mlines - 2, 0, 0, mcols)

        # Calculate percent done
        if len(self.stack) <= 1:
            percent = "100"
        else:
            percent = str(
                round(self.obj.index / (len(self.stack) - 1) * 100)
            ).zfill(2)

        # Print yellow if starred
        if self.current_card().starred:
            star_color = curses.color_pair(3)
        else:
            star_color = curses.color_pair(1)

        # Compose bar text
        bar_start = "["
        bar_middle = self.current_card().printStar()
        bar_end = (
            f"] [{len(self.nstarred())}/{str(len(self.stack))} starred] "
            f"[{percent}% ("
            f"{str(self.obj.index).zfill(len(str(len(self.stack))))}"
            f"/{str(len(self.stack))})]"
        )
        if self.view != 3:
            bar_end += (
                f" [{self.get_side()} ("
                f"{str(int(self.current_card().side) + 1)})]"
            )
        bar_end += f" [View {str(self.view)}]"

        # Put it all togethor
        self.win.addstr(mlines - 1, 0, bar_start, curses.color_pair(1))
        self.win.addstr(mlines - 1, len(bar_start), bar_middle, star_color)
        self.win.addstr(
            mlines - 1,
            len(bar_start + bar_middle),
            textwrap.shorten(bar_end, width=mcols - 20, placeholder="…"),
            curses.color_pair(1),
        )

    def wrap_width(self):
        """Calculate the width at which the body text should wrap"""
        (_, mcols) = self.win.getmaxyx()
        wrap_width = mcols - 20
        if wrap_width > 80:
            wrap_width = 80
        return wrap_width

    def get_side(self):
        if self.obj.side == 0:
            return self.headers[self.current_card().side]
        else:
            return self.headers[self.current_card().get_reverse()]

    def disp_card(self):
        (_, mcols) = self.win.getmaxyx()
        self.main_panel.bottom()
        self.win.clear()
        num_done = str(self.obj.index + 1).zfill(len(str(len(self.stack))))

        if self.view in [1, 2, 4]:
            """
            Display the contents of the card.
            Shows a header, a horizontal line, and the contents of the current
            side.
            """
            # If on the back of the card, show the content of the front side in
            # the header
            if self.view == 1:
                self.obj.side = 0
            elif self.view == 2:
                self.obj.side = 1

            if self.current_card().side == 0:
                top = num_done + " | " + self.get_side()
            else:
                top = (
                    num_done
                    + " | "
                    + self.get_side()
                    + ' | "'
                    + str(self.current_card().get()[self.obj.get_reverse()])
                    + '"'
                )

            self.win.addstr(
                0,
                0,
                textwrap.shorten(top, width=mcols - 20, placeholder="…"),
                curses.A_BOLD,
            )

            # Show current side
            self.win.addstr(
                2,
                0,
                textwrap.fill(
                    self.current_card().get()[self.obj.side],
                    width=self.wrap_width(),
                ),
            )

        elif self.view == 3:
            """
            Display the contents of the card with both the front and back sides.
            """
            (_, mcols) = self.win.getmaxyx()
            self.main_panel.bottom()
            self.win.clear()

            self.win.addstr(
                0,
                0,
                textwrap.shorten(
                    num_done,
                    width=mcols - 20,
                    placeholder="…",
                ),
                curses.A_BOLD,
            )

            # Show card content
            self.win.addstr(
                2,
                0,
                textwrap.fill(
                    self.headers[0] + ": " + self.current_card().front,
                    width=self.wrap_width(),
                )
                + "\n\n"
                + textwrap.fill(
                    self.headers[1] + ": " + self.current_card().back,
                    width=self.wrap_width(),
                ),
            )

        self.win.hline(1, 0, curses.ACS_HLINE, mcols)
        self.disp_bar()
        self.disp_sidebar()

    def current_card(self):
        """Get current card object"""
        return self.stack[self.obj.index]

    def get_key(self):
        """
        Display a card and wait for the input.
        Used as a general way of getting back into the card flow from a menu
        """
        while True:
            self.check_size()
            key = self.win.getkey()
            if key == "q":
                self.leave()
            elif key in ["h", "KEY_LEFT"]:
                self.obj.back()
                self.current_card().side = 0
                self.disp_card()
            elif key in ["l", "KEY_RIGHT"]:
                if self.obj.index + 1 == len(self.stack):
                    self.menu_obj.disp()
                else:
                    self.obj.forward(self.stack)
                    self.current_card().side = 0
                    self.disp_card()
            elif key in ["j", "k", "KEY_UP", "KEY_DOWN"] and self.view != 3:
                self.current_card().flip()
                self.disp_card()
            elif key in ["i", "/"]:
                self.current_card().toggleStar()
                self.disp_card()
            elif key in ["0", "^", "KEY_HOME"]:
                self.obj.index = 0
                self.current_card().side = 0
                self.disp_card()
            elif key in ["$", "KEY_END"]:
                self.obj.index = len(self.stack) - 1
                self.current_card().side = 0
                self.disp_card()
            elif key in ["H", "?"]:
                self.help_obj.disp()
            elif key == "m":
                self.menu_obj.disp()
            elif key in ["1", "2", "3", "4"]:
                self.view = int(key)

    def disp_sidebar(self):
        """Display a sidebar with the starred terms"""
        (mlines, mcols) = self.win.getmaxyx()
        left = mcols - 19

        self.win.addstr(
            0,
            mcols - 16,
            "STARRED CARDS",
            curses.color_pair(3) + curses.A_BOLD,
        )
        self.win.vline(0, mcols - 20, 0, mlines - 2)

        nstarred = self.nstarred()
        for i, card in enumerate(nstarred):
            term = card.get()[self.obj.side]
            if len(term) > 18:
                term = term[:18] + "…"

            if i > mlines - 5:
                for i in range(19):
                    self.win.addch(mlines - 3, left + i, " ")

                self.win.addstr(
                    mlines - 3,
                    left,
                    f"({len(nstarred) - i - 2} more)",
                )
            else:
                self.win.addstr(2 + i, left, term)

        if len(self.nstarred()) == 0:
            self.win.addstr(2, left, "None starred")
