#!/usr/bin/env python3

#
# Check out my Python calculator!
#

def validate(expression):
  if any([banned in expression for banned in [
    # my friends ran rm -rf / on my computer, so now I have to be careful
    "os",
    "system",
    "breakpoint",
    "sh",
    "vars(",
    "exec(",
    "eval(",
    "input(",
    "getattr",
    # sick and tired of vars shenanigans; no indexing!
    ".",
    "[",
    "]",
    "dict",
  ]]):
    return False
  return True

import sys

expr = input(">>> ")
if not validate(expr):
  print("no")
  sys.exit(0)

# no variables for you!
print(eval(expr, {}, {}))

# hey what does this do
print(vars())
