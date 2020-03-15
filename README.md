# Rooaa
An application to help the blind navigate their surroundings using voice generated messages based on detected objects and their threat level

## Getting Started
- Clone the repo locally
- Install Docker and ensure it is running
    - [Docker Desktop for Mac and Windows](https://www.docker.com/products/docker-desktop)
    - [Docker Engine for Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
    - Additional step for Linux: install [docker compose](https://docs.docker.com/compose/install/#install-compose) as well.
- Download model weights by running `download_weights.sh`
- [Install Make](http://gnuwin32.sourceforge.net/packages/make.htm) if you're on Windows. OSX already has it installed. Linux will tell you how to install it (i.e., `sudo apt-get install make`)

- Run `make run` and then navigate to `https://[YOUR IPV4 ADDRESS]:5000/`
    - To get your `IPV4 Address` run `ipconfig` in cmd if you're on Windows or `ifconfig` if you're on Linux

- Click `Advanced` then `proceed to unsafe`

## Acknowledgements:
- [DenseDepth](https://github.com/ialhashim/DenseDepth)
- [YoloV3](https://pjreddie.com/darknet/yolo/) 