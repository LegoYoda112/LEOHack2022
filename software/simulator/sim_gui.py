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

# Verbase mode!
parser.add_argument(
    '--challenge', action="store", type=int, default=1
)

# Parse args
args = parser.parse_args()

print(args.challenge)

# Create simulator object
sim = Sim(args.loglevel, args.challenge)

class SimFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="LEOHack Sim Control")

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)


        # ===================================== SIM CONTROL BUTTONS
        self.start_button = wx.Button(panel, label = "Start")
        main_sizer.Add(self.start_button, 1, wx.EXPAND)
        self.start_button.Bind(wx.EVT_BUTTON, self.start)

        play_pause_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.play_button = wx.Button(panel, label = "Play")
        play_pause_sizer.Add(self.play_button, 1, wx.EXPAND)
        self.play_button.Bind(wx.EVT_BUTTON, self.play)

        self.pause_button = wx.Button(panel, label = "Pause")
        play_pause_sizer.Add(self.pause_button, 1, wx.EXPAND)
        self.pause_button.Bind(wx.EVT_BUTTON, self.pause)

        self.reset_button = wx.Button(panel, label = "Reset")
        play_pause_sizer.Add(self.reset_button, 1, wx.EXPAND)
        self.reset_button.Bind(wx.EVT_BUTTON, self.reset)

        main_sizer.Add(play_pause_sizer, 1, wx.EXPAND)

        self.reload_button = wx.Button(panel, label = "Reload Controller and Reset")
        main_sizer.Add(self.reload_button, 0, wx.EXPAND)
        self.reload_button.Bind(wx.EVT_BUTTON, self.reload)

        panel.SetSizer(main_sizer)

        self.play_button.Disable()
        self.pause_button.Disable()
        self.reset_button.Disable()
        self.reload_button.Disable()


    def start(self, event):
        sim.start()

        self.play_button.Disable()
        self.pause_button.Enable()
        self.reset_button.Enable()

        self.start_button.Disable()
        self.reload_button.Enable()

    def pause(self, event):
        sim.pause()

        self.play_button.Enable()
        self.pause_button.Disable()

    def play(self, event):
        sim.play()

        self.play_button.Disable()
        self.pause_button.Enable()

    def reset(self, event):
        sim.reset()

        self.play_button.Enable()
        self.pause_button.Disable()

    def reload(self, event):
        sim.reload()

        self.play_button.Enable()
        self.pause_button.Disable()

if __name__ == "__main__":
    
    sim.start_meshcat()

    app = wx.App()
    frame = SimFrame()
    app.MainLoop()

    sim.end()
