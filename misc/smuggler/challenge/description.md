# smuggler

This challenge was inspired by an imaginaryCTF challenge called "gaas" utilizing
a similar concept (exfiltrating files through gcc). The solution there involved
utilizing `#include` and newlines to get the output in a compiler error. My
solution, however, ended up utilizing an assembly include directive. Thus,
`smuggler` was born, where I restricted `#include` to force this other solution.
