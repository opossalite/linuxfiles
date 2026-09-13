import subprocess



def ezrun(command: str, cwd: str | None = None) -> str:
    return subprocess.run(command, capture_output=True, text=True, shell=True, cwd=cwd).stdout

