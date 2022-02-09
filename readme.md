# LEOHack 2022
This is a repository for all the code written for the LEOHack 2022 competiton run by ICRS and ICSS. This contains both the code to run the actual sattalites and a simulator.

## What's contained here
For competition participents; you will not need to worry about most of the files in this repo (anything in `hardware` or `software`) unless you are interested in loolking at how some of the back end stuff works.

`hardware` contains PCB designs for the pi pico breakout boards.

`software` contains all software elements.
- `base_control` contains code to communicate between the base station and the satalite
- `low_level` can be deleted
- `micropython` contains the embedded python code that runs on the sats
- `msgs` defines protobuf messages that are used to pass information between base station and satalites
- `sat_control` contains both the team written control code and the comms code that runs on the satalite itself
- `simulator` contains all code to run the simulator
- `tests` contains old code

`team` contains code and scripts for each team to interact with
- `run_sim_gui.py` runs the simulator with a gui for play/pause/reset/reload
- `run_sim_no_gui.py` runs the simulator with no gui, but still a 3d vis
- `team_controller.py` is where teams will write their custom control code

## Getting set up

A Python 3 installation is required. A set of packages are also required and can be installed by running 
```pip install -r requirements.txt``` 
in the root folder. If you prefer to use a different package manager, a list of required packages is as follows: `zmq protobuf coloredlogs numpy meshcat argparse`.

## Writing your first sat controller

Go into `team/first_controller.md` and take it from there!