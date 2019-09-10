# #!/usr/bin/env python
# used with windows and Linux - not defined python environment - python version 2.7.12
#
# Copyright (C) Shashank N D All rights reserved.
#
# This document contains proprietary information belonging to Author.
# Passing on and copying of this document, use and communication of its
# contents is not permitted without prior written authorization.
#
# HM_Dictionary.
#
# This module is used to create and search in dictionary.

import wx
import sys
import os
import time
import datetime
import threading
import random
import hashlib
import re
from collections import OrderedDict


__version__ = '0.1'
__author__ = 'Shashank Devaraj'
__copyright__ = __author__
__date__ = '07th September 2018'

# define variables
iconpath = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'HMD.ico'

# config file
config_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'sys.cfg'

# previous words file
prvwrds_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'prv.wrds'

# default paths
selfpath = os.path.dirname(os.path.abspath(__file__)) + os.sep

# temp variables
temp = None
tcmd = None
dial = None

# globals
prvhash = ""
prvsep = ""
gspes = [',', ':', '|', '"']
hmddict = {}
prvwrds = []


class RandError(Exception):
    pass


class HMDGUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(HMDGUI, self).__init__(*args, **kwargs)

        # constructors
        self.statusbar = None
        self.settin = None
        self.tc1 = None
        self.tc2 = None
        self.tc3 = None
        self.tc4 = None
        self.tc5 = None
        self.combo = None
        self.helpcontents = None
        self.stopthread = None
        self.abortrun = False
        self.runcomplete = False

        # create gui
        self.initgui()

    def initgui(self):
        global gspes, prvwrds

        # define icon for the app
        icon = wx.Icon(iconpath, wx.BITMAP_TYPE_ICO)

        # icon.CopyFromBitmap(wx.Bitmap(iconpath, wx.BITMAP_TYPE_ICO))
        self.SetIcon(icon)

        # define panels
        panel = wx.Panel(self)

        # define fonts
        font = wx.Font(13, wx.MODERN, wx.NORMAL, wx.BOLD)
        efont = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL)
        bfont = wx.Font(5, wx.MODERN, wx.NORMAL, wx.NORMAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetBackgroundColour((217, 217, 217))

        # define size and title
        self.SetSize((850, 600))
        self.SetTitle('HMD')
        self.Centre()

        # bring title slightly below
        vbox.Add((-1, 9))

        # box title and define name align center with color
        lbl = wx.StaticText(panel, -1, style=wx.ALIGN_CENTER)
        lfont = wx.Font(21, wx.MODERN, wx.NORMAL, wx.BOLD)
        lbl.SetFont(lfont)
        lbl.SetLabel("Happiest Minds Dictionary")
        vbox.Add(lbl, 0, wx.ALIGN_CENTER)
        lbl.SetForegroundColour((51, 181, 67))

        # Add space at top
        vbox.Add((-1, 25))

        # define input file path box
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Input File path ')
        st1.SetFont(font)
        hbox1.Add(st1)
        self.tc1 = wx.TextCtrl(panel)
        self.tc1.SetFont(efont)
        hbox1.Add(self.tc1, proportion=1)

        # define folder dialog button
        st2_btn0 = wx.Button(panel, label='', size=(30, 20))
        st2_btn0.SetFont(bfont)
        hbox1.Add(st2_btn0, flag=wx.LEFT, border=20)

        # add spaces around
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # space at top
        vbox.Add((-1, 45))

        # define sepertors box
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(panel, label='Seperators  ')
        st3.SetFont(font)
        hbox2.Add(st3, flag=wx.RIGHT, border=8)
        self.tc2 = wx.TextCtrl(panel)
        self.tc2.SetFont(efont)
        hbox2.Add(self.tc2, proportion=1)

        # combo for seperators
        self.combo = wx.ComboBox(panel, choices=gspes, size=(40, 40))
        self.combo.SetFont(efont)
        hbox2.Add(self.combo, flag=wx.LEFT, border=10)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # space at top
        vbox.Add((-1, 25))

        # define search word box
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(panel, label='Search Word ')
        st4.SetFont(font)
        hbox3.Add(st4, flag=wx.RIGHT, border=8)

        # combo for previous words
        self.tc3 = wx.ComboBox(panel, choices=prvwrds, size=(40, 40), style=wx.TE_PROCESS_ENTER)
        self.tc3.SetFont(efont)
        hbox3.Add(self.tc3, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # space at top
        vbox.Add((-1, 25))

        # define at output - word meaning box
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        st5 = wx.StaticText(panel, label='Word Found')
        st5.SetFont(font)
        hbox4.Add(st5, flag=wx.RIGHT, border=8)
        self.tc4 = wx.TextCtrl(panel)
        self.tc4.SetFont(efont)
        hbox4.Add(self.tc4, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # space at top
        vbox.Add((-1, 25))

        # space at top
        vbox.Add((-1, 25))

        # search and abort
        bfont = wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='SEARCH', size=(70, 30))
        btn1.SetFont(bfont)
        hbox5.Add(btn1, proportion=1)
        btn2 = wx.Button(panel, label='ABORT', size=(70, 30))
        btn2.SetFont(bfont)
        hbox5.Add(btn2, proportion=1, flag=wx.LEFT | wx.BOTTOM, border=10)
        vbox.Add(hbox5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # bind with events
        self.Bind(wx.EVT_BUTTON, self.runthread, btn1)
        self.Bind(wx.EVT_BUTTON, self.abort, btn2)
        self.Bind(wx.EVT_BUTTON, self.loadfile, st2_btn0)
        self.combo.Bind(wx.EVT_COMBOBOX, self.comboselect)
        self.tc2.Bind(wx.EVT_TEXT, self.showwarn)
        self.tc3.Bind(wx.EVT_TEXT_ENTER, self.runthread)

        # space at top
        vbox.Add((-1, 20))

        # log box
        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc5 = wx.TextCtrl(panel, style=style)
        self.tc5.SetFont(efont)
        hbox6.Add(self.tc5, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox6, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)

        # configure all system output to log box
        sys.stdout = self.tc5

        # space at bottom
        vbox.Add((-1, 10))

        # auto adjust
        panel.SetSizer(vbox)

        # define menu bars
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        helpmenu = wx.Menu()
        self.settin = wx.Menu()

        # create sub menu's
        clr = wx.MenuItem(filemenu, wx.ID_ANY, '&Clear\tCtrl+R', 'Clear the contents')
        qmi = wx.MenuItem(filemenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
        hmu = wx.MenuItem(helpmenu, wx.ID_HELP, '&Help', 'Help contents')
        habu = wx.MenuItem(helpmenu, wx.ID_ANY, '&About', 'Version of the tool')
        savecfg = wx.MenuItem(self.settin, wx.ID_ANY, '&Save Configuration\tCtrl+S',
                              'Save the current configurations to load next time')
        savelog = wx.MenuItem(self.settin, wx.ID_ANY, '&Save Log\tCtrl+L', 'Save the current log to a file')

        # Add sub menu's to main menu's
        filemenu.AppendSeparator()
        filemenu.Append(clr)
        filemenu.Append(qmi)
        helpmenu.Append(hmu)
        helpmenu.Append(habu)
        self.settin.Append(savecfg)
        self.settin.Append(savelog)

        # add event for sub menu's if any
        self.Bind(wx.EVT_MENU, self.helpapp, hmu)
        self.Bind(wx.EVT_MENU, self.helpabout, habu)
        self.Bind(wx.EVT_MENU, self.onclose, qmi)
        self.Bind(wx.EVT_MENU, self.clearall, clr)
        self.Bind(wx.EVT_MENU, self.showmessage1, savecfg)
        self.Bind(wx.EVT_MENU, self.showmessage7, savelog)
        self.Bind(wx.EVT_CLOSE, self.onclose)

        # Define the menu bar, name and append all to the menu
        menubar.Append(filemenu, '&File')
        menubar.Append(self.settin, '&Settings')
        menubar.Append(helpmenu, '&Help')
        self.SetMenuBar(menubar)

        # define status bar
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        # load previous configuration if exists
        self.loadconfigu()

        # gui aest
        self.progressbar("Loading Configuration,.......", 100)

        # validate root files
        self.rootfiles()

    def showwarn(self, event):
        self.statusbar.SetStatusText("Warning: Use combobox. All the delimeters should be seperated by commas")

    def comboselect(self, event):
        if self.tc2.GetValue() == "":
            self.tc2.ChangeValue(self.combo.GetValue())
        else:
            self.tc2.ChangeValue(self.tc2.GetValue() + ',' + self.combo.GetValue())

    def rootfiles(self):
        global dial
        self.helpcontents = False
        rp = os.path.dirname(os.path.abspath(__file__)) + os.sep
        ap = [rp + 'HMD.ico']
        for p in ap:
            if not os.path.exists(p):
                dial = wx.MessageDialog(None, 'Root files does not exists!!!, need fresh installation', 'Error',
                                        wx.OK | wx.ICON_ERROR)
                dial.ShowModal()
                sys.exit(-1)

    def progressbar(self, guimessage, guirange):
        progress = wx.ProgressDialog("HMD", guimessage, maximum=100, parent=self, style=wx.PD_SMOOTH | wx.PD_AUTO_HIDE)
        self.processsents()
        for i in range(guirange):
            progress.Update(i)
            time.sleep(0.001)
        progress.Destroy()

    def processsents(self):
        self.helpcontents = False
        wx.Yield()

    def onclose(self, e):
        global prvwrds
        # save previous words if available
        try:
            if os.path.exists(prvwrds_file):
                os.remove(prvwrds_file)
        except IOError:
            print "Exception in creating previous words file"
            self.Destroy()

        tf = open(prvwrds_file, 'w')
        for wrd in prvwrds:
            tf.write(wrd + '\n')

        # Close or Destroy
        self.Destroy()

    def clearall(self, e):
        self.tc1.ChangeValue('')
        self.tc2.ChangeValue('')
        self.tc3.ChangeValue('')
        self.tc4.ChangeValue('')
        self.tc5.ChangeValue('')
        print "Cleared!!!"

    def saveconfigu(self):
        # Save current configuration
        if self.tc1.GetValue() or self.tc2.GetValue() or self.tc3.GetValue() or self.tc4.GetValue():
            if os.path.exists(config_file):
                os.remove(config_file)
            f = open(config_file, 'w')
            f.write(self.tc1.GetValue())
            f.write('\n' + self.tc2.GetValue())
            f.write('\n' + self.tc3.GetValue())
            f.write('\n' + self.tc4.GetValue())
            f.close()
            print "Saved current configuration!!!"
            return True
        else:
            if os.path.exists(config_file):
                os.remove(config_file)
            print "Empty configuration!!!"
            return False

    def savelog(self):
        global dial
        tn = time.time()
        dts = datetime.datetime.fromtimestamp(tn).strftime('%Y_%m_%d_%H_%M_%S')
        try:
            lfile = open(selfpath + dts + ".txt", 'w')
            lfile.write(self.tc5.GetValue())
            lfile.close()
            print "Created a log file %s" % (selfpath + dts + ".txt")
            return True
        except IOError:
            print "Error in creating a log file"
            return False

    def loadconfigu(self):
        global prvwrds
        # load the configuration file
        temprwrd = ""
        if os.path.exists(config_file):
            path_lines = [pline.rstrip('\n') for pline in open(config_file)]
            try:
                self.tc1.ChangeValue(path_lines[0])
                self.tc2.ChangeValue(path_lines[1])
                self.tc3.ChangeValue(path_lines[2])
                temprwrd = path_lines[2]
                self.tc4.ChangeValue(path_lines[3])
            except IndexError:
                pass
            open(config_file).close()
            print "Previous configuration loaded"
        else:
            print "No configuration saved"
        # load previous words if available
        if os.path.exists(prvwrds_file):
            path_lines = [pline.rstrip('\n') for pline in open(prvwrds_file)][:-1]
            try:
                for w in range(len(path_lines)):
                    prvwrds.append(path_lines[w])
                    if w > 9:
                        break
                for wrd in prvwrds:
                    self.tc3.Append(wrd)
                self.tc3.ChangeValue(temprwrd)
            except IndexError:
                pass
            open(prvwrds_file).close()
            print "Previous words loaded"
        else:
            print "No previous words saved"

    def validateinputs(self):
        print "Validating inputs"
        if not (self.tc1.GetValue() and self.tc2.GetValue() and self.tc3.GetValue()):
            self.showmessage2()
            return False
        else:
            return True

    def helpapp(self, e):
        global dial
        self.helpcontents = True
        print "Show help contents:%s" % self.helpcontents
        help_contents = "HMD: Happiest Minds Dictionary \n" \
                        "How to run: \n1. Fill the input file path, should be in the text format\n" \
                        "2. Enter the separtors between the words in the text file seperated by comma's."\
                        " Example: ;,/, ,,,,\n" \
                        "3. Enter the search word\n" \
                        "4. Hit search to get the output\n"\
                        "Default Delimeters:\\n nextline \\s space \\r carriage return \\| Dot\\. \n"\
                        "***In cases of any concerns, mail us @ abcd@hmd.com***"
        dial = wx.MessageDialog(None, help_contents, 'Info', wx.OK)
        dial.ShowModal()

    def helpabout(self, e):
        self.showmessage3()
        print 'HMD Version 0.1'

    def showmessage1(self, e):
        global dial
        if self.saveconfigu():
            dial = wx.MessageDialog(None, 'Configuration saved', 'Info', wx.OK)
        else:
            dial = wx.MessageDialog(None, 'Empty configuration!!!', 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()

    def showmessage2(self):
        global dial
        self.helpcontents = False
        dial = wx.MessageDialog(None, 'Please provide all the inputs!!!', 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()

    def showmessage3(self):
        global dial
        self.helpcontents = False
        dial = wx.MessageDialog(None, 'HMD Version 0.1', 'Info', wx.OK)
        dial.ShowModal()

    def showmessage5(self):
        global dial
        self.helpcontents = False
        dial = wx.MessageDialog(None, 'Aborting process!!!', 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        print '!' * 64 + "\n" + "Aborting Process" + "\n" + '!' * 64 + '\n'

    def showmessage6(self):
        global dial
        self.helpcontents = False
        dial = wx.MessageDialog(None, 'HMD Search Failed!!!', 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        print '!' * 64 + "\n" + "HMD Search Failed" + "\n" + '!' * 64 + '\n'

    def showmessage7(self, e):
        global dial
        if self.savelog():
            dial = wx.MessageDialog(None, 'Log saved', 'Info', wx.OK)
        else:
            dial = wx.MessageDialog(None, 'Cannot save log!!!', 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()

    def abort(self, e):
        self.abortrun = True
        self.runcomplete = True

    def loadfile(self, event):
        # create file window for ease
        with wx.FileDialog(self, "Load text file", wildcard="Text files (*.txt)|*.txt", style=wx.FD_OPEN) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                # the user changed their mind
                return

            # save the current contents in the file
            self.tc1.ChangeValue(fileDialog.GetPath())
            print(self.tc1.GetValue())

    def runthread(self, e):
        print "Run:Start@ %s" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S')
        self.runcomplete = False
        runt = threading.Thread(target=self.run)
        runt.daemon = True
        runt.start()
        prct = threading.Thread(target=self.processingthread)
        prct.daemon = True
        prct.start()
        while True:
            wx.Yield()
            time.sleep(0.001)
            if self.runcomplete:
                print "Exit yield"
                self.statusbar.SetStatusText('Ready')
                time.sleep(0.5)
                wx.Yield()
                return True

    def processingthread(self):
        rn = random.randint(0, 2)
        symbls1 = ['/', '-', '\\', '|', '/', '-', '\\', '|']
        symbls2 = ['.', '..', '...', '....', '.....', '......', '........', '.........']
        symbls3 = ['[' + '#' * 1 + ' ' * 8 + ']', '[' + '#' * 2 + ' ' * 7 + ']', '[' + '#' * 3 + ' ' * 6 + ']', '[' +
                   '#' * 4 + ' ' * 5 + ']', '[' + '#' * 5 + ' ' * 4 + ']', '[' + '#' * 6 + ' ' * 3 + ']', '[' + '#' * 7
                   + ' ' * 2 + ']', '[' + '#' * 8 + ' ' * 1 + ']', '[' + '#' * 9 + ' ' * 0 + ']']
        symblsosymbls = [symbls1, symbls2, symbls3]
        final = symblsosymbls[rn]
        while True:
            for sym in final:
                time.sleep(0.07)
                self.statusbar.SetStatusText('Processing %s' % sym)
                if self.runcomplete:
                    self.statusbar.SetStatusText('Ready')
                    return True
            if self.runcomplete:
                self.statusbar.SetStatusText('Ready')
                return True

    def run(self):
        global prvhash, hmddict, dial, prvsep

        self.abortrun = False
        self.runcomplete = False

        # get user inputs
        inputpath = self.tc1.GetValue()
        seperators = self.tc2.GetValue()
        srchwrd = self.tc3.GetValue()

        # to check change in seps
        changesep = False
        tempsep = seperators

        if prvsep != tempsep:
            changesep = True
            prvsep = tempsep

        # read at once
        try:
            ofle = open(inputpath)
        except IOError:
            dial = wx.MessageDialog(None, 'Check for file path!', 'Error', wx.OK)
            print "Check for file path!!!"
            dial.ShowModal()
            self.runcomplete = True
            return False
        readfile = ofle.read()
        ofle.close()

        if self.abortrun:
            self.abortrun = False
            self.showmessage5()
            return False

        def checkchange():
            global prvhash, hmddict
            sha1hash = hashlib.sha1(readfile)
            temphash = sha1hash.hexdigest()
            if prvhash == "":
                print "New file detected, Hash of file %s" % temphash
                prvhash = temphash
                return False
            elif prvhash == temphash:
                print "No change in previous file, using same dict"
            else:
                print "Change in file detected, calculating hash: %s" % temphash
                prvhash = temphash
                hmddict = {}
                return False
            if changesep:
                print "Change in seperators detected"
                print "Calculating hash: %s" % temphash
                prvhash = temphash
                hmddict = {}
                return False
            return True

        def calcdict(rfle, sprts):
            global hmddict, dial
            # validate seperators input
            for i in range(len(sprts)):
                if i % 2 != 0 and sprts[i] != ",":
                    dial = wx.MessageDialog(None, 'Seperators format incorrect!!!', 'Error', wx.OK)
                    dial.ShowModal()
                    return False
            # re format
            tempstr = ""
            for i in range(len(sprts)):
                if i % 2 == 0 and sprts[i] not in tempstr and not sprts[i].isspace():
                    tempstr += sprts[i]
            if len(tempstr) > 0:
                sprts = "|".join(tempstr)
                sprts += "|"
            else:
                sprts = ""
            alsrts = sprts + '\\n|\\r|\\s|\\||\\r|\\.'
            print "Separators are %s" % alsrts
            templst = re.split(alsrts, rfle)
            hmddict = OrderedDict.fromkeys(templst)
            hmddict.pop('', None)
            return True

        def searchword(srwrd):
            global hmddict, dial, prvwrds
            print
            print '=' * 64
            print 'Searching for the word : %s' % srwrd
            if srwrd in hmddict:
                print 'output : True'
                print '=' * 64
                self.tc4.ChangeValue("True")
                prvwrds.insert(0, srwrd)
                prvwrds = list(OrderedDict.fromkeys(prvwrds))
                prvwrds = prvwrds[0:10]
                self.tc3.Clear()
                for wrd in prvwrds:
                    self.tc3.Append(wrd)
                self.tc3.ChangeValue(srwrd)
                print "Run:End@ %s" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S')
                dial = wx.MessageDialog(None, 'Word Found!', 'Info', wx.OK)
                dial.ShowModal()
                return True
            else:
                print 'word not found'
                print "Run:End@ %s" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S')
                print '=' * 64
                self.tc4.ChangeValue("False")
                dial = wx.MessageDialog(None, 'Word Not Found!', 'Info', wx.OK)
                dial.ShowModal()
                return False

        # check for change
        if not checkchange():
            if not calcdict(readfile, seperators):
                self.runcomplete = True
                return False

        if self.abortrun:
            self.abortrun = False
            self.showmessage5()
            return False

        # search the word
        if not searchword(srchwrd):
            self.runcomplete = True
            return False

        if self.abortrun:
            self.abortrun = False
            self.showmessage5()
            return False

        self.runcomplete = True
        self.abortrun = False


def main():
    # Define main window
    app = wx.App()
    ex = HMDGUI(None, title='HMD')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
