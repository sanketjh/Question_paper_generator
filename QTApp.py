import PyQt5
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView , QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
from PyQt5.QtNetwork import *
import sys
from optparse import OptionParser


#MathJax script tag for using MathJax in the preview
mathJaxScript = '''\n <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script> \n'''

class QWebView(QWebView):
    #If X is pressed in the window
    def closeEvent(self, event):
        app.quit()

app = QApplication([])

def showQP(html):
    web_view = QWebView()
    #Add the script tag
    html2 = html.split('</head>')
    html = html2[0]+mathJaxScript+"</head>\n"+html2[1]

    web_view.setHtml(html)
    web_view.show()
    app.exec_()
