import os
import subprocess


class CommandRunner():
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def run(self, string, stdin=None):
        string = "source ~/.zshrc && " + string
        command = ("zsh", "-l", "-c", string)
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        env = os.environ
        # env["TERM"] = "xterm-256color"
        # env["TERM"] = "xterm"

        p = subprocess.Popen(command,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             cwd=self.working_dir,
                             env=env,
                             startupinfo=startupinfo)
        stdout, stderr = p.communicate(stdin.encode(encoding="UTF-8") if stdin else None)
        stdout, stderr = stdout.decode(), stderr.decode()

        return stdout, stderr

