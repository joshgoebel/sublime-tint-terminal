import sublime
import sublime_plugin


class CommandHistory():
    def __init__(self, view):
        self._view = view
        self._history = view.settings().get("tint.history") or []

    def add(self, cmd):
        previous = self._history[-1] if self._history else None
        if previous != cmd:
            self._history.append(cmd)
            self._view.settings().set("tint.history", self._history)

    def list(self):
        return self._history


class Watcher(sublime_plugin.EventListener):
    def on_activated(self, view):
        if view.settings().get("tint.terminal"):
            view.run_command("tint_wake_terminal")

    def on_selection_modified(self, view):
        if not view.settings().get("tint.terminal"):
            return

        sel = view.sel()[0]
        inp = view.get_regions("input")
        if inp and inp[0].contains(sel.a):
            print("data entry")
            view.settings().set("tint.entry", True)
        else:
            print("data entry: NO")
            view.settings().set("tint.entry", False)


class Buffer():

    def prompt(self, edit):
        settings = sublime.load_settings("Tint.sublime-settings")
        prompt = settings.get("prompt", "% ")

        end = self.view.size()
        self.view.insert(edit, end, prompt)
        end += len(prompt)

        # move cursor to input area
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(end,end))
        self.reset_input_buffer()

    def replace_edit_buffer(self, edit, s):
        inp = self.view.get_regions("input")[0]
        self.view.replace(edit, inp, " " + s)

        end = self.view.size()
        reg = sublime.Region(inp.a, end+1)
        self.view.add_regions("input", [reg])

    def scroll_bottom(self):
        end = self.view.size()
        h = self.view.viewport_extent()[1]
        max = self.view.layout_extent()[1]
        self.view.set_viewport_position((0, max-h+5))

    def reset_input_buffer(self):
        end = self.view.size()
        reg = sublime.Region(end-1, end+1)
        self.view.add_regions("input", [reg])
        self.scroll_bottom()
