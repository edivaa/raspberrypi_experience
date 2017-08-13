from flask import Flask, render_template, jsonify
import RPi.GPIO as GPIO ## Import GPIO library
import Adafruit_DHT
import time ## Import 'time' library. Allows us to use 'sleep'
import json
from datetime import datetime

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
    GPIO.setwarnings(False)
    GPIO.setup(7,GPIO.OUT) ## Setup GPIO Pin 7 to OUT
    GPIO.setup(11,GPIO.OUT) ## Setup GPIO Pin 11 to OUT
    GPIO.setup(13,GPIO.OUT) ## Setup GPIO Pin 13 to OUT

    #acionamento dos leds
    GPIO.output(7,GPIO.HIGH) ## Setup GPIO Pin 7 to OUT
    time.sleep(speed)## Wait
    GPIO.output(7,GPIO.LOW)## Switch off pin 7
    GPIO.output(11,GPIO.HIGH) ## Setup GPIO Pin 7 to OUT
    time.sleep(speed)## Wait
    GPIO.output(11,GPIO.LOW)## Switch off pin 7
    GPIO.output(13,GPIO.HIGH) ## Setup GPIO Pin 7 to OUT
    time.sleep(speed)## Wait
    GPIO.output(13,GPIO.LOW)## Switch off pin 7
    GPIO.cleanup()
    return 'Led foi acionado durante %s segundos'%speed

@app.route('/controle/<string:comando>')
def controle(comando):

     GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
     GPIO.setwarnings(False)
     GPIO.setup(7,GPIO.OUT) ## Setup GPIO Pin 7 to OUT
     GPIO.setup(11,GPIO.OUT) ## Setup GPIO Pin 11 to OUT
     GPIO.setup(13,GPIO.OUT) ## Setup GPIO Pin 13 to OUT

     if comando == "vermelho_ligar":
        GPIO.output(7,GPIO.HIGH) ## Setup GPIO Pin 7 to OUT
        return jsonify({'Led vermelho': 'on'})
     if comando == "vermelho_desligar" :
        GPIO.output(7,GPIO.LOW)## Switch off pin 7
        return jsonify({'Led vermelho': 'off'})

     if comando == "amarelo_ligar":
        GPIO.output(11,GPIO.HIGH) ## Setup GPIO Pin 11 to OUT
        return jsonify({'Led amarelo': 'on'})
     if comando == "amarelo_desliga" :
        GPIO.output(11,GPIO.LOW)## Switch off pin 11
        return jsonify({'Led amarelo': 'off'})

     if comando == "verde_ligar":
        GPIO.output(13,GPIO.HIGH) ## Setup GPIO Pin 13 to OUT
        return jsonify({'Led verde': 'on'})
     if comando == "verde_desligar" :
        GPIO.output(13,GPIO.LOW)## Switch off pin 13
        return jsonify({'Led verde': 'off'})


@app.route('/ligar/')
def ligar():
    GPIO.output(15,GPIO.LOW)## Switch off pin 15
    return jsonify({'ventilador': 'on'})

@app.route('/desligar/')
def desligar():
    GPIO.output(15,GPIO.HIGH)## Switch off pin 15
    return jsonify({'ventilador': 'off'})

@app.route('/temp/')
def temp():
    # Define o tipo de sensor
    sensor = Adafruit_DHT.DHT11
    #sensor = Adafruit_DHT.DHT22

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(15,GPIO.OUT) ## Setup GPIO Pin 13 to OUT

    # Define a GPIO conectada ao pino de dados do sensor
    pino_sensor = 25
    pino_rele = 15

    # Informacoes iniciais
    print ("*** Lendo os valores de temperatura e umidade");

    # Efetua a leitura do sensor
    umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor);
    # Caso leitura esteja ok, mostra os valores na tela
    if umid is not None and temp is not None:
        print ("Temperatura = {0:0.1f}  Umidade = {1:0.1f}").format(temp, umid);
        #return 'Sensor de temperatura ligado temperatura %s  Umidade %s ' %temp, umid
        print ("Aguarda 5 segundos para efetuar nova leitura...");
        # time.sleep(5)
        timestamp = str(datetime.now())
        return jsonify({'umidade': umid, 'temperatura': temp, 'timestamp': timestamp})
    else:
        # Mensagem de erro de comunicacao com o sensor
        return jsonify({'Falha ao ler dados do DHT11 !!!'})
