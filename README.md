# ROV ROS Backend

## Description
- ROS backend for the ROV robot developed by (Zewail City ROV 23) software engineering team.

## How to Run
```
1- configure your network then write its IPs in the settings.json and docker-compose.yml files
2- python ros_lauch.py
```

## Required Dependencies
```
python3.10+
docker
rospy
pydantic
```

## Provided Libraries
- settings.py: parses the settings.json file into a python runtime object
- serial_driver.py: provides reliable serial communication API
- log.py: logging manager for easier debugging
- ros.py: helps integrating your node with the entire ROS backend