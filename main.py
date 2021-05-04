#!/usr/bin/python
import wx
import sys
import os
import logging
import locale
from threading import Thread

from curibio.sdk import PlateRecording

logger = logging.getLogger()
locale.getlocale = lambda _: 'en-us' #windows locales are different

def analyze(path):
    r = PlateRecording.from_directory(path)
    r.write_xlsx(path)


class WxTextCtrlHandler(logging.Handler):
    def __init__(self, ctrl):
        logging.Handler.__init__(self)
        self.ctrl = ctrl

    def emit(self, record):
        s = self.format(record) + '\n'
        print(s)
        wx.CallAfter(self.ctrl.WriteText, s)


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='curibio.sdk')
        self.analysis_running = False

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        self.dir_sel = wx.DirPickerCtrl(panel)
        self.dir_sel.SetInitialDirectory('/Users/jason')
        self.dir_sel.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_dir_select)
        box.Add(self.dir_sel, 0, wx.ALL | wx.EXPAND, 5)

        style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL
        log = wx.TextCtrl(panel, wx.ID_ANY, size=(300,100), style=style)
        box.Add(log, 1, wx.ALL|wx.EXPAND, 5)

        handler = WxTextCtrlHandler(log)
        FORMAT = "%(asctime)s %(levelname)s %(message)s"
        handler.setFormatter(logging.Formatter(FORMAT))
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        panel.SetSizer(box)
        self.Show()

    def on_dir_select(self, event):
        path = self.dir_sel.GetPath()
        if path:
            t = Thread(target=analyze, args=(path,))
            t.start()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()

