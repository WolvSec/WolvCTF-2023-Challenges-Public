# Build

```
docker compose build
```

# Confirm Docker Image

```
docker images
```

Should see something like:

```
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
zombie-301   1         5cf8c6e124a9   6 minutes ago    275MB
```

# Run Image Locally

Assumes no process is already listening on port 80.

```
docker compose up
```

Should see something like:

```
[+] Running 1/0
 ⠿ Container zombie-301  Recreated                                                                                                                                                                                  0.1s
Attaching to zombie-301
zombie-301  | Running on 80
```
