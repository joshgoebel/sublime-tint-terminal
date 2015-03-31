import re
import sublime
import sublime_plugin
from .util.shell import *
from .util.runner import *

import imp
import sys

imp.reload(sys.modules["TerminalWindow.util.runner"])
#sublime.sublime_api.plugin_host_ready()

PLUGIN_NAME = "TinT"
INTRO = """

# Welcome to TinT.

"""


class TerminalInTabCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.new_file()
        view.set_name(PLUGIN_NAME)
        view.settings().set("terminal_window", True)
        view.settings().set("line_numbers", False)
        pwd = self.window.folders()[0]
        view.settings().set("pwd", pwd)
        view.set_scratch(True)
        view.run_command("boot_terminal")


class Buffer:
    def prompt(self, edit):
        settings = sublime.load_settings("TerminalWindow.sublime-settings")
        PROMPT = settings.get("prompt", "% ")

        end = self.view.size()
        self.view.insert(edit, end, "{}".format(PROMPT))
        self.reset_input_buffer()

    def reset_input_buffer(self):
        end = self.view.size()
        reg = sublime.Region(end-1, end+1)
        self.view.add_regions("input", [reg])
        # scroll to bottom of view
        self.view.show(end)


class TwUpCursor(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        print("up")


class TwDownCursor(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        print("down")


class TwClearCommand(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        end = self.view.size()
        self.view.replace(edit, sublime.Region(0,end), "")
        self.prompt(edit)


class TwRunLine(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        r = self.view.get_regions("input")[0]
        input = self.view.substr(r)[1:]

        sublime.set_timeout_async(lambda: self.run_async(input))

    def run_async(self, input):

        # exit built-in
        shell = Shell(self.view)
        if shell.has_builtin(input):
            out, err = shell.builtin(input)
            if not out:
                return
        else:
            pwd = self.view.settings().get("pwd")
            out, err = CommandRunner(pwd).run(input)

        no_ansi = re.compile(r'\x1b[^mhlHB]+[mhlHB]')
        no_nroff = re.compile(r'.\x08')
        out = no_ansi.sub('',out)
        out = no_nroff.sub('',out)

        self.view.run_command("output", {"out": out, "err": err})


class OutputCommand(sublime_plugin.TextCommand, Buffer):
    def run(self, edit, out="", err="" ):
        end = self.view.size()
        self.view.insert(edit, end, "\n")

        end = self.view.size()
        self.view.insert(edit, end, out)
        end = self.view.size()
        self.view.insert(edit, end, err)

        # print("cmd was {}".format(input))

        self.prompt(edit)


class BootTerminalCommand(sublime_plugin.TextCommand, Buffer):

    def run(self, edit):
        self.view.insert(edit, 0, INTRO.lstrip())
        self.prompt(edit)

