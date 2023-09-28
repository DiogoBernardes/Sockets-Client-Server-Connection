import socket

#Definimos a função "run_client", onde iremos colocar o nosso código

def run_client():
    #De seguida, vamos utilizar a função "socket" e vamos criar um objeto Socket TCP, que irá servir 
    # de ponto de contacto entre o cliente e o servido
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    #Após criarmos o Socket, vamos agora proceder à conexão ao Socket do servidor, para isso iremos atribuir o IP e o numero da Porta
    #a duas variaveis e de seguida através da função "connect"
    server_ip = "127.0.0.1" #localhost
    server_port = 8000
    
    client.connect((server_ip,server_port))
    
    #Finalizada a conexão ao servidor, vamos agora fazer um loop infinito para que consigamos enviar várias mensagem para o servidor
    #Para isso vamos utilizar a função "input" e em seguida procedemos a codificação da mesma em bytes
    while True:
        msg = input("Write a Message: ")
        client.send(msg.encode("utf-8")[:1024])
        
        #Após enviarmos a mensagem, vamos agora fazer o código para que consigamos receber as mensagens por parte do servidor
        #Assim sendo, dentro do loop vamos utilizar a função "recv" para que consigamos receber a mensagem em bytes
        #após isso, procedemos a descodificação da mesma para string através da função "decode" e verificamos se a resposta do servidor
        #é igual a "closed", caso seja o loop é encerrado, caso contrário a mensagem enviada pelo servidor será imprimida
        
        response = client.recv(1024) 
        response = response.decode("utf-8")
        
        if response.lower() == "closed":
            break
        
        print(f"Received: {response}")
        
    #Para finalizar vamos finalizar a conexão do socket do cliente através da função "close", para que assim consigamos libertar recursos
    client.close()
    print("Connection to server closed")
        
run_client()