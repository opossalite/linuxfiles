import sys
import getpass

if len(sys.argv) != 2:
    exit()

splitted = sys.argv[1].split("/")[1:]

# replace home directory with ~
user = getpass.getuser()
if len(splitted) > 1 and splitted[0] == "home" and splitted[1] == user:
    splitted.pop(0)
    splitted[0] = "~"

# define function to shorten a folder
def shorten(string: str) -> str:
    if string.startswith("."):
        return string[:2]
    else:
        return string[:1]

# ensure the tilde doesn't get a slash
if splitted[0] == "~":
    new = "~"
    splitted.pop(0)
else:
    new = ""

# process all the folders
for i in range(len(splitted) - 1):
    new += "/" + shorten(splitted[i])

# attach the end directory as is without processing
if len(splitted) > 0:
    new += "/" + splitted[-1]

print(new)


