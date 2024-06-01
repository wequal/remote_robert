from flask import Flask, render_template, request, redirect, url_for, Response
import RPi.GPIO as GPIO
import cv2

app = Flask(__name__)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led_pin = 18
GPIO.setup(led_pin, GPIO.OUT)

# MJPEG Streamer URL
STREAM_URL = 'http://192.168.2.169:8080/?action=stream'

# Dummy user credentials
USERNAME = 'admin'
PASSWORD = 'password'

@app.route('/')
def index():
    return render_template('index.html', stream_url=STREAM_URL)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    state = request.form['state']
    if state == 'on':
        GPIO.output(led_pin, GPIO.HIGH)
    else:
        GPIO.output(led_pin, GPIO.LOW)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
