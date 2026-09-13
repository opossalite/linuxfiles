import os
import sys
import base



match len(sys.argv):
    case 1:
        print("ERROR: Please enter a flag: -p, -w.")
        exit()
    case 2:
        print("ERROR: Please enter a GitHub link to clone.")
        exit()
    case _:
        pass

flag = sys.argv[1]
link = sys.argv[2]

match flag:
    case "-p" | "-w":
        pass
    case _:
        print("ERROR: Invalid flag: " + flag)
        exit()

if not link.startswith("git@"):
    print("ERROR: Please enter a valid GitHub SSH link.")
    exit()

#git@github.com:opossalite/plasma-keyswitcher.git

colon_loc = link.find(":")
slash_loc = link.find("/")
period_loc = link.rfind(".")

new_link = link[:colon_loc] + flag + link[colon_loc:]
repo = link[slash_loc+1:period_loc]
print("repo: " + repo)

print("Cloning...")
#base.ezrun("git clone " + link)

print("Applying configs...")
#print(base.ezrun("cd " + repo))
#os.chdir(repo)
#print(base.ezrun("gitconfig" + flag[1]))
print(base.ezrun("gitconfig" + flag[1]), repo)
print("hi")




