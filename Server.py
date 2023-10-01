import socket
import threading
import os

def handle_client(client_socket, client_address, client_name):
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")
        
            if not request:
                break
                
            if request == "message":  # Verifica o request
                message = client_socket.recv(1024).decode("utf-8")
                
                if message == "":
                    print(f"The message sent by client {client_name} is empty")
                else:
                    # Divida a mensagem em nome e conteúdo
                    parts = message.split(" - ")
                    if len(parts) == 2:
                        client_name = parts[0]
                        message_content = parts[1]
                        print(f"Received from client {client_name}({client_address[0]}:{client_address[1]}): {message_content}")
                        response = "Server: Message received".encode("utf-8")
                        client_socket.send(response)
                    else:
                        print(f"Invalid message format from client {client_name}: {message}")

            elif request.startswith("calculate:"):
                expression = request.split("calculate:")[1]
                try:
                    result = str(eval(expression))
                    client_socket.send(f"Result: {result}".encode("utf-8"))

                    print(f"Received from client: {client_name}({client_address[0]}:{client_address[1]}): {request}")
                    print(f"The result of the operation made by client {client_name} was: {result}".encode("utf-8"))
                except Exception as e:
                    client_socket.send(f"Error: {str(e)}".encode("utf-8"))

            elif request == "Close session":
                print(f"Connection to {client_name}({client_address[0]}:{client_address[1]}) has been lost.")
                client_socket.close()
                break
                
            else:
                print(f"Invalid request from client {client_name}: {request}")

           
    except ConnectionResetError:
        print(f"Connection to {client_name}({client_address[0]}:{client_address[1]}) has been lost.")
    finally:
        client_socket.close()


def run_server():
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 8000

    server.bind((server_ip, port))
    server.listen(1)

    os.system("cls")
    print(f"Welcome to the server!")
    print(f"Listening on IP: {server_ip}")
    print(f"Listening on Port: {port}")
    
    while True:
    
        client_socket, client_address = server.accept()
        client_name = client_socket.recv(1024).decode("utf-8")
        print(f"Connected to {client_name} with the Adress:{client_address[0]}:{client_address[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, client_name))
        client_handler.start() 

run_server()