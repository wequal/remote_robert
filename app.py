from flask import Flask, render_template, request, redirect, url_for, session
import RPi.GPIO as GPIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins
led_pin = 18
up_pin = 17
down_pin = 27
left_pin = 22
right_pin = 23

# Set GPIO pins as output
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(up_pin, GPIO.OUT)
GPIO.setup(down_pin, GPIO.OUT)
GPIO.setup(left_pin, GPIO.OUT)
GPIO.setup(right_pin, GPIO.OUT)

# MJPEG Streamer URL
STREAM_URL = 'http://192.168.2.169:8080/?action=stream'

# Dummy user credentials
USERNAME = 'ADMIN'
PASSWORD = 'ADMIN'

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('index.html', stream_url=STREAM_URL)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    state = request.form['state']
    if state == 'on':
        GPIO.output(led_pin, GPIO.HIGH)
    else:
        GPIO.output(led_pin, GPIO.LOW)
    return redirect(url_for('index'))

@app.route('/control_motor', methods=['POST'])
def control_motor():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    direction = request.form['direction']
    if direction == 'up':
        GPIO.output(up_pin, GPIO.HIGH)
    elif direction == 'down':
        GPIO.output(down_pin, GPIO.HIGH)
    elif direction == 'left':
        GPIO.output(left_pin, GPIO.HIGH)
    elif direction == 'right':
        GPIO.output(right_pin, GPIO.HIGH)
    return redirect(url_for('index'))

@app.route('/stop_motor', methods=['POST'])
def stop_motor():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    GPIO.output(up_pin, GPIO.LOW)
    GPIO.output(down_pin, GPIO.LOW)
    GPIO.output(left_pin, GPIO.LOW)
    GPIO.output(right_pin, GPIO.LOW)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
