import re
import sublime
import sublime_plugin
from .util.shell import *
from .util.runner import *
from .commands.custom import *

import imp
import sys

# imp.reload(sys.modules["Tint.util.runner"])
# imp.reload(sys.modules["Tint.util.shell"])
#sublime.sublime_api.plugin_host_ready()

PLUGIN_NAME = "Tint: Terminal"
INTRO = """

# Welcome to Terminal in a Tab (Tint for short).

You can type commands at the Tint prompt just like you would if Tint were
a real terminal.  There are a few caveats:

- Interactive commands will not work (anything that requires input)
- There is a 10 second timeout on all commands (configurable)
- You're (currently) stuck in the projects root directory
- Each command is discrete, this is not a real shell. (ex: you can't
  set/export ENV variables, etc.)

To hide this introduction edit the Tint settings and set
`show_introduction` to false.

"""


class TintNewTerminalCommand(sublime_plugin.WindowCommand):

    def run(self, cmd=None):
        view = self.window.new_file()
        view.set_name(PLUGIN_NAME)
        view.settings().set("tint.terminal", True)
        view.settings().set("line_numbers", False)
        # view.settings().set("caret_style", "solid")
        # view.settings().set("caret_extra_width", 5)
        pwd = self.window.folders()[0]
        view.settings().set("pwd", pwd)
        if cmd:
            view.settings().set("tint.command", cmd)
        view.set_scratch(True)
        view.run_command("boot_terminal")


class Buffer:
    def prompt(self, edit):
        settings = sublime.load_settings("Tint.sublime-settings")
        PROMPT = settings.get("prompt", "% ")

        end = self.view.size()
        self.view.insert(edit, end, "{}".format(PROMPT))
        self.reset_input_buffer()

    def replace_edit_buffer(self, edit, s):
        inp = self.view.get_regions("input")[0]
        self.view.replace(edit, inp, " " + s)

        end = self.view.size()
        reg = sublime.Region(inp.a, end+1)
        self.view.add_regions("input", [reg])

    def scroll_bottom(self):
        # scroll to bottom of view
        end = self.view.size()
        h = self.view.viewport_extent()[1]
        max = self.view.layout_extent()[1]
        self.view.set_viewport_position((0,max-h+5))
        # self.view.show(end)

    def reset_input_buffer(self):
        end = self.view.size()
        reg = sublime.Region(end-1, end+1)
        self.view.add_regions("input", [reg])
        self.scroll_bottom()


class TintUpCursor(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        print("up")


class TintDownCursor(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        print("down")


class TintClearCommand(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        end = self.view.size()
        self.view.replace(edit, sublime.Region(0, end), "")
        self.prompt(edit)


class TintRunLine(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        r = self.view.get_regions("input")[0]
        input = self.view.substr(r)[1:]

        end = self.view.size()
        self.view.insert(edit, end, "\n")

        sublime.set_timeout_async(lambda: self.run_async(input))

    def run_async(self, input):
        # exit built-in
        shell = SimpleShell(self.view)
        if shell.has_builtin(input):
            out, err = shell.builtin(input)
            if not out:
                return
        else:
            pwd = self.view.settings().get("pwd")
            out, err = CommandRunner(pwd).run(input)

        no_ansi = re.compile(r'\x1b[^mhlHB]+[mhlHB]')
        no_nroff = re.compile(r'.\x08')
        out = no_ansi.sub('', out)
        out = no_nroff.sub('', out)

        self.view.run_command("output", {"out": out, "err": err})


class OutputCommand(sublime_plugin.TextCommand, Buffer):
    def run(self, edit, out="", err=""):
        self.view.set_syntax_file("Packages/Text/Plain text.tmLanguage")
        end = self.view.size()
        self.view.insert(edit, end, out)
        end = self.view.size()
        self.view.insert(edit, end, err)

        # print("cmd was {}".format(input))

        self.prompt(edit)


class BootTerminalCommand(sublime_plugin.TextCommand, Buffer):

    def run(self, edit):
        startup_command = self.view.settings().get("tint.command")
        settings = sublime.load_settings("Tint.sublime-settings")
        show_intro = settings.get("show_introduction")

        if startup_command:
            self.prompt(edit)
            self.replace_edit_buffer(edit, startup_command)
            self.view.run_command("tint_run_line")
        else:
            if show_intro:
                self.view.set_syntax_file("Packages/Markdown/Markdown.tmLanguage")
                self.view.insert(edit, 0, INTRO.lstrip())
            self.prompt(edit)
