# Rooaa
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/khaledAIVR/Rooaa/blob/master/LICENSE)
[![Maintenance](https://img.shields.io/badge/status-experimental-green.svg)](https://github.com/Kandeel4411/Rooaa/pulse)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

An experimental web application that aims to help the blind navigate their surroundings using voice generated messages based on detected objects and their distance using only the mobile camera / web cam.  
  
## Getting Started

- Clone the repo to your local machine. 
- Install Docker and ensure it is running
    - [Docker Desktop for Mac and Windows](https://www.docker.com/products/docker-desktop)
    - [Docker Engine for Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
    - Additional step for Linux: install [docker compose](https://docs.docker.com/compose/install/#install-compose) as well.
- [Install Make](http://gnuwin32.sourceforge.net/packages/make.htm) if you're on Windows. OSX already has it installed. Linux will tell you how to install it (i.e., `sudo apt-get install make`)
- Run `make run` and then navigate to `https://[YOUR IPV4 ADDRESS]:5000/`
    - To get your `IPV4 Address` run `ipconfig` in cmd if you're on Windows or `ifconfig` if you're on Linux

- Click `Advanced` then `proceed to unsafe` The warning is because we are using a dummy SSL context in order to use `https` to be able to access the camera feed.  
*Note: Dense service has quite a high inital loading time (60 seconds) as we are currently running on the CPU but it should function normally after this*

## Demo:
- https://www.youtube.com/watch?v=59n85nJyu6g

## Acknowledgements:
- [DenseDepth](https://github.com/ialhashim/DenseDepth)
- [YoloV3](https://pjreddie.com/darknet/yolo/) 
