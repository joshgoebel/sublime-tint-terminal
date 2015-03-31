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

    def chdir(self):
        return self.cd()

    def bye(self):
        return self.exit()

    def exit(self):
        self.view.window().run_command("close_file")
