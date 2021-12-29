import coloredlogs, logging
from team_controller import TeamController, sat_msgs

coloredlogs.install(level=logging.INFO)

logging.basicConfig(level=logging.INFO)

test_team_controller = TeamController()

test_team_controller.init()
test_team_controller.run(sat_msgs.SystemState(), sat_msgs.SataliteState())
test_team_controller.run(sat_msgs.SystemState(), sat_msgs.SataliteState())
