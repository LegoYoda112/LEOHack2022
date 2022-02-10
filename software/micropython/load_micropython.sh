#!/bin/bash

echo $1

ampy -p /dev/$1 put main.py
echo "Loaded main.py"
ampy -p /dev/$1 put motors.py
echo "Loaded motors.py"
ampy -p /dev/$1 put kinematics.py
echo "Loaded kinematics.py"

echo "Scripts now on pico are:"

ampy -p /dev/$1 ls