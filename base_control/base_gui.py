import wx
import time

from base_control import BaseControl

ctl = BaseControl("Test")

class BaseFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="LEOHack Base Control")

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        border_num = 5

        defaultFlags = wx.EXPAND | wx.ALL

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # ============ GROUP 1: Sat connection

        # connection_sizer = wx.GridSizer(2, 3)

        sat_connection_sizer = wx.StaticBoxSizer(wx.VERTICAL, panel, "Sat Connection")
        grid_sizer = wx.GridBagSizer(3, 3)

        sat_ip_lab = wx.StaticText(panel, label = "IP")
        grid_sizer.Add(sat_ip_lab, flag = wx.EXPAND, pos = (0, 0))
        self.sat_ip = wx.TextCtrl(panel, value = "localhost")
        grid_sizer.Add(self.sat_ip, flag = wx.EXPAND, pos = (1, 0))

        sat_ip_lab = wx.StaticText(panel, label = "Port")
        grid_sizer.Add(sat_ip_lab, flag = wx.EXPAND, pos = (0, 1))
        self.sat_port = wx.TextCtrl(panel, value = "9000")
        grid_sizer.Add(self.sat_port, flag = wx.EXPAND, pos = (1, 1))

        self.connect_button = wx.Button(panel, label = "Connect")
        grid_sizer.Add(self.connect_button, flag = wx.EXPAND, pos = (0, 2), span = (2, 1))
        self.connect_button.Bind(wx.EVT_BUTTON, self.connect)

        self.connection_status = wx.StaticText(panel, label = "No connection")
        grid_sizer.Add(self.connection_status, flag = wx.ALL|wx.EXPAND, pos = (2, 0), span = (1, 3), border = 10)

        grid_sizer.AddGrowableCol(0)
        grid_sizer.AddGrowableCol(1)

        sat_connection_sizer.Add(grid_sizer, 0, wx.EXPAND)
        main_sizer.Add(sat_connection_sizer, 0, defaultFlags, border_num)

        # ============ GROUP 2: Control
        manual_control_sizer = wx.StaticBoxSizer(wx.VERTICAL, panel, "Manual Control")
        grid_sizer = wx.GridBagSizer(3, 3)

        self.manual_control_button = wx.Button(panel, label = "Manual Control")
        grid_sizer.Add(self.manual_control_button, flag = wx.EXPAND, pos = (0, 0), span = (2, 1))
        self.manual_control_button.Bind(wx.EVT_BUTTON, self.manual_control)

        manual_control_sizer.Add(grid_sizer, 0, wx.EXPAND)
        main_sizer.Add(manual_control_sizer, 0, defaultFlags, border_num)

        # main_sizer.Add(row_sizer, 1, wx.EXPAND)
        panel.SetSizer(main_sizer)

    def heartbeat_status(self, status):
        print(status)

        if status == False:
            self.connection_status.SetLabel("DISCONNECTED!")

    # Open a connection to the satellite
    def connect(self, event):
        ip = self.sat_ip.GetValue()
        port = int(self.sat_port.GetValue())
        status_string = "Connecting to satellite at {}:{}...".format(ip, port)
        print(status_string)

        self.connection_status.SetLabel(status_string)
        self.Update()

        # TODO: Connect
        status, sat_name = ctl.connect_sat(ip, port)

        if(status == False):
            self.connection_status.SetLabel("Failed to connect")
        else:
            self.connection_status.SetLabel("Connected to sat with ID: " + sat_name + "!")

        ctl.start_heartbeat(self.heartbeat_status)
    
    # Perform a basic manual control test
    def manual_control(self, event):
        print("Manual control test")
        ctl.send_drive()

if __name__ == "__main__":
    app = wx.App()
    frame = BaseFrame()
    app.MainLoop()