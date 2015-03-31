import sublime
import sublime_plugin
from ..util import *


class TintReplaceInput(sublime_plugin.TextCommand, Buffer):
    def run(self, edit, cmd=""):
        self.replace_edit_buffer(edit, cmd)


class TintUpCursor(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        self.edit = edit
        self.items = [[item] for item in CommandHistory(self.view).list()]
        self.view.window().show_quick_panel(self.items,
            self.go,
            sublime.MONOSPACE_FONT,
            len(items)-1,
            self.replace
            )
        print("up")

    def replace(self, index):
        cmd = self.items[index][0]
        self.view.run_command("tint_replace_input", {"cmd": cmd})

    def go(self, index):
        if index == -1:
            return

        cmd = self.items[index][0]
        self.view.run_command("tint_run_line")


class TintDownCursor(sublime_plugin.TextCommand):
    def run(self, edit):
        print("down")


class TintGoBeginLine(sublime_plugin.TextCommand):
    def run(self, edit):
        inp = self.view.get_regions("input")[0]
        c = inp.a+1
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(c,c))

