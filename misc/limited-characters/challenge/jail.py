import string

allowed = set("1<rjhniocd()_'[]+yremlsp,. ")

code = input("Enter your code:\n>>> ")

if set(code) != allowed:
    raise Exception("No no no! Only: \"1<rjhniocd()_'[]+yremlsp,. \" allowed")

exec(eval(code))