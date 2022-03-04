# Rotor Powered Rocket Lander

## Goal
The team will develop a landing system capable of landing a small rocket vertically at a designated target zone, without the use of traditional combustion engines.
The product will function completely autonomously from the start of its descent (more than 10 meters but less than 50 meters) until stable landing on the landing 
pad. The device will also adhere to typical guidelines and mission goals set by the NASA Student Launch competition in order to benefit future NUSTARS (Northwestern 
University Space Technology and Rocketry Society) competition teams. Finally, the product will be designed using concepts and methods which allow for modularity 
between rockets of different scales.

## Useage
Most of the code in this repo is intended to run on the Raspberry Pi 4 flight computer, so it is hardware independent. To download the code on the Raspberry Pi, 
if you are on a secure network (Northwestern Guest is apparently not secure) clone the repo with HTTPS as follows
```
git clone https://github.com/nmarks99/aero-capstone.git
```
If you are on Northwestern Guest or something similar you may need to clone the repo with SSH if you want the ability to be able push to the remote repo. To do 
this run the following command. You will need to have generated an SSH key already.
```
git clone git@github.com:nmarks99/aero-capstone.git
```
