import sys
import getopt
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines
from threading import Thread

# Autor: Daniel Arena Toledo

#Definicao da classe sensor que representara o recurso no servidor
class Sensor(Resource):

    def __init__(self,name="Sensor",coap_server=None):
        super(Sensor,self).__init__(name,coap_server,visible=True,observable=True,allow_children=True)
        self.payload = "0 0" #Valores dos limiares configurados, inicializado com 0 em cada
        self.resource_type = "rt1"
        self.content_type = "application/json"
        self.interface_type = "if1"
        self.limiar_temp_total = 0 #Valor do total do limiar de temperatura inscritos
        self.limiar_pres_total = 0 #Valor do total do limiar de pressao inscritos
        self.num_cadastrados = 0 #Numero de clientes inscritos

    #GET para esse recurso, retorna ele mesmo
    def render_GET(self,request):    
        return self
    
    #PUT para esse recurso, atualiza valores de limiares de acordo com o cliente estar se inscrevendo ou nao
    #e calcula a media atual desses limiares e atualzia no payload
    #values[0] a temperatura enviada
    #values[1] a pressao enviada
    #values[2] diz se o cliente ta se inscrevendo (1) ou desescrevendo (-1)
    def render_PUT(self, request):
        values = request.payload.split()
        self.limiar_temp_total = self.limiar_temp_total + float(values[0])*float(values[2])
        self.limiar_pres_total = self.limiar_pres_total + float(values[1])*float(values[2])
        self.num_cadastrados = self.num_cadastrados + float(values[2])
        self.payload = str(self.limiar_temp_total/self.num_cadastrados if self.num_cadastrados != 0 else 0)+ ' ' + str(self.limiar_pres_total/self.num_cadastrados if self.num_cadastrados != 0 else 0)
        return self

#Definicao da classe CoAPServer
class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self,(host,port),multicast)
        self.add_resource('sensor/',Sensor())
        print "CoAP server started on {}:{}".format(str(host),str(port))
        print self.root.dump()

def main():
    address = sys.argv[1] #le o argumento passado
    host, port = address.split(':') #divide o argumento passado em host e porta pelo ':'
    port = int(port)
    multicast=False

    server = CoAPServer(host,port,multicast) #instancia o CoAPServer

    try:
        server.listen(10)
        print "executed after listen"
    except KeyboardInterrupt:
        print server.root.dump()
        server.close()
        sys.exit()

if __name__=="__main__":
    main()
