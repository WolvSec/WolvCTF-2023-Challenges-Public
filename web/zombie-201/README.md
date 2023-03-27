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
zombie-201   1         c275cda9f33f   10 minutes ago   275MB
```

# Run Image Locally

Assumes no process is already listening on port 80.

```
docker compose up
```

Should see something like:

```
[+] Running 1/0
 ⠿ Container zombie-201  Recreated                                                                                                                                                                                  0.1s
Attaching to zombie-201
zombie-201  | Running on 80
```
