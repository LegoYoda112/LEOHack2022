import coloredlogs, logging
from team_controller import TeamController, sat_msgs

coloredlogs.install(level=logging.INFO)

logging.basicConfig(level=logging.INFO)

test_team_controller = TeamController()

state = sat_msgs.SystemState()
state.state = sat_msgs.SystemState.INIT

sat_state = sat_msgs.SataliteState()

test_team_controller.handleState(state, sat_state)

state.state = sat_msgs.SystemState.RUN
test_team_controller.handleState(state, sat_state)
test_team_controller.handleState(state, sat_state)
print(test_team_controller.handleState(state, sat_state))