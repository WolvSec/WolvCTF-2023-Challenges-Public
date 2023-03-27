# Solve

- Find redacted password list jpg in documents
- Figure original file is lost somewhere in unallocated space from deleting
- Looking for an exact copy yields no results
- However, looking for similar strings between the files (incase the unallocated file was overwritten) yields results. For example, `grep -r !Adobe` states that `Binary file 01994768/06149412 matches` in unallocated space
- As hinted by the challenge description "we really need to *carve* up an idea up here" we can use file carving to carve out the jpg. [Example](https://www.youtube.com/watch?v=MbZkMJsT2TM)
- Find the start of the jpg hex by looking for identical hex between the unallocated image and the redacted image in documents
- Exract hex until you reach the jpg footer (there are trailing 0s in hex to make this more obvious where the file ends)
- Append the hex from the redacted file to the carved file, up until where the hex is identical
- Save as jpg
- Open jpg and get the flag


`wctf{n0_w4y_dUd3_1_g0t_th3_fl4g_3Nd1Ng}`

## Writeups:
- Author Writeup - Coming Soon
nighthex#5712's discord msg (only solve):
> I was sure the way I solved 428 wasn't intended lol, I spent a while chasing down anything related to the github link, but in the end tried some good old hex bruteforcing
since I had the redacted jpeg, I figured that the first few rows of the redacted image would be identical to the non-redacted one, so I searched for similar hex strings in  all files and found one in an unallocated space chunk, pasted that after the redacted jpeg header and it was the full image

Note: This is the intended solution :)