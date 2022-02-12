# LEOHack 2022
This is a repository for all the code written for the LEOHack 2022 competition run by ICRS and ICSS. This contains both the code to run the actual satellites and a simulator.

## Getting set up

A Python 3 installation is required, it is suggested that you use a virtual environment to run out of. 
Python 3.8 is required, if you do not have this installed, install from: https://www.python.org/downloads/release/python-386/

Next we will install a virtual environment and required packages. Pipenv will handle this for us. Don't forget to run these commands in the LEOHack folder.
``` 
pip install pipenv
pipenv install

```
If you prefer to use a different package manager, a list of required packages is as follows: `protobuf coloredlogs numpy meshcat argparse wxpython`.

To check if everything works, spin up the simulator using `pipenv run python ./software/simulator/sim_gui.py` from the root LEOHack folder.


## Writing your first sat controller

Go into `team/first_controller.md` and take it from there!

## What's contained here
For competition participents; you will not need to worry about most of the files in this repo (anything in `hardware` or `software`) unless you are interested in looking at how some of the back end stuff works.

`hardware` contains PCB designs for the pi pico breakout boards.

`software` contains all software elements.
- `base_control` contains code to communicate between the base station and the satellite
- `low_level` can be deleted
- `micropython` contains the embedded python code that runs on the sats
- `msgs` defines protobuf messages that are used to pass information between base station and fatalities
- `sat_control` contains both the team written control code and the comms code that runs on the satellite itself
- `simulator` contains all code to run the simulator
- `tests` contains old code

`team` contains code and scripts for each team to interact with
- `team_controller.py` is where teams will write their custom control code