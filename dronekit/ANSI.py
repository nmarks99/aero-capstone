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
    "BOLD_YELLLOW" : "\x1B[1;33m",
    "BOLD_BLUE" : "\x1B[1;34m",
    "BOLD_MAGENTA" : "\x1B[1;35m",
    "BOLD_CYAN" : "\x1B[1;36m",
    "BOLD_WHITE" : "\x1B[1;37m"
}

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

    esc_code = escapes_dict[color.upper()]
    reset = escapes_dict["RESET"]
    out_str = "".join([esc_code,text,reset])
    print(out_str)
