# Down Under
I sure hope nobody goes down on me  
## Setup
```
$ sage -pip install -r src/requirements.txt
$ cd src
$ docker compose build
```
## Generate
Generate `p`,`g`,`q`
```
$ pwd
~/WolvCtf-2023-Challenges/christheyankee/DownUnder
$ scuba generate
```
## Run
Run the challenge server
```
$ scuba run
```

## Solve
Run the solve at the same time as the challenger server
```
$ sage solv/solv.py
```
Monitor what solv spits out for `N` values like `800000` are doable. Values like `489824612411893891618223384575211313111139978607205168624702220` not so much.  
You can tune this by adjusting difficulty in `generate.py`. This will also allow for longer flag lengths.
