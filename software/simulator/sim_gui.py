import wx
import time

import argparse, logging

from sim import Sim

# ===================================== ARGS
# Create arg parser
parser = argparse.ArgumentParser()

# Verbase mode!
parser.add_argument(
    '-v', '--verbose',
    help="Verbose mode",
    action='store_const', dest='loglevel', const=logging.DEBUG,
    default = logging.INFO
)
# Parse args
args = parser.parse_args()

# Create simulator object
sim = Sim(args.loglevel)

class SimFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="LEOHack Sim Control")

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.start_button = wx.Button(panel, label = "Start")
        main_sizer.Add(self.start_button, 0, wx.EXPAND, 5)
        self.start_button.Bind(wx.EVT_BUTTON, self.start)


    def start(self, event):
        sim.start()

if __name__ == "__main__":
    
    sim.start_meshcat()

    app = wx.App()
    frame = SimFrame()
    app.MainLoop()

    sim.end()
