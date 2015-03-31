import sublime


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
