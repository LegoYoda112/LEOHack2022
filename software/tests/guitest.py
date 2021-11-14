import wx
import zmq

import socket as skt

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

# Subscribe
socketSUB = context.socket(zmq.SUB)
socketSUB.connect("tcp://localhost:5556")
socketSUB.setsockopt_string(zmq.SUBSCRIBE, "")

def send_zmq(message):
    socket.send_string(message)

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="hello")

        self._make_widgets()

        self.Show()

    def _make_widgets(self):
        panel = wx.Panel(self)

        box_sizer = wx.BoxSizer(wx.VERTICAL)

        ip = skt.gethostbyname(skt.gethostname())
        print(ip)

        self.ip_txt = wx.StaticText(panel, label = str(ip), style = wx.ALIGN_CENTER)
        box_sizer.Add(self.ip_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.text_ctrl = wx.TextCtrl(panel)
        box_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.test_btn = wx.Button(panel, label = "press me!", pos = (5, 55))
        self.test_btn.Bind(wx.EVT_BUTTON, self.send_msg)
        box_sizer.Add(self.test_btn, 0, wx.ALL | wx.CENTER, 5)

        self.text = wx.StaticText(panel, label = "", style = wx.ALIGN_LEFT)
        box_sizer.Add(self.text, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(box_sizer)

    
    def send_msg(self, event):
        value = self.text_ctrl.GetValue()
        print(value)
        self.text.SetLabel(str(value))
        send_zmq(value)

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()