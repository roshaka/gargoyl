
from time import sleep

def print_titles():
    title="""\033[1;33m
 ,adPPYb,      ,adPPPYb,     ,adPPPYb,     ,adPPYb,      ,adPPYba,    88       88   88
a8"    `Y8    a8"     `Y8   a8"     `Y8   a8"    `Y8    a8"     "8a   88       88   88
8b       88   8b       88   8b       88   8b       88   8b       d8   ad       88   88
"8a,   ,d88   88a,   ,d88   88a,   ,d8,   "8a,   ,d88   "8a,   ,a8"   8b       88   88
 `"YbbdP"Y8   88"YbbdP"Y8   88"YbbdP"      `"YbbdP"Y8    `"YbbdP"'    "8a,   ,d88   88
         88   88       88   88                     88                  `"YbbdP"Y8   88
         88   88       88   88PPPPYb,              88                          88   88
         88   88       88   a8     `Y8             88                          88   88
 aa,    ,88   88       88   8b       88    aa,    ,88                  aa,    ,88   88       
  "Y8bbdP"    88       88   88       88     "Y8bbdP"    88888888888     "Y8bbdP"    888888   888 \033[00m

                                                                                  ROSHAKA © 1985
"""
    lines = title.split('\n')
    for l in lines:
        print(l)
        sleep(0.15)

def print_start_msg():
    print("""
    \033[33m                                      PRESS ENTER TO BEGIN
        \033[00m
        """)
    input('')