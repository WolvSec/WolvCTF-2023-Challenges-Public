# pyjail

A pyjail challenge! A lot of things are banned, but there's still many ways to
solve it! Unicode `breakpoint` was one of my favorites. The original intended
solution revolved around utilizing a tuple and overwriting both `print` and
`vars` to `exec` and `input` respectively, allowing any input to be executed.
