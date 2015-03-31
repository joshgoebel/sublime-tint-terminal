import re
import sublime
import sublime_plugin

from .util import *
from .commands import *

# imp.reload(sys.modules["Tint.util.runner"])
# imp.reload(sys.modules["Tint.util.shell"])
# sublime.sublime_api.plugin_host_ready()


def boot():
    if sublime.active_window().active_view():
        sublime.active_window().active_view().run_command("tint_wake_terminal")


def plugin_loaded():
    sublime.set_timeout_async(lambda: boot())


class TintRunLine(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        r = self.view.get_regions("input")[0]
        input = self.view.substr(r)[1:]

        CommandHistory(self.view).add(input)

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

        self.view.run_command("tint_print_output", {"out": out, "err": err})


class TintPrintOutputCommand(sublime_plugin.TextCommand, Buffer):
    def run(self, edit, out="", err=""):
        self.view.set_syntax_file("Packages/Text/Plain text.tmLanguage")
        end = self.view.size()
        self.view.insert(edit, end, out)
        end = self.view.size()
        self.view.insert(edit, end, err)

        # print("cmd was {}".format(input))

        self.prompt(edit)
