from flask import Flask, render_template
import Adafruit_DHT
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/temp/<int:speed>')
def temp(speed):

    
    if speed == 1:
       GPIO.setmode(GPIO.BOARD)
       ## Use board pin numbering
       pino_sensor = 25;  #Define a GPIO conectada ao pino de dados do sensor
       #Efetua a leitura do sensor
       umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor);
       # Caso leitura esteja ok, mostra os valores na tela
       if umid is not None and temp is not None:
           print ("Temperatura = {0:0.1f}  Umidade = {1:0.1f}").format(temp, umid);
           
        return "Pegando temperatura"
      
    if speed == 2:
        GPIO.output(7,True)## Switch on pin 7
        return  "Desativando porta 7"
        

    time.sleep(5)## Wait
 
@app.route('/acender/<string:acao>')
def acender(acao):
    return  acao
