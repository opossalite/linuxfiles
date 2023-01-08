import os
import sys
import subprocess
from typing import List, Dict

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

def apply(settings: Dict[str, str]):
    for setting in settings:
        match setting:

            case "gaps":
                lines = []
                with open(dir_path + "ricing.py", "r") as file:
                    lines = file.readlines()
                for i in range(len(lines)):
                    if "gap" in lines[i]:
                        lines[i] = "gap = " + settings["gaps"]
                with open(dir_path + "ricing.py", "w") as file:
                    file.writelines(lines)
                    
            case "corners":
                lines = []
                with open(dir_path + "../picom/picom.conf", "r") as file:
                    lines = file.readlines()
                for i in range(len(lines)):
                    if "corner-radius" in lines[i]:
                        lines[i] = f"corner-radius = {settings['corners']};\n"
                with open(dir_path + "../picom/picom.conf", "w") as file:
                    file.writelines(lines)

            case "theme":
                lines = []
                with open(dir_path + "../gtk-3.0/settings.ini", "r") as file:
                    lines = file.readlines()
                for i in range(len(lines)):
                    if "gtk-theme-name" in lines[i]:
                        lines[i] = f"gtk-theme-name={settings['theme']}\n"
                with open(dir_path + "../gtk-3.0/settings.ini", "w") as file:
                    file.writelines(lines)

            case "background":
                print('a')
                subprocess.run([f"nitrogen --set-zoom-fill --head=0 ~/Pictures/wallpapers/{settings['background']}"], shell = True)
                subprocess.run([f"nitrogen --set-zoom-fill --head=1 ~/Pictures/wallpapers/{settings['background']}"], shell = True)
                pass


def main():
    settings = dict()
    lines: List[str] = []
    
    with open(dir_path + "rice_config.txt", "r") as file: #quickly read all lines
        lines = file.readlines()
        
    first_line: str = lines[0].split() #check to see if ricing is on or off
    if len(first_line) != 3:
        print(f"Bad input, {lines[0]}")
        return
    riced: bool = first_line[2].strip() == "on" #set the actual bool
    
    reading: bool = False
    for line in lines:
        line = line.strip()
        if line == "rice_on": #found group for ricing on
            if not riced:
                continue
            reading = True
            continue
        elif line == "rice_off": #found group for ricing off
            if riced:
                continue
            reading = True
            continue
        elif line == "end": #end group
            if not reading:
                continue
            break
        elif line == "":
            continue
        
        words = line.split()
        if len(words) != 3:
            print(f"Bad input, {line}")
            return
        
        # set all the settings individually
        if words[0] in set(["gaps", "corners", "theme", "background"]):
            settings[words[0]] = words[2]
                
    print('a')
    apply(settings) 
            
            

if __name__ == "__main__":
    main()
    subprocess.run(["qtile cmd-obj -o cmd -f reload_config"], shell = True)