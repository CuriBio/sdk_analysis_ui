#!/usr/bin/python
import wx
import sys
import os
import logging
import locale
import numpy as np
from threading import Thread

import logging
#logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

from pulse3D.plate_recording import PlateRecording
from pulse3D.excel_writer import write_xlsx

logger = logging.getLogger()
locale.getlocale = lambda _: 'en-us' #windows locales are different

wx.USE_FILEPICKERCTRL = 1

def analyze(input_path, output_path, start_time, end_time):
    recordings = PlateRecording.from_directory(input_path)

    for r in recordings:
        write_xlsx(r, name=output_path, start_time=start_time, end_time=end_time)


class WxTextCtrlHandler(logging.Handler):
    def __init__(self, ctrl):
        logging.Handler.__init__(self)
        self.ctrl = ctrl

    def emit(self, record):
        s = self.format(record) + '\n'
        print(s)
        wx.CallAfter(self.ctrl.WriteText, s)


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1200, 300))
        self.panel = wx.Panel(self, -1)
        
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.panel, 0)

        input_prompt = wx.StaticText(self.panel, -1, "Input directory:", pos=wx.Point(10, 10))
        self.dir_sel = wx.DirPickerCtrl(self.panel, size=(280,30), pos=(10, 25))
        self.dir_sel.SetInitialDirectory('/Users//kristianeschenburg/Downloads/MA20211223__2021_12_23_204133_d7_UYX-001-S1_opt-run1-rerun_001')
        self.box.Add(self.dir_sel, 1, wx.ALL | wx.EXPAND, 5)

        output_prompt = wx.StaticText(self.panel, -1, "Output file:", pos=wx.Point(10, 60))
        self.out_file_sel = wx.FilePickerCtrl(self.panel, size=(280,30), pos=(10, 75))
        self.box.Add(self.out_file_sel, 1, wx.ALL | wx.EXPAND, 5)

        start_prompt = wx.StaticText(self.panel, -1, "Start time (sec):", pos=wx.Point(10, 140))
        self.start_time = wx.TextCtrl(self.panel, -1, 
                                 value="",
                                 pos=wx.Point(10, 160),
                                 size=wx.Size(65, 23))

        end_prompt = wx.StaticText(self.panel, -1, "End time (sec):", pos=wx.Point(10, 190))
        self.end_time = wx.TextCtrl(self.panel, -1, 
                                 value="",
                                 pos=wx.Point(10, 210),
                                 size=wx.Size(65, 23))

        self.run_button = wx.Button(self.panel, -1, 
                                 label="Run",
                                 pos=wx.Point(10, 245), 
                                 size=wx.Size(175, 30))

        # Respond to button click event
        self.run_button.Bind(wx.EVT_BUTTON, self.run, self.run_button)

        # panel.SetSizer(box)
        self.Show()

    def run(self, event):
        """
        Conversion button has been clicked.
        """

        input_path = self.dir_sel.GetPath()
        
        output_path = self.out_file_sel.GetPath()
        if output_path == "":
            output_path = None

        start_time=self.start_time.GetValue()
        end_time=self.end_time.GetValue()

        if start_time=="":
            start_time=0
        if end_time=="":
            end_time=np.inf

        try:
            start_time=float(start_time)
        except Exception as e:
            raise(ValueError)

        try:
            end_time=float(end_time)
        except Exception as e:
            raise(ValueError)

        panel2 = wx.Panel(self.panel, -1, style=wx.RAISED_BORDER, size=(800, 300), pos = (300,0))
        self.box.Add(panel2, 0)

        style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL
        log = wx.TextCtrl(panel2, wx.ID_ANY, size=(800,300), style=style)

        handler = WxTextCtrlHandler(log)
        FORMAT = "%(asctime)s %(levelname)s %(message)s"
        handler.setFormatter(logging.Formatter(FORMAT))
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        if input_path:
            t = Thread(target=analyze, args=(input_path, output_path, start_time, end_time))
            t.start()

class MyApp(wx.App):
     def OnInit(self):
         frame = MainFrame(None, -1, 'Pulse3D')
         frame.Show(True)
         return True

if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()