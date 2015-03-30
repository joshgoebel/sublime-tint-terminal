import re
import sublime
import sublime_plugin
from .util.runner import *

PROMPT = "S:TINT % "
PLUGIN_NAME = "S:TINT"



class TerminalInTabCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.new_file()
        view.run_command("boot_terminal")
        view.set_name(PLUGIN_NAME)
        view.settings().set("terminal_window", True)
        pwd = self.window.folders()[0]
        view.settings().set("pwd", pwd)
        view.set_scratch(True)


class TwUpCursor(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        print("up")


class TwDownCursor(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        print("down")


class Buffer:
    def prompt(self, edit):
        end = self.view.size()
        self.view.insert(edit, end, "{}".format(PROMPT))
        self.reset_input_buffer()

    def reset_input_buffer(self):
        end = self.view.size()
        reg = sublime.Region(end-1, end+1)
        self.view.add_regions("input", [reg])
        # scroll to bottom of view
        self.view.show(end)


class TwClearCommand(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        end = self.view.size()
        self.view.replace(edit, sublime.Region(0,end), "")
        self.prompt(edit)


class TwRunLine(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        r = self.view.get_regions("input")[0]
        input = self.view.substr(r)[1:]

        end = self.view.size()
        self.view.insert(edit, end, "\n")

        pwd = self.view.settings().get("pwd")
        out, err = CommandRunner(pwd).run(input)

        no_ansi = re.compile(r'\x1b[^mhlHB]+[mhlHB]')
        no_nroff = re.compile(r'.\x08')
        out = no_ansi.sub('',out)
        out = no_nroff.sub('',out)

        end = self.view.size()
        self.view.insert(edit, end, out)
        end = self.view.size()
        self.view.insert(edit, end, err)

        # print("cmd was {}".format(input))

        self.prompt(edit)


class BootTerminalCommand(sublime_plugin.TextCommand, Buffer):

    def run(self, edit):
        self.prompt(edit)

