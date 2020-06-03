import getopt
import socket
import sys

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
from coapthon import defines

# Autor: Daniel Arena Toledo

client = None #variavel global para a instancia do client do servidor
enviado_temp = 0 #armazena o valor de temperatura enviada
enviado_pres = 0 #armazena o valor de pressao enviado

#Imprime como usar os comandos
def usage():
    print "Command:\tpython cliente.py -a -p"
    print "Options:"
    print "\t-a, --address=\t\tEndereco da requisicao"
    print "\t-p, --payload=\t\tPayload da requisicao"


#Funcao a ser executada quando o observe detecta alteracao no recurso
def callback(response):
    global client
    global enviado_temp
    global enviado_pres
    print ("Medias dos limites atuais no servidor")
    if(response.payload):
        limites = response.payload.split()
        print ("Temperatura: {} C".format(limites[0]) + " ---- Pressao: {} mbar".format(limites[1]))
    else:
        print ("Nao ha valores armazenados")
    inscrito = True
    while inscrito: 
        opcao = raw_input("Continuar inscrito no servidor? [Y/n]: ")
        print ("------------------------")
        if not (opcao == "n" or opcao == "N" or opcao == "y" or opcao == "Y" or opcao == ""):
            print "Escolha nao reconhecida."
            continue
        elif opcao == "n" or opcao == "N":
            #Caso o usuario nao deseje estar mais inscrito envia o comando para se desescrever no servidor
            #e remover seus valores da media
            while True:
                client.put('sensor', str(enviado_temp) + ' ' + str(enviado_pres) + ' -1')
                client.cancel_observing(response, True)
                inscrito = False
                break
        else:
            break

def main():  
    global client
    global enviado_temp
    global enviado_pres
    address = None
    payload = None
    
    #verifica e processa os argumentos passados
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:a:p:", ["help","address=", "payload="])
    except getopt.GetoptError as err:
        print str(err)  
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-a", "--address"):
            address = a
        elif o in ("-p", "--payload"):
            payload = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(2)

    if address is None:
        print "Endereco deve ser especificado"
        usage()
        sys.exit(2)
    
    if payload is None:
        print "Payload nao pode ser vazio"
        usage()
        sys.exit(2)

    host, port = address.split(':') #trata o endereco passado separando o host e a porta
    port = int(port)

    client = HelperClient(server=(host, port)) #inicializa o client

    enviados = payload.split()
    enviado_temp = enviados[0] #salva temperatura enviada
    enviado_pres = enviados[1] #salva pressao enviada
    response = client.put('sensor', payload + ' 1') #executa o put no servidor mandando os valores
    client.observe('sensor', callback) #observa o recurso e chama o callback quando ele e alterado


if __name__ == '__main__':
    main()
