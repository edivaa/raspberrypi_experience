from flask import Flask, render_template
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/blink/<int:speed>')
def blink(speed):
    GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
    GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
    
    if speed == 1:
        GPIO.output(7,True)## Switch on pin 7
        print 'aciondo porta 7'
        return "Led ligado"
    if speed == 2:
        GPIO.output(7,False)## Switch off pin 7
        return  "Led desligado"
        
    GPIO.cleanup()

@app.route('/acender/<string:acao>')
def acender(acao):

    GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
    GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
    
    if acao == 'acende':
        GPIO.output(7,True)## Switch on pin 7
        print 'aciondo porta 7'
        return "Led ligado"
    if acao == 'apaga':
        GPIO.output(7,False)## Switch off pin 7
        return  "Led desligado"
    return  acao
