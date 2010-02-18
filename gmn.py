## gmn.py - Google mail notifier

# ======================================================================
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# ======================================================================

from optparse import OptionParser
import PyQt4
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys

import mail

# URL must end in /
_URL = "https://mail.google.com/gmail/feed/atom/"

class MainWindow(QtGui.QMainWindow):

    def __init__(self, win_parent = None):
        #Init the base class
        QtGui.QMainWindow.__init__(self, win_parent)
        self.create_widgets()
        self.resize(400, 300)
        self.title = "gmail notifier"
        self.setWindowTitle(self.title)
        self.center()
        
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def create_widgets(self):
        # Widgets
        self.username = QtGui.QLineEdit()
        self.password = QtGui.QLineEdit()
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.update = QtGui.QPushButton("Update")
        self.connect(self.update
            , QtCore.SIGNAL("clicked()")
            , self.on_update_clicked)
        self.html_view = QtGui.QTextEdit()
        # Vertical layout contains H layouts
        v_box = QtGui.QVBoxLayout()
        v_box.addWidget(self.username)
        v_box.addWidget(self.password)
        v_box.addWidget(self.update)
        v_box.addWidget(self.html_view)        
        #Create central widget, add layout, and set
        central_widget = QtGui.QWidget()
        central_widget.setLayout(v_box)
        self.setCentralWidget(central_widget)
               
    def on_update_clicked(self):
        self.html_view.setHtml("Retrieving mail...")
        self.html_view.repaint()
        url = _URL + self.label
        self.html_view.setHtml(mail.getmail(url, self.username.text(), self.password.text()))

    def set_label(self, label):
        self.label = label
        if self.label:
            self.setWindowTitle(self.title + " - " + self.label)
        
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--user_name", type="string", dest="user_name", default="",
                      help="default user name")
    parser.add_option("-l", "--label", type="string", dest="label", default="",
                      help="Googlemail label to retrieve")
    (options, args) = parser.parse_args()
    # Someone is launching this directly
    app = QtGui.QApplication(sys.argv)
    #The Main window
    main_window = MainWindow()
    main_window.username.setText(options.user_name)
    main_window.set_label(options.label)
    main_window.show()
    # Enter the main loop
    sys.exit(app.exec_())
