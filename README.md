# Exercicio 3
![Projeto](figura_1.png)

* O **Cliente** envia seus valores de temperatura e pressão e depois fica observando por alterações no recurso do servidor até que ele deseje se desinscrever, removendo seus valores do recurso.

* O **Servidor CoAP** é resposável por disponibilizar e gerenciar o recurso. Por meio de GET os clientes podem saber seu valor, e por meio de PUT eles enviam o par de valores de temperatura e pressão para o servidor, que vai usá-los para calcular a média com todos os outros valores inscritos, tendo assim os limiares de pressão e temperatura

* A **Camada de Aplicação** recupera os valores dos limiares do servidor e de acordo com as medições de temperatura e pressão acende os LEDs

----------------------------------

## Requisitos:
*	PIP
*	Python 2.7
*	CoAPthon 4.0.2
*	SenseHat Emulator


## Execução:

1) Instalar o CoAPthon usando o comando pip:

	```sudo pip install CoAPthon```


2) Fazer download dos arquivos do Github para a pasta desejada.
Para isso abra o terminal na pasta desejada e execute o comando:

	```git clone https://github.com/daniel-02/Exercicio3CoAP```

3) Apos download entrar no diretorio Exercicio3CoAP:

4) Iniciar o servidor no IP da maquina e na porta desejada, por exemplo, iniciando o servidor no IP 127.0.0.1 e porta 5683:

	```python servidor.py 127.0.0.1:5683```

5) Abrir outro terminal, entrar no diretorio Exercicio3CoAP e iniciar a Camada de Aplicação informando o IP e a porta na qual o servidor foi iniciado:

	```python aplicacao.py 127.0.0.1:5683```

6) Abrir outro terminal, entrar no diretorio Exercicio3CoAP. O Cliente envia os valores de temperatura e pressão, respectivamente, no segundo argumento (-p) e no primeiro argumento (-a) é passado o IP e a porta onde o servidor foi iniciado:

	```python cliente.py -a 127.0.0.1:5683 -p "50 200"```

---------------------------------