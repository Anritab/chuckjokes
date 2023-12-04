from flask import Flask, render_template
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from sys import argv
import requests
app = Flask(__name__)


@app.route('/joke')
def joke():
    try:
        response = requests.get('https://api.chucknorris.io/jokes/random')
        data = response.json()
        joke_text = data['value']
    except Exception as e:
        joke_text = f"Failed to fetch joke: {e}"

    return render_template('joke.html', joke_text=joke_text)

@app.route('/')
def index():
    return render_template('index.html')

class WebViewApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('ugly website')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        self.webview = QWebEngineView(self)
        layout.addWidget(self.webview)

if __name__ == '__main__':
    from threading import Thread
    Thread(target=app.run, kwargs={'host': '0.0.0.0'}).start()

    qt_app = QApplication(argv)
    main_window = WebViewApp()
    main_window.webview.setUrl(QUrl('http://127.0.0.1:5000'))
    main_window.show()
    qt_app.exec_()

