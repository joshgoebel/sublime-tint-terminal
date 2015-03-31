import sublime

class SimpleShell():
    def __init__(self, view):
        self.view = view
        pass

    def has_builtin(self, string):
        cmd = string.split(" ")[0]
        return getattr(self, cmd, None)

    def builtin(self, string):
        cmd = string.split(" ")[0]
        fn = getattr(self, cmd, None)
        return (fn(), "")

    def cd(self):
        return "You may not change directories.\n"

    # easter egg
    def whoareyou(self):
        return "I'm Sublime {}. Thanks for asking.\n".format(sublime.version())

    def chdir(self):
        return self.cd()

    def bye(self):
        return self.exit()

    def clear(self):
        self.view.run_command("tint_clear")

    def exit(self):
        self.view.window().run_command("close_file")
