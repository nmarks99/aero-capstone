import os

def gen_unique_filename(default_name,extension, directory="./"):
    '''
    Generates a string "default_name.extension" if a file 
    of that name does not already exist in the directory "directory". If a file of that 
    name already exists, the generated string will be "default_name_1.extension". If that 
    already exists, the string will be "default_name_2.extension" and so on.
    '''
    contents = os.listdir(directory)
    nums = []
    f = False
    for name in contents:
        print(name)
        if default_name in name:
            f = True
            for ch in name:
                if ch.isdigit():
                    nums.append(int(ch))
            nums.sort()

    if not f:
        outfile = "".join([default_name,extension])
    else:
        if len(nums) >= 1:
            n = nums[-1]
            outfile = "".join([default_name,"_{}".format(n+1),extension])
        else:
            outfile = "".join([default_name,"_1",extension])

    return outfile


# ANSI escape codes for different colors
escapes_dict = { 
    "RESET" : "\x1B[0m",
    "RED" : "\x1B[0;31m",
    "GREEN" : "\x1B[0;32m",
    "YELLLOW" : "\x1B[0;33m",
    "BLUE" : "\x1B[0;34m",
    "MAGENTA" : "\x1B[0;35m",
    "CYAN" : "\x1B[0;36m",
    "WHITE" : "\x1B[0;37m",
    "BOLD_RED" : "\x1B[1;31m",
    "BOLD_GREEN" : "\x1B[1;32m",
    "BOLD_YELLOW" : "\x1B[1;33m",
    "BOLD_BLUE" : "\x1B[1;34m",
    "BOLD_MAGENTA" : "\x1B[1;35m",
    "BOLD_CYAN" : "\x1B[1;36m",
    "BOLD_WHITE" : "\x1B[1;37m"
}

def hline(length):
    '''
    Draws a horizontal line on the screen of the requested length
    '''
    for _ in range(length):
        print("\u2500",end="")
    else:
        print("\n")


def color_print(text, color):
    '''
    Color options are shown below:
    "RED"
    "GREEN"
    "YELLLOW"
    "BLUE"
    "MAGENTA"
    "CYAN"
    "WHITE"
    "BOLD_RED"
    "BOLD_GREEN"
    "BOLD_YELLLOW"
    "BOLD_BLUE"
    "BOLD_MAGENTA"
    "BOLD_CYAN"
    "BOLD_WHITE"
    '''
    assert(isinstance(color,str)),"color must be a string"
    assert(isinstance(text,str)), "text must be a string"
    os.system("")
    esc_code = escapes_dict[color.upper()]
    reset = escapes_dict["RESET"]
    out_str = "".join([esc_code,text,reset])
    print(out_str)

def clear():
    '''
    Clears the screen
    '''
    os.system("clear || cls")
