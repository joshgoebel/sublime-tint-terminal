import sublime
import sublime_plugin


class TintUpCursor(sublime_plugin.TextCommand):
    def run(self, edit):
        print("up")


class TintDownCursor(sublime_plugin.TextCommand):
    def run(self, edit):
        print("down")


class TintBeginLine(sublime_plugin.TextCommand):
    def run(self, edit):
        inp = self.view.get_regions("input")[0]
        c = inp.a+1
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(c,c))

