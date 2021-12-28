from base_control import BaseControl

ctl = BaseControl("Remote")

# Connect to satalite
# ctl.connect_sat("192.168.51.11", 9000)
ctl.connect_sat("localhost", 9000)

# Status callback
def callback(status):
    print(status)

# Start heartbeat with status callback
ctl.start_heartbeat(callback)

# Import pygame
import pygame
pygame.init()

# Define deadzone function
def deadzone(value, deadzone):
    if(abs(value) < deadzone):
        return 0
    return value

 # Main!
def main():
    axis0 = 0
    axis1 = 0
    axis2 = 0
    axis3 = 0

    # Start pygame to recive joystick values
    pygame.display.set_caption('JoyStick Example')
    surface = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True
    

    font = pygame.font.Font(None, 20)
    linesize = font.get_linesize()

    # Get joysticks and start them
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joy in joysticks:
        joy.init()
    
    # Main loop
    while running:

        # Get events and update axis values
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                #print("reading axis")
                axis0 = deadzone(joysticks[0].get_axis(0), 0.05)
                axis1 = deadzone(joysticks[0].get_axis(1), 0.05)
                axis2 = deadzone(joysticks[0].get_axis(2), 0.05)
                axis3 = deadzone(joysticks[0].get_axis(3), 0.05)
        
        # Print out axis
        print(axis0, axis1, axis2, axis3)

        # Send axis values to satalite
        # ctl.send_drive((round(-axis2 * 60, 2),
        #                 round(axis1 * 60, 2),
        #                 round(-axis0 / 0.5, 2)))

        ctl.send_drive((round(-axis0 * 60, 2),
                         round(axis1 * 60, 2),
                         round(-axis1 / 0.5, 2)))


        surface.fill((0,0,0))

        pygame.display.flip()

        # Run at 15 fps max
        clock.tick(15)
 
    pygame.quit()
    writeTwist(0, 0, 0)
 
# Start loop
main()