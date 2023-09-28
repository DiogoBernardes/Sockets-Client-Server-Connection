import socket
import threading

def handle_client(client_socket, client_address):
    #Após a conexão ser realizada, vamos realizar uma chamada à função "recv" do objeto client_socket, para que possamos receber dados do socket do cliente
    #Após recebermos os dados do cliente na variável "request", vamos então utilizar a função "decode" para que possamos passar os dados de bytes para uma string
    #Por último, caso o cliente envie a mensagem "close", será enviada uma mensagem de confirmação de encerramento ao cliente através da função "send" 
    # e a conexão será encerrada de seguida, caso contrário irá ser imprimida a mensagem enviada pelo cliente.
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8")
        
        if request.lower() == "close":
            client_socket.send ("closed".encode("utf-8"))
            break
        print(f"Received: {request}")
        
        #Para informarmos o cliente de que o servidor recebeu a mensagem enviada pelo mesmo, criamos uma variavel response,que guardará a resposta por parte do servidor em bytes
        # e de seguida enviamos a mensagem ao cliente novamente através da função "send"
        response = "Message received".encode("utf-8")
        client_socket.send(response)
        
        #Após terminarmos a comunicação com o cliente, vamos então fechar o Socket do cliente utilizando a função "close", para que assim consigamos libtertar recursos do sistema.
        #Para além disso, neste exemplo iremos encerrar também o servidor, embora num contexto real dificilmente isso aconteceria, pois iriamos continuar a espera que mais clientes se conectassem.
    client_socket.close()
    print(f"Connection to client ({client_address[0]}:{client_address[1]}) closed")

#Função que vai conter a maioria do nosso código
def run_server():
    
    #De seguida é criado um objeto do Socket através da função socket.socket()
    #O primeiro parâmetro(socket.AF_INET) é o endereço da família do protocolo, neste caso o IPv4
    #O segundo parâmetro(socket.SOCK_STREAM) é o tipo de socket, neste caso o TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Posto isto, vamos vincular o Socket do servidor a um endereço de IP e a uma Porta
    #Como o servidor está hospedado na máquina local, iremos utilizar o IP associado ao localhost, que é o 127.0.0.1
    #Quanto à porta, definimos a porta 8000 que será através dela que o sistema operacional irá identificar a aplicação do servidor.
    server_ip = "127.0.0.1"
    port = 8000
    
    #Após criarmos as variaveis com o IP e a  porta, vamos agora preparar o socket para receber conexões,
    #para isso utilizamos a função "bind" que é responsãvel por associar o Socket a um IP e a uma Porta
    server.bind((server_ip, port))
    
    #De seguida, vamos especificar que o servidor apenas estará a conectado a um cliente de cada vez
    #Para isso utilizamos a função "Listen" que é responsável por escutar as conexões de entrada no Socket e para que o servidor apenas se conecte a um cliente
    #vamos utilizar o valor "0", pois se espeficicarmos um valor maior, esse valor será o número de conexões pendentes que o servidor poderá ter para serem aceites
    server.listen(0)
    print(f"Listening on IP: {server_ip}")
    print(f"Listening on Port: {port}")
    
    #Após especificarmos o IP e a porta, vamos agora aceitar as conexões entre servidor e cliente,
    #para isso utilizamos a função "accept" que e responsável por ficar à espera que algum cliente se conecte
    #após isso acontecer, esta função retorna dois valores, sendo eles um novo objeto Socket que representa a conexão com o cliente
    #e o IP e a Porta do cliente.
    while True:
        client_socket, client_address = server.accept()
        print(f"Connected to {client_address[0]}:{client_address[1]}")
        # Criando uma nova thread para lidar com o cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()  # Iniciando a thread
        
#Por ultimo, para que o servidor funcione não nos podemos esquecer de chamar a função "run_server"
run_server()