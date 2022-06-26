import os
import sublime
import sublime_plugin
from ..util.buffer import *

PLUGIN_NAME = "Tint: Terminal"
INTRO = """

# Welcome to Tint, the lightweight terminal in a tab

You can type commands at a Tint prompt just like you would at a
real terminal.  There are a few caveats:

- Interactive commands will not work
- There is a 10 second timeout on commands (configurable)
- Each command is discrete, this is not a real shell.
  - you can't export ENV variables, etc.

To hide this intro edit the Tint settings and set
`show_introduction` to `false`.

"""


class TintNewTerminalCommand(sublime_plugin.WindowCommand):

    def run(self, cmd=None):
        view = self.window.new_file()
        view.set_name(PLUGIN_NAME)
        view.settings().set("tint.terminal", True)
        view.settings().set("line_numbers", False)
        # view.settings().set("caret_style", "solid")
        # view.settings().set("caret_extra_width", 5)
        view.settings().set("tint.pwd", self.get_pwd())
        if cmd:
            view.settings().set("tint.command", cmd)
        view.set_scratch(True)
        view.run_command("tint_boot_terminal")

    def get_pwd(self):
        folders = self.window.folders()
        if folders:
            return folders[0]

        # first try users home folder
        if os.environ['HOME']:
            return os.environ['HOME']
        else:  # otherwise fallback to `pwd`
            return os.getcwd()


class TintWakeTerminalCommand(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        if not self.view.settings().get("tint.terminal"):
            return

        if not self.view.get_regions("input"):
            self.prompt(edit)


class TintBootTerminalCommand(sublime_plugin.TextCommand, Buffer):

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


class TintClearCommand(sublime_plugin.TextCommand, Buffer):
    def run(self, edit):
        end = self.view.size()
        self.view.replace(edit, sublime.Region(0, end), "")
        self.prompt(edit)
