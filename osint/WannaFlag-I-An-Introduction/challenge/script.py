import time
import sys

def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.1)

def delay_print_slow(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.5)

def delay_print_slowest(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(1)

def print_skull():
    print("                       ______")
    print("                    .-\"      \"-.")
    print("                   /            \\")
    print("       _          |              |          _")
    print("      ( \         |,  .-.  .-.  ,|         / )")
    print("       > \"=._     | )(__/  \__)( |     _.=\" <")
    print("      (_/\"=._\"=._ |/     /\     \| _.=\"_.=\"\\_)")
    print("             \"=._ (_     ^^     _)\"_.=\"")
    print("                 \"=\__|IIIIII|__/=\"\")")
    print("                _.=\"| \IIIIII/ |\"=._")
    print("      _     _.=\"_.=\"\          /\"=._\"=._     _")
    print("     ( \_.=\"_.=\"     `--------`     \"=._\"=._/ )")
    print("      > _.=\"                            \"=._ <")
    print("     (_/                                    \_)")

def print_wannaflag():
    print("██╗    ██╗ █████╗ ███╗   ██╗███╗   ██╗ █████╗ ███████╗██╗      █████╗  ██████╗ ")
    print("██║    ██║██╔══██╗████╗  ██║████╗  ██║██╔══██╗██╔════╝██║     ██╔══██╗██╔════╝ ")
    print("██║ █╗ ██║███████║██╔██╗ ██║██╔██╗ ██║███████║█████╗  ██║     ███████║██║  ███╗")
    print("██║███╗██║██╔══██║██║╚██╗██║██║╚██╗██║██╔══██║██╔══╝  ██║     ██╔══██║██║   ██║")
    print("╚███╔███╔╝██║  ██║██║ ╚████║██║ ╚████║██║  ██║██║     ███████╗██║  ██║╚██████╔╝")
    print(" ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ")

hashstr = ""
for i in range(100):
        hashstr += "#YourFlagsBelongToUs "

delay_print("Good job finding the Cube! It's a favorite destination among UofM students!\n")
time.sleep(1)
delay_print("Anyways here is the flag:\n")
delay_print_slow("wctf{")
delay_print_slowest("sp1n")
time.sleep(3)
delay_print("\nHuh???? Where did the rest of the flag g\n")
print_skull()
time.sleep(1)
print_skull()
time.sleep(1)
print_skull()
time.sleep(1)
print_wannaflag()
time.sleep(3)
delay_print("HAHAHHAHAHHAHA Ohhhhh man what an easy CTF to pwn\n\n")
delay_print("And I mean also really?? At least make a geo-osint KIND of difficult\n")
delay_print("The CTF is HOSTED by UofM where else would that dumb cube be????\n\n")
delay_print("Oh man ok well organizers if you want your \"challenge\" back or flags or whatever send 500,000 Goerli here:\n")
delay_print("0x08f5AF98610aE4B93cD0A856682E6319bF1be8a6\n\n")
delay_print("Who knows maybe we'll take more flags if you don't pay in time >:)\n")
time.sleep(2)
delay_print("#YourFlagsBelongToUs ")
for i in range(3):
    time.sleep(1)
    print(hashstr)
time.sleep(1)
print_skull()
time.sleep(1)
print_skull()
time.sleep(1)
print_skull()
time.sleep(1)
print_wannaflag()
time.sleep(1)
print_wannaflag()
time.sleep(1)
print_wannaflag()
delay_print("Also all of you John OSINTs on twitter need to leave us alone")
