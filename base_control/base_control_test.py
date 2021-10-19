from base_control import BaseControl

ctl = BaseControl("Test")

ctl.connect_sat("localhost", 9000)

def callback(status):
    print(status)

ctl.start_heartbeat(callback)