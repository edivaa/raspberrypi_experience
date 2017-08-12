from flask import Flask, render_template
import RPi.GPIO as GPIO ## Import GPIO library
import Adafruit_DHT
import time ## Import 'time' library. Allows us to use 'sleep'
import json

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

     if comando == "ligaver":
        GPIO.output(7,GPIO.HIGH) ## Setup GPIO Pin 7 to OUT
        return 'Led vermelho ligado'
     if comando == "deslver" :
        GPIO.output(7,GPIO.LOW)## Switch off pin 7
        return 'Led vermelho desligado'

     if comando == "ligaamar":
        GPIO.output(11,GPIO.HIGH) ## Setup GPIO Pin 7 to OUT
        return 'Led amarelo ligado'
     if comando == "deslamar" :
        GPIO.output(11,GPIO.LOW)## Switch off pin 7
        return 'Led amarelo desligado'

     if comando == "ligaverd":
        GPIO.output(13,GPIO.HIGH) ## Setup GPIO Pin 7 to OUT
        return 'Led verde ligado'
     if comando == "deslverd" :
        GPIO.output(13,GPIO.LOW)## Switch off pin 7
        return 'Led amarelo desligado'


@app.route('/temp/<int:grau>')
def temp(grau):
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

        if int(temp) >= grau:
            GPIO.output(15,GPIO.LOW)## Switch off pin 15
        else:  GPIO.output(15,GPIO.HIGH)## Switch off pin 15

        if grau == 1:
            GPIO.output(15,GPIO.HIGH)## Switch off pin 15
        # time.sleep(5)
        return json.dumps({'umidade': umid, 'temperatura': temp})
    else:
        # Mensagem de erro de comunicacao com o sensor
        return json.dumps({'Falha ao ler dados do DHT11 !!!'})
