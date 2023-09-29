import socket
import os

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
    
    #Finalizada a conexão ao servidor, vamos agora fazer um menu para que o cliente escolha qual a operação que quer realizar
    while True:
        os.system('cls')
        print('1 - Send message')
        print('2 - Calculator')
        print('3 - Quit')
        
        op1 = int(input('Choose an option:'))
        
        if op1 == 1:
            os.system("cls")
            while True:
                #Para o cliente conseguir enviar mensagens para o servidor, utilizamos a função "input" e em seguida procedemos a codificação da mesma em bytes
                msg = input("Write a Message (1 to return to menu): ")
                
                if msg == "1":
                    break
                client.send(msg.encode("utf-8")[:1024])
                
        elif op1 == 2:
            os.system('cls')
            while True:
                operation = input('Your operation (1 to return to menu):')
                if operation == "1":
                    break
                    
                #Para a calculadora utilizamos a função eval que é responsável por avaliar uma expressão em formato string e retorna o resultado da operação
                #Após obtermos o resultado, procedemos á codificação do mesmo enviando o resultado para o servidor e para o cliente
                try:
                    res = eval(operation)
                    message = f"Calc result: {res}".encode("utf-8")
                    client.send(message)
                    print(f"Result: {res}")
                except Exception as e:
                    print(f"Error Calculating: {e}")
                
        elif op1 == 3:
            #Caso o cliente queira fechar a conexão escolha a opção nº3
            break                        
        
    print("Connection to server closed")
        
run_client()