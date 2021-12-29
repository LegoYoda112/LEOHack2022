import coloredlogs, logging
from team_controller import TeamController

coloredlogs.install(level=logging.INFO)

logging.basicConfig(level=logging.INFO)

test_team_controller = TeamController()
test_team_controller.init()