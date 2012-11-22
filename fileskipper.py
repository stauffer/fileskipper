#!/usr/bin/python
'Utility to search directory for python scripts and create launch buttons'
__author__ = "Jeff Stauffer"
__copyright__ = "2012 Jeff Stauffer"
__license__ = "GPLv3"
__title__ = "fileskipper"
version = '0.2.4'

#    Built for python 2.7

#    Copyright 2012 Jeff Stauffer
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Utility to search the current directory for all python files and list them in
a GUI with buttons to launch the scripts. Save this script anywhere in your
home directory and it will find all python scripts alongside or below it in
the file tree.

Written exclusively using the fine editor Nano

Special thanks to Dave Umrysh for thoughts, ideas, assistance, etc. You can find
Dave's software at www.umrysh.com

0.2.4
 - code clean ups
 - Lately Dave has added a lot of bug fixes and updates
 - Fixed bug in system arguments being passed as string of strings

TODO
 - use entry box to allow searching for specific file names; use wildcards
'''

import time
from datetime import datetime
import os, glob, fnmatch
import sys,subprocess

try:
  import pygtk
  pygtk.require('2.0')
except ImportError:
  print("pygtk not installed.")
  pygtk = None

try:
  import gtk
except ImportError:
  print("gtk not installed.")
  gtk = None

class Vars:
  path = sys.path[0]
  maxrows = 1
  maxcols = 5
  fileslist = []
  fileslistfullpath = []
  tooltipslist = []
  pattern = '*'
  extensions = 'py, php, txt'
  launchlist = ['python2', 'python3','idle', 'gedit', 'sublime', 'php', 'new']
  sublimeoptions = ['sublime', 'sbl','subl']
  idleoptions = ['/usr/bin/idle-python2.7']
  launcher = ''
  patternbox = gtk.Entry()
  extensionsbox = gtk.Entry()
  sysargs = ''

class Mainwin:
  def deleteEvent(self, widget, data=None):
    print('Quitting...')
    gtk.main_quit()
    return False

  def setlaunchwith(self, widget):
    Vars.launcher = self.launchwith.get_active_text()

  def reloadClicked(self, widget):
    #self.table.hide()
    self.table.destroy()
    Vars.fileslist = [] #reset the list to blank
    Vars.tooltipslist = [] #reset the list to blank
    Vars.fileslistfullpath = []
    #reload the gui based on the user imputted wildcard and extensions
    #read the search criteria entry box
    #read the extension entry box
    Vars.pattern = Vars.patternbox.get_text()
    print Vars.pattern
    Vars.extensions = Vars.extensionsbox.get_text()
    print Vars.extensions
    #self.setArgs()
    self.readthedirectory()
    self.setmax()
    self.makeTable()

  def makeTable(self):
    print('makeTable()')
    self.table = gtk.Table(Vars.maxrows, Vars.maxcols, False)
    self.table.set_col_spacing(5, 5)
    self.scrollwin.add_with_viewport(self.table)
    indx = 0
    for x in range(Vars.maxcols):
    #print len(Vars.fileslist), indx
      if indx > len(Vars.fileslist):
        pass
      else:
        for y in range(Vars.maxrows):
          #print len(Vars.fileslist), indx
          if indx > (len(Vars.fileslist) - 1):
            pass
          else:
            buffer = "button (%d, %d)" %(y, x)
            button = gtk.Button(Vars.fileslist[indx])
            button.set_size_request(80,27)
            #print(Vars.fileslist[indx])
            button.set_tooltip_text(Vars.tooltipslist[indx])
            button.connect("clicked", self.launchbutton, indx)
            self.table.attach(button, x, x+1, y, y+1)
            button.show()
            indx += 1
    self.table.show()

  ## Function modified from: http://stackoverflow.com/a/377028 ##
  def is_tool(self,program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return False

  def setmax(self):
    print('setmax()')
    totalfiles = len(Vars.fileslist)
    if totalfiles % 2 == 0:
      extra = 0
    else:
      extra = 1
    if totalfiles < 13:
      Vars.maxcols = 2
      Vars.maxrows = totalfiles / Vars.maxcols + extra
      print('<12, C:%s, R:%s' %(str(Vars.maxcols), str(Vars.maxrows)))
    elif totalfiles > 12 and totalfiles < 51:
      Vars.maxcols = totalfiles / 10 + extra
      Vars.maxrows = totalfiles / Vars.maxcols + extra
      print('<31, C:%s, R:%s' %(str(Vars.maxcols), str(Vars.maxrows)))
    else:
      Vars.maxcols = totalfiles / 10 + extra
      Vars.maxrows = totalfiles / Vars.maxcols + extra
      print('>30, C:%s, R:%s' %(str(Vars.maxcols), str(Vars.maxrows)))

  def setLaunchWith(self):
    for x in Vars.launchlist:
      self.launchwith.append_text(x)
    self.launchwith.set_active(0)
    Vars.launcher = Vars.launchlist[0]
    print Vars.launchlist

  def readthedirectory(self):
    #filelist = os.listdir(Vars.path)
    if Vars.extensions == '*': #search for all file types
      Vars.extensionsbox.set_text(Vars.extensions)
    else:
      r = (' `~!@#$%^&*()_-+={}|[]\\:;\"\'<>?/.')
      for x in r:
        Vars.extensions = Vars.extensions.replace(x, '')
      extensions= Vars.extensions.split(',')
      extensions.sort()
      Vars.extensionsbox.set_text(Vars.extensions)
      for filetype in extensions:
        print('Searching for .%s files' %(filetype))
        self.locatefiles(filetype, extensions)
      print('Found %s files.' %(len(Vars.fileslist)))

  def locatefiles(self, filetype, extensions):
    if Vars.pattern == "":
      Vars.pattern = "*"
      Vars.patternbox.set_text("*")
      
    for x in os.walk(Vars.path):
      for fname in x[2]:
        filenameArray = fname.split('.')
        if len(fname.split('.')) > 1 and filenameArray[len(filenameArray)-1] == filetype and  fnmatch.fnmatch(fname[:-len(filenameArray[len(filenameArray)-1])],Vars.pattern):#in extensions:
          Vars.fileslist.append(fname)
          fpath = os.path.join(x[0], fname)
          mdate = os.path.getmtime(fpath)
          print('\t- %s' %(fpath))
          mdate = datetime.fromtimestamp(float(mdate)).strftime('%y-%m-%d %H:%M:%S')
          fullfpath = os.path.realpath(fpath)
          Vars.fileslistfullpath.append(fullfpath)
          size = os.path.getsize(fpath)
          tooltiptext = fullfpath + '\n' + 'Last Modified: ' + mdate + '\t' + 'Size: ' + str(size)
          Vars.tooltipslist.append(tooltiptext)

  def launchbutton(self, widget, x):
    self.setArgs()
    print('Launching %s (%s - %s)...' %(Vars.fileslist[x], x, Vars.fileslistfullpath[x]))
    if Vars.launcher == "sublime":
      for count in range(0,len(Vars.sublimeoptions)):
        if self.is_tool(Vars.sublimeoptions[count]) != False:
          print("Using %s to run Sublime" % Vars.sublimeoptions[count])
          Vars.launcher = Vars.sublimeoptions[count]
          break
    #os.system(Vars.launcher + str(Vars.fileslistfullpath[x]) + Vars.sysargs)
    
    if Vars.sysargs == "":
      p = subprocess.Popen((Vars.launcher, str(Vars.fileslistfullpath[x])))
    else:
      ### Make a big-eyed long string and split it for the sysarg call
      popenstring = str(Vars.launcher) + ' ' + str(Vars.fileslistfullpath[x])
      for y in range(len(Vars.sysargs)):
        popenstring = popenstring + ' '+ Vars.sysargs[y]
      Vars.sysargs = popenstring.split(' ')
      print('subprocess.Popen(%s)' %(Vars.sysargs))
      p = subprocess.Popen(Vars.sysargs)
      #p = subprocess.Popen((Vars.launcher, str(Vars.fileslistfullpath[x]), Vars.sysargs))

  def setArgs(self):
    Vars.sysargs = ''
    if self.sysargbox.get_text() != "":
      args = self.sysargbox.get_text().split(' ')
      Vars.sysargs = args
    print('fileskipper.py---- Vars.sysargs: %s' %(Vars.sysargs))

  def changeFolder(self, widget):
    print('changeFolder()...........')
    dialog = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
      Vars.path = dialog.get_filename() + '/'
      self.pathebox.set_text(Vars.path)
    dialog.destroy()
    self.reloadClicked(True)


  def __init__(self): #Make the GUI

    # Check for Import Errors
    if(pygtk == None or gtk == None):
      sys.exit(1) 
  ##########################################################################
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.connect("delete_event", self.deleteEvent)
    self.window.set_default_size(350, 200)
    self.window.set_border_width(10)
    self.window.set_title('%s %s' %(__title__, version))
    self.vbox = gtk.VBox(False, 0)
    self.window.add(self.vbox)

    self.pathhbox = gtk.HBox(False, 0)
    self.vbox.pack_start(self.pathhbox, False, False, 0)
    self.pathhbox.show()

    self.pathebox = gtk.Entry()
    self.pathebox.set_editable(False)
    self.pathebox.set_size_request(280, 26)
    self.pathebox.set_text(Vars.path)
    self.pathhbox.pack_start(self.pathebox, False, False, 0)
    self.pathebox.show()
    self.browsebutton = gtk.Button("Browse")
    #self.browsebutton.set_size_request(40, 30)
    self.browsebutton.connect("clicked", self.changeFolder)
    self.pathhbox.pack_end(self.browsebutton, False, False, 0)
    self.browsebutton.show()

    self.tophbox = gtk.HBox(False, 0)
    self.vbox.pack_start(self.tophbox, False, False, 0)
    self.tophbox.show()

    Vars.patternbox = gtk.Entry()
    Vars.patternbox.set_size_request(90, 26)
    Vars.patternbox.set_text('*')
    self.tophbox.pack_start(Vars.patternbox, False, False, 0)
    #TODO hitting Enter activate Reload button
    Vars.patternbox.connect("activate", self.reloadClicked)
    Vars.patternbox.show()
    Vars.extensionsbox = gtk.Entry()
    Vars.extensionsbox.set_text(Vars.extensions)
    Vars.extensionsbox.set_size_request(120, 26)
    self.tophbox.pack_start(Vars.extensionsbox, False, False, 0)
    #TODO hitting Enter activate Reload button
    Vars.extensionsbox.connect("activate", self.reloadClicked)
    Vars.extensionsbox.show()
    self.reloadbut = gtk.Button('Reload')
    self.tophbox.pack_end(self.reloadbut, False, False, 0)
    self.reloadbut.connect("clicked", self.reloadClicked)
    self.reloadbut.show()    
    self.scrollwin = gtk.ScrolledWindow()
    self.scrollwin.set_border_width(5)
    self.scrollwin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
    self.vbox.pack_start(self.scrollwin, True, True, 0)
    self.scrollwin.show()
    self.readthedirectory()
    self.setmax()
    self.makeTable() #build the table and add it to the scroll window
    self.btmhbox = gtk.HBox(False, 0)
    self.vbox.pack_start(self.btmhbox, False, False, 0)
    self.btmhbox.show ()
    self.launchwith = gtk.combo_box_new_text()
    self.launchwith.connect("changed", self.setlaunchwith)
    self.btmhbox.pack_start(self.launchwith, False, False, 0)
    self.setlaunchwith(self) #load the combo box
    self.launchwith.show()
    self.sysargbox = gtk.Entry()
    self.sysargbox.set_size_request(100, 26)
    self.sysargbox.set_tooltip_text('Enter any arguments (for script to be launched) here.')
    #self.sysargbox.connect("changed", self.setArgs)
    self.btmhbox.pack_start(self.sysargbox, False, False, 20)
    self.sysargbox.show()
    btnquit = gtk.Button("Quit")
    btnquit.connect ("clicked", self.deleteEvent)
    self.btmhbox.pack_end(btnquit, False, False, 0)
    btnquit.show()
    self.setLaunchWith()
    
    self.window.show()
    self.window.show_all()
    self.vbox.show()
    gtk.main()

    for x in Vars.fileslist:
      print x
    print('-----------------------------------')
    for x in Vars.tooltipslist:
      print x

if __name__ == "__main__":
  Mainwin()
