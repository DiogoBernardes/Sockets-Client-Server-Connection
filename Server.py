import socket
import threading
import os

connected_clients = []
chat_clients = {}
chat_history = {} 
def handle_client(client_socket, client_address, client_name):
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")
        
            if not request:
                break   

            if request.startswith("calculate:"):
                expression = request.split("calculate:")[1]
                try:
                    result = str(eval(expression))
                    client_socket.send(f"Result: {result}".encode("utf-8"))

                    print(f"Received from client: {client_name}({client_address[0]}:{client_address[1]}): {request}")
                    print(f"The result of the operation made by client {client_name} was: {result}".encode("utf-8"))
                except Exception as e:
                    client_socket.send(f"Error: {str(e)}".encode("utf-8"))
                    
            elif request.startswith("Enter chat"):
                print(f"{client_name}({client_address[0]}:{client_address[1]}) entered the chat.")
                chat_clients[client_name] = client_socket
                print(f"Current chat clients: {len(chat_clients)}")
                
                # Verifique se há um arquivo de histórico para o cliente
                history_file = f"{client_name}_history.txt"
                if os.path.exists(history_file):
                    with open(history_file, "r") as f:
                        history = f.read()
                        client_socket.send(history.encode("utf-8"))
                        
                while True:
                    message = client_socket.recv(1024).decode("utf-8")

                    if not message or message == "close" or message == "Leave chat":
                        print(f"{client_name} left the chat.")
                        chat_clients.pop(client_name, None)
                        print(f"Current chat clients after removal: {len(chat_clients)}")
                        break
                            
                    broadcast(f"{client_name}: {message}")
                    print(f"Received from client {client_name}({client_address[0]}:{client_address[1]}): {message}")

            elif request.startswith("Request client list"):
                # Extraia apenas os nomes dos clientes da lista conectada
                client_names = [name for name, _ in connected_clients]
                # Converta a lista de nomes em uma única string com quebras de linha
                client_list_str = "\n".join(client_names)
                client_socket.send(client_list_str.encode("utf-8"))
                
            elif request.startswith("Close session"):
                print(f"Connection to {client_name}({client_address[0]}:{client_address[1]}) has been lost.")
                client_socket.close()
                connected_clients.remove((client_name, client_socket))
                remove_history_file(client_name)
                break
                
            else:
                print(f"Invalid request from client {client_name}: {request}")

           
    except ConnectionResetError:
        print(f"Connection to {client_name}({client_address[0]}:{client_address[1]}) has been lost.")
        connected_clients.remove((client_name, client_socket))
        remove_history_file(client_name)
    finally:
        connected_clients.remove((client_name, client_socket))
        remove_history_file(client_name)
        client_socket.close()

def broadcast(message):
    print(f"Broadcasting: {message}")
    for client_name, client_socket in chat_clients.items():
        try:
            client_socket.send(message.encode("utf-8"))
            
            # Adicione a mensagem ao arquivo de histórico do cliente
            history_file = f"{client_name}_history.txt"
            with open(history_file, "a") as f:
                f.write(message + "\n")
        except:
            chat_clients.pop(client_name, None)
            
def remove(client_socket):
    for client in connected_clients:
        if client[1] == client_socket:
            connected_clients.remove(client)

def remove_history_file(client_name):
    # Remova o arquivo de histórico se existir
    history_file = f"{client_name}_history.txt"
    if os.path.exists(history_file):
        os.remove(history_file)
                 
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

        connected_clients.append((client_name,client_socket))
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, client_name))
        client_handler.start() 

run_server() 