import sublime_plugin


class TintUpCursor(sublime_plugin.TextCommand):
    def run(self, edit):
        print("up")


class TintDownCursor(sublime_plugin.TextCommand):
    def run(self, edit):
        print("down")

