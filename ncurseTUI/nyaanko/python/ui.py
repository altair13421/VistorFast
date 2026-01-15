# nyaa_tui.py
import curses
import json
import os
from datetime import datetime
from typing import Any
from automator.nyaa import search_torrent
from automator import get_categories

CONFIG_FILE = os.path.join(".", "config.json")

def get_config() -> dict[str,Any]:
    with open(CONFIG_FILE) as config_read:
        config = json.load(config_read)
    return config

def create_config(config: dict["str", Any]) -> bool:
    try:
        with open(CONFIG_FILE, "w") as config_write:
            config_write.write(json.dumps(config, indent=4, sort_keys=False))
        return True
    except:
        return False
class TorrentHelper:
    def __init__(self):
        pass

    def get_default_settings(self): ...

    def add_magnet(self, magnet): ...


class Torrenting(TorrentHelper):
    def __init__(self):
        self.torrents = []

    def draw_header(self, stdscr, height, width):
        """Draw application header"""
        # Title
        title = " Torrentor "
        stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)

        # Stats
        total = len(self.torrents)
        stats = f"Torrent-or| Total: {total}"
        stdscr.addstr(2, (width - len(stats)) // 2, stats)

        # Separator
        stdscr.addstr(3, 0, "=" * width)


    def draw_torrents(self, stdscr, height, width): ...


    def draw_footer(self, stdscr, height, width):
        """Draw help/status footer"""
        # Separator
        stdscr.addstr(height - 4, 0, "-" * width)

        # Help text
        help_items = [
            ("a", "Add Magnet"),
            ("s", "Stop/Start"),
            ("d", "Delete"),
            ("f", "Search Files"),
            ("o", "Open (Linux Only)"),
            ("T", "Change Screen"),
            ("q", "Quit"),
        ]

        help_text = " | ".join([f"{key}: {desc}" for key, desc in help_items])
        stdscr.addstr(height - 2, (width - len(help_text)) // 2, help_text)

    def draw_ui(self, stdscr):
        """Main UI drawing function"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Title
        title = "Torrenting Screen"
        win = curses.initscr()
        win.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)

        # Setup colors (if supported)
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Pending
            curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Completed
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlight
        self.draw_header(win, height, width)

        self.draw_footer(win, height, width)


class NyaaHelper:
    def __init__(self):
        self.categories = get_categories()

    def search(self):
        return search_torrent(
            search=self.query,
            category=self.category,
            sub_category=self.sub_category,
            page = self.page,
        )

    def startup(self):
        torrents = self.search()
        self.torrents = torrents

    def get_category(self, cat_string):
        cat, sub_cat = cat_string.split("_")
        if cat == "0" and sub_cat == "0":
            return "All"
        if sub_cat == "0":
            return f"{self.categories[cat]["name"]} - All"
        return f"{self.categories[cat]['name']} - {self.categories[cat]['sub_cats'][sub_cat]}"

class NyaaScreen(NyaaHelper):
    def __init__(self):
        super().__init__()
        self.torrents = []
        self.query = ""
        self.filter = 0
        self.category = 0
        self.sub_category = 0
        self.page = 1
        self.running = True
        self.selected = 0
        self.startup()
        self.filter_mode = ""  # Added missing attribute filter_mode
        self.start_index = 0

    def draw_header(self, stdscr, height, width):
        """Draw application header"""
        # Title
        title = " Nyaa App (ncurses) "
        stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)

        # Stats
        total = len(self.torrents)
        stats = f"Torrent-or| Total: {total} | Searching: {self.query if self.query != '' else 'Nothing'} | Filtering: {self.get_category(f'{self.category}_{self.sub_category}')}"
        stdscr.addstr(2, (width - len(stats)) // 2, stats)

        # Separator
        stdscr.addstr(3, 0, "=" * width)

    def draw_footer(self, stdscr, height, width):
        """Draw help/status footer"""
        # Separator
        stdscr.addstr(height - 4, 0, "-" * width)

        # Filter status
        # filter_text = f"Filter: {self.filter_mode}"
        # stdscr.addstr(height - 3, 2, filter_text, curses.A_BOLD)

        # Help text
        help_items = [
            ("s", "search"),
            ("f", "Filter"),
            ("r", "Reset"),
            ("Space", "Toggle"),
            ("o", "Open Torrent App"),
            ("T", "Change Screen"),
            ("q", "Quit"),
        ]

        help_text = " | ".join([f"{key}: {desc}" for key, desc in help_items])
        stdscr.addstr(height - 2, (width - len(help_text)) // 2, help_text)

    def draw_torrents(self, stdscr, height, width):
        # Torrents
        max_torrents = (
            height - 7
        )  # Leave space for header (4 lines) and footer (3 lines)
        for i, torrent in enumerate(self.torrents[:max_torrents]):
            text = f"{torrent['size']}\t|\tSeeds:{torrent['seeders']}  \t|\t{torrent['category']}\t|\t{torrent['title']} | "
            # Truncate text if it's too long for the width
            if len(text) > width - 4:
                text = text[: width - 7] + "..."

            # Highlight selection
            if i == self.selected:
                stdscr.addstr(i + 4, 2, text, curses.A_REVERSE)
            else:
                stdscr.addstr(i + 4, 2, text)

    def handle_input(self, stdscr, key):
        # Navigation
        if key == curses.KEY_UP:
            self.selected = max(0, self.selected - 1)
        elif key == curses.KEY_DOWN:
            self.selected = min(len(self.torrents) - 1, self.selected + 1)

        # No Page Stuff
        # elif key == curses.KEY_LEFT:
        #     if self.page > 1:
        #         self.page -= 1
        #     self.torrents = self.search()
        # elif key == curses.KEY_RIGHT:
        #     self.page += 1
        #     self.torrents = self.search()
        # main UI
        elif key == ord("s"):
            self.handle_search(stdscr)
        elif key == ord("f"):
            self.handle_filter(stdscr)
        elif key == ord('r'):
            self.query = ""
            self.category = 0
            self.sub_category = 0
            self.torrents = self.search()

    def handle_filter(self, stdscr):
        h, w = stdscr.getmaxyx()

        category = " | ".join([f"{key}: {desc['name']}" for key, desc in self.categories.items()])
        stdscr.addstr(h-3, 2, category)

        prompt = "Filter: "
        stdscr.addstr(h-2, 2, prompt)

        # Setting up for input
        curses.echo()
        curses.curs_set(1)

        # Get input
        stdscr.refresh()
        try:
            user_input = stdscr.getstr(h - 2, len(prompt) + 2, w - len(prompt) - 4)
            text = user_input.decode("utf-8").strip()
            if text:
                self.category = text
                if self.category == 0:
                    self.torrents = self.search()
                else:
                    sub_cat = " | ".join([f"{key}: {desc}" for key, desc in self.categories[text]["sub_cats"].items()])
                    stdscr.addstr(h-3, 2, sub_cat)
                    try:
                        user_input = stdscr.getstr(h - 2, len(prompt) + 2, w - len(prompt) - 4)
                        text = user_input.decode("utf-8").strip()
                        if text:
                            self.sub_category = text
                            self.torrents = self.search()
                    except Exception:
                        pass
        except Exception:
            pass
        curses.noecho()
        curses.curs_set(0)

    def handle_search(self, stdscr):
        """Simple input dialog"""
        h, w = stdscr.getmaxyx()

        # Show input prompt
        prompt = "New Search: "
        stdscr.addstr(h - 3, 2, prompt)

        # Setup for input
        curses.echo()
        curses.curs_set(1)

        # Get input
        stdscr.refresh()
        try:
            user_input = stdscr.getstr(h - 3, len(prompt) + 2, w - len(prompt) - 4)
            text = user_input.decode("utf-8").strip()
            if text:
                self.query = text
                self.torrents = self.search()
        except Exception:
            pass
        curses.noecho()
        curses.curs_set(0)

    def draw_ui(self, stdscr):
        """Main UI drawing function"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Title
        title = "Simple NYAA Interpreter"
        win = curses.initscr()
        win.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)
        # Setup colors (if supported)
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Pending
            curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Completed
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlight

        # Draw all UI components
        self.draw_header(win, height, width)
        self.draw_torrents(win, height, width)
        self.draw_footer(win, height, width)

        stdscr.refresh()


class TerminalUI():
    def __init__(self):
        self.running = True
        self.screens = {
            "NyaaScreen": NyaaScreen(),
            "TorrentScreen": Torrenting(),
        }
        self.active_screen = self.get_home_screen()

    def get_home_screen(self):
        screen_keys = list(self.screens.keys())
        return screen_keys[0]

    def get_next_screen(self):
        screen_keys = list(self.screens.keys())
        current_idx = screen_keys.index(self.active_screen)
        self.active_screen = screen_keys[(current_idx + 1) % len(screen_keys)]

    def copy_to_clipboard(self, index): ...


    def draw_ui(self, stdscr):
        self.screens[self.active_screen].draw_ui(stdscr)

    def handle_input(self, stdscr, key):
        if key == ord("q"):
            self.running = False

        elif key == ord("T"):
            self.get_next_screen()

        else:
            self.screens[self.active_screen].handle_input(stdscr, key)

    def run(self, stdscr):
        """Main application loop"""
        # Setup
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(0)  # Wait for input
        stdscr.clear()

        # Initial draw
        self.draw_ui(stdscr)

        # Main loop
        while self.running:
            # Draw UI
            self.draw_ui(stdscr)

            # Get input
            try:
                key = stdscr.getch()
                self.handle_input(stdscr, key)
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                # Handle any errors gracefully
                self.draw_error(stdscr, str(e))

        # Cleanup
        curses.curs_set(1)

    def draw_error(self, stdscr, message):
        """Draw error message on the screen"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        error_msg = f"Error: {message}"
        stdscr.addstr(height // 2, (width - len(error_msg)) // 2, error_msg, curses.A_BOLD | curses.color_pair(3))
        stdscr.refresh()
        stdscr.getch()  # Wait for user to acknowledge
        self.running = False


def main():
    app = TerminalUI()
    curses.wrapper(app.run)


if __name__ == "__main__":
    main()
