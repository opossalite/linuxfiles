import subprocess


def ezrun(command) -> str:
    return subprocess.run(command, capture_output=True, text=True, shell=True).stdout

def fastrun(command: list) -> str:
    return subprocess.run(command, capture_output=True, text=True).stdout

