# Artisanal Futures Routing Service

This repository contains the necessary files to spin up a dockerized [OSRM](https://github.com/Project-OSRM/osrm-backend) backend service for Michigan.

## Setting Up

You need to have Docker installed. You can always just build the image yourself if you don't want to install Docker Compose as well.

```bash
docker-compose build
docker-compose up
```

To test, head to [http://localhost:8080/route/v1/driving/-83.7778416,42.2542447;-83.7401024,42.2787389?steps=true](http://localhost:8080/route/v1/driving/-83.7778416,42.2542447;-83.7401024,42.2787389?steps=true). If you get something back, it works.

## Notes

This is a memory hog. Roughly takes 2GB solo, just for the single state. Midwest takes 16GB in comparison. Also initial startup can take upwards of 30-40 minutes depending on your memory.
