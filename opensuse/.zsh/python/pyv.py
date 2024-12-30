import sys

#print("dumb cunt")
#print(sys.argv[0])

if len(sys.argv) == 1:
    print("Please enter a subcommand: new, rm/remove, rename, list")

subcommand = sys.argv[1]

match subcommand:
    case "new":
        print(subcommand)
        pass

    case "rm" | "remove":
        print(subcommand)

    case _:
        print("fake")



