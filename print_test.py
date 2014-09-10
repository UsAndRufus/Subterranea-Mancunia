'''
from win32com import client
import time

ie = client.Dispatch("InternetExplorer.Application")

def printPDFDocument(filename):

    ie.Navigate(filename)

    if ie.Busy:
        time.sleep(1)

    ie.Document.printAll()
    time.sleep(2)

printPDFDocument("test.pdf")

ie.Quit()
'''
'''
import tempfile
import win32api
import win32print

#filename = tempfile.mktemp (".txt")
#open (filename, "w").write ("This is a test")
filename = "test.txt"
win32api.ShellExecute (
  0,
  "print",
  filename,
  #
  # If this is None, the default printer will
  # be used anyway.
  #
  '/d:\\EdwardB-ASUSN56\Toshiba4610',
  ".",
  0
)
'''

import os
os.system('\"C:\Program Files (x86)\Adobe\Reader 10.0\Reader\AcroRd32.exe\" /t test.pdf')
