import os
import re
import random
import platform
from concurrent.futures import ThreadPoolExecutor
from common import fastrun


# variables
HORIZONTAL_SPACING = "      " #between the logo and the cowsay
RESET_COLOR = "\x1b[0m" #ansi code; to ensure the logo color doesn't bleed into the cowsay

# regex
CURSOR_MOVEMENT_PATTERN = re.compile(r'\x1b\[[0-9;]*[^0-9;m]') #identify cursor movement codes so we can remove them
COLOR_CODE_PATTERN = re.compile(r'\x1b\[[0-9;]*m') #identify a color code to remove for string length counts
KERNEL_LINE_PATTERN = re.compile(r'((?:\x1b\[[0-9;]*m)*)Kernel')  #color codes right before the kernel line


# retrieve a random quote for cowsay to say
with open(os.path.expanduser("~/gits/linuxfiles/documents/cowsay-list.txt")) as file:
    quote = random.choice(file.read().splitlines())

# run both commands at the same time instead of one after the other
with ThreadPoolExecutor() as pool:
    fastfetch_job = pool.submit(fastrun, ["fastfetch", "--logo-color-2", "000000", "--structure", "kernel", "--pipe", "false"])
    cowsay_job = pool.submit(fastrun, ["cowsay", quote])
    fastfetch_raw, cowsay_lines = fastfetch_job.result(), cowsay_job.result().splitlines()

# the kernel line comes after the logo in the output, so split there
kernel_match = KERNEL_LINE_PATTERN.search(fastfetch_raw)
fastfetch_color = kernel_match.group(1) # type: ignore
logo_raw = CURSOR_MOVEMENT_PATTERN.sub('', fastfetch_raw[:kernel_match.start()]).rstrip() # type: ignore

#cowsay_lines = fastrun(["cowsay", quote]).splitlines()
fastfetch_logo, colorless_logo = logo_raw.splitlines(), COLOR_CODE_PATTERN.sub('', logo_raw).splitlines()
os_name = platform.freedesktop_os_release()["PRETTY_NAME"]

# make both blocks the same height by padding the cowsay, and insert os info lines
cowsay_padding = abs(len(cowsay_lines) - len(fastfetch_logo))
cowsay_lines = [""] * (len(fastfetch_logo) - len(cowsay_lines)) + cowsay_lines
cowsay_lines[cowsay_padding // 2 - 1] = fastfetch_color + "You are now using:"
cowsay_lines[cowsay_padding // 2] = os_name + "!"

logo_max_width = max(map(len, colorless_logo)) #used to make the logo uniformly wide
for logo_line, colorless_line, cowsay_line in zip(fastfetch_logo, colorless_logo, cowsay_lines):
    padding = " " * (logo_max_width - len(colorless_line))
    print(logo_line + RESET_COLOR + padding + HORIZONTAL_SPACING + cowsay_line)

print()

