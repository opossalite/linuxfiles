import sys
import subprocess

#print("dumb cunt")
#print(sys.argv[0])

if len(sys.argv) == 1:
    print("ERROR: Please enter a subcommand: new, rm/remove, rename, list")
    exit()

subcommand = sys.argv[1]
match subcommand:
    case "new":

        # Run the command in a shell
        result = subprocess.run("ls -l | grep '.py'", capture_output=True, text=True, shell=True).stdout
        print(result)

    case "rm" | "remove":
        print(subcommand)

    case "rename":
        print(subcommand)

    case "list":
        print("Listing all existing Python virtual environments:")

    case _:
        venv = subcommand
        print("venv name: " + venv)



