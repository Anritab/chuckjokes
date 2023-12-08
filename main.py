from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from sys import argv
from threading import Thread
from flask import Flask, render_template, send_file
from PIL import Image, ImageDraw
import io
import requests

app = Flask(__name__)

def dragon(x1, y1, x2, y2, depth):
    def paint(draw, x1, y1, x2, y2, k):
        if k == 0:
            draw.line([x1, y1, x2, y2], fill='white')
        else:
            tx = (x1 + x2) // 2 + (y2 - y1) // 2
            ty = (y1 + y2) // 2 - (x2 - x1) // 2
            paint(draw, x2, y2, tx, ty, k - 1)
            paint(draw, x1, y1, tx, ty, k - 1)

    img = Image.new('RGB', (750, 750), color='black')
    draw = ImageDraw.Draw(img)
    paint(draw, x1, y1, x2, y2, depth)

    return img

@app.route('/draw_dragon')
def draw_dragon():
    img = dragon(50, 350, 650, 350, 14)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

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
    Thread(target=app.run, kwargs={'host': '0.0.0.0'}).start()

    qt_app = QApplication(argv)
    main_window = WebViewApp()
    main_window.webview.setUrl(QUrl('http://127.0.0.1:5000'))
    main_window.show()
    qt_app.exec()
