# escaped

A simple pyjail! Here, we're given a program that reads in a string and prints
it back out, but utilizes a few `eval`s to very insecurely process the input.

The design around this jail was inspired by SQL injection attacks: being able to
break out of the quotes by adding in escaped quotes (`\x22`) to add in arbitrary
code execution. One possible solution is:

`"\x22,__import__('os').system('/bin/bash'),\x22"`
