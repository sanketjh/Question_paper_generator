import PyQt5
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView , QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
from PyQt5.QtNetwork import *
import sys
from optparse import OptionParser


class QWebView(QWebView):
    def closeEvent(self, event):
        # do stuff
        app.quit()

app = QApplication([])

def showQP(html):
    # window = Window()
    # window.show()
    web_view = QWebView()
    web_view.setHtml(html)
    web_view.show()
    app.exec_()
