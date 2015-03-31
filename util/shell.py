import sublime
import os


class SimpleShell():
    def __init__(self, view):
        self.view = view
        pass

    def has_builtin(self, string):
        cmd = string.split(" ")[0]
        return getattr(self, cmd, None)

    def builtin(self, string):
        cmd = string.split(" ")[0]
        args = string.split(" ")[1:]
        fn = getattr(self, cmd, None)
        return (fn(args), "")

    def cd(self, args):
        pwd = self.view.settings().get("tint.pwd")
        args = " ".join(args)
        p = os.path.abspath(os.path.join(pwd, args))
        if os.path.isdir(p):
            self.view.settings().set("tint.pwd", p)
            return ""
        else:
            return "cd: no such file or directory: {}\n".format(args)

    # easter egg
    def whoareyou(self):
        return "I'm Sublime {}. Thanks for asking.\n".format(sublime.version())

    def chdir(self, *args):
        return self.cd(*args)

    def bye(self, *args):
        return self.exit()

    def clear(self, *args):
        self.view.run_command("tint_clear")

    def exit(self, *args):
        self.view.window().run_command("close_file")
