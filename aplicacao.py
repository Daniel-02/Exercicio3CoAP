import getopt
import socket
import sys

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon import defines
from threading import Thread

from sense_emu import SenseHat


# Autor: Daniel Arena Toledo

#Funcao a ser executada quando o observe detecta alteracao no recurso

client = None

sense = SenseHat() #instancia emulado so SenseHat
red = (255, 0, 0) #RGB para cor vermelha
black = (0, 0, 0) #RGB para cor preta (apagado)

limiar_temp = 0 #armazena o limiar de temperatura recebido
limiar_pres = 0 #armazena o limiar de pressao recebido

def callback(response):
    global client
    global limiar_temp
    global limiar_pres
    if(response.payload):
        limites = response.payload.split()
        limiar_temp = float(limites[0]) #armazena a nova temperatura recebida do servidor
        limiar_pres = float(limites[1]) #armazena a nova pressao recebida do servidor
        print ("Media dos limites atuais no servidor")
        print ("Temperatura: {} C".format(limiar_temp) + " ---- Pressao: {} mbar".format(limiar_pres))
    else:
        print ("Nao ha valores armazenados")
    
#Trata o argumento passado e separa em host e porta
address = sys.argv[1]
host, port = address.split(':')
port = int(port)
client = HelperClient(server=(host, port)) #instancia um Client

resposta = client.get('sensor') #faz um get do recurso no servidor
if(resposta.payload):
    limites = resposta.payload.split()
    limiar_temp = float(limites[0]) #armazena a temperatura recebida do servidor
    limiar_pres = float(limites[1]) #armazena a pressao recebida do servidor


client.observe('sensor', callback) #observa o recurso e chama o callback quando ele e alterado

while True:
        temp = sense.temperature #pega a temperatura atual do sensor
        pressure = sense.pressure #pega a pressao atual do sensor
        #Verifica se ambas temperatura e pressao estao acima do limiar
        acende_leds = True if (temp > limiar_temp and pressure > limiar_pres) else False

        #Se estiverem acima do limiar seta leds vermelho, senao preto
        pixels = [red if acende_leds else black for i in range(64)]
        sense.set_pixels(pixels)

