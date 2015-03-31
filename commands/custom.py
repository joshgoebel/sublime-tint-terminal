import sublime
import sublime_plugin


class TintRunCustomCommand(sublime_plugin.WindowCommand):
    def run(self, cmd=None):
        if cmd:
            self.go(cmd)
            return

        self.window.show_input_panel(
            "Command:",
            "",
            on_done=self.go,
            on_change=None,
            on_cancel=None
            )
        pass

    def go(self, cmd):
        if cmd:
            self.window.run_command("tint_new_terminal", {"cmd": cmd})
        # print(cmd)
