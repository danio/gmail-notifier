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
        self.timer = None
        
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
        # Create central widget, add layout, and set
        central_widget = QtGui.QWidget()
        central_widget.setLayout(v_box)
        self.setCentralWidget(central_widget)

    def show_entries(self, entries):
        html = "<table>" + "\n"
        html += "<tr><th>Subject</th><th>Sender</th></tr>"
        for i in xrange(len(entries)):
            html += "<tr><td>" + entries[i].title + "</td>"
            html += "<td>" + entries[i].author + "</td></tr>\n"
        html += "</table>"
        self.html_view.setHtml(html)

    def check_mail(self):
        self.html_view.setHtml("Retrieving mail...")
        self.html_view.repaint()
        url = _URL + self.options.label
        try:
            entries = mail.getmail(url, self.username.text(), self.password.text())
        except:
            self.html_view.setHtml("Failed to open " + url + ".<p>Check your username and password.")
            self.html_view.repaint()
        else:                
            if len(entries) == 0:
                self.html_view.setHtml("No new mail.")
                self.html_view.repaint()
            else:
                self.show_entries(entries)
                self.html_view.repaint()
                self.activateWindow()
                self.raise_()

    def on_update_clicked(self):
        self.check_mail()
        if not self.timer and self.options.interval > 0: 
            # start a timer to check mail
            self.timer = QtCore.QTimer(self);
            self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.check_mail)
            self.timer.start(self.options.interval * 1000);

    def set_options(self, options):
        self.options = options
        if self.options.label:
            self.setWindowTitle(self.title + " - " + self.options.label)
        
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--user_name", type="string", dest="user_name", default="",
                      help="default user name")
    parser.add_option("-l", "--label", type="string", dest="label", default="",
                      help="Googlemail label to retrieve")
    parser.add_option("-i", "--interval", type="int", dest="interval", default=0,
                      help="Interval (seconds) to check mail - 0 to disable")
    (options, args) = parser.parse_args()
    # Someone is launching this directly
    app = QtGui.QApplication(sys.argv)
    #The Main window
    main_window = MainWindow()
    main_window.username.setText(options.user_name)
    main_window.set_options(options)
    main_window.show()
    # Enter the main loop
    sys.exit(app.exec_())
