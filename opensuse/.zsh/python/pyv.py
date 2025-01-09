import sys
import subprocess

#print("dumb cunt")
#print(sys.argv[0])



def ezrun(command) -> str:
    return subprocess.run(command, capture_output=True, text=True, shell=True).stdout




if len(sys.argv) == 1:
    print("ERROR: Please enter a subcommand: new, rm/remove, rename, list.")
    exit()

subcommand = sys.argv[1]
match subcommand:
    case "new":
        if len(sys.argv) != 3:
            print("ERROR: Invalid arguments. Please enter a name for the virtual environment.")
            exit()

        name = sys.argv[2]
        contents = ezrun("ls -a ~/.pyv").splitlines()[2:]

        if name in contents:
            print(f"ERROR: Virtual environment named \"{name}\" already exists!")
            exit()

        ezrun("cd ~/.pyv && python3 -m venv " + name)
        print("Virtual environment created successfully.")


    case "rm" | "remove":
        if len(sys.argv) != 3:
            print("ERROR: Invalid arguments. Please enter the name of a virtual environment.")
            exit()

        name = sys.argv[2]
        contents = ezrun("ls -a ~/.pyv").splitlines()[2:]

        if name not in contents:
            print(f"ERROR: Virtual environment named \"{name}\" doesn't exist!")
            exit()

        result = ezrun("cd ~/.pyv && trash " + name)
        if result.startswith("trash"):
            print(result)
        elif result == "":
            print("Virtual environment successfully removed.")
        else:
            print("ERROR: trash-cli not installed, required for removing virtual environments.")


    case "mv" | "rename" | "move":
        if len(sys.argv) != 4:
            print("ERROR: Invalid arguments. Please enter the old and new name of a virtual environment.")
            exit()

        name_old = sys.argv[2]
        name_new = sys.argv[3]
        contents = ezrun("ls -a ~/.pyv").splitlines()[2:]

        if name_old not in contents:
            print(f"ERROR: Virtual environment named \"{name_old}\" doesn't exist!")
            exit()

        if name_new in contents:
            print(f"ERROR: Another virtual environment named \"{name_new}\" already exists!")
            exit()

        ezrun("cd ~/.pyv && mv " + name_old + " " + name_new)


    case "ls" | "list":
        contents = ezrun("ls -a ~/.pyv").splitlines()[2:]

        if len(contents) == 0:
            print("No virtual environments exist.")
            exit()

        for item in contents:
            print(item)


    case "da" | "deactivate":
        #print("Deactivating virtual environment if active.")
        ezrun("deactivate")


    case _:
        if subcommand == "enter":
            if len(sys.argv) != 3:
                print("ERROR: Invalid arguments. Please enter the name of a virtual environment.")
                exit()

            name = sys.argv[2]
        else:
            name = subcommand

        contents = ezrun("ls -a ~/.pyv").splitlines()[2:]

        if name not in contents:
            print(f"ERROR: Virtual environment named \"{name}\" doesn't exist!")
            exit()

        import os
        #os.system("/bin/bash --rcfile ~/.pyv/" + name + "/bin/activate")

        #os.system("/bin/zsh -c ~/.pyv/" + name + "/bin/activate")
        #os.execvp(f'/bin/zsh --rcs -i -c "source ~/.pyv/{name}/bin/activate" && exec zsh')
        os.execvp("/bin/zsh", ["/bin/zsh", "--rcs", "-i", "-c", f"source ~/.pyv/{name}/bin/activate && exec zsh"])
        #os.system('/bin/bash --rcfile flask/bin/activate')
        #print(command)
        #ezrun(command)



