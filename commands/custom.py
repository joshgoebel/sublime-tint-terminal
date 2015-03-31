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
        self.window.run_command("terminal_in_tab", {"cmd": cmd})
        # print(cmd)
