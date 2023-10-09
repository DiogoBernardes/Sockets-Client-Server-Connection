import socket
import os
import threading

in_chat = False

def receive_messages(client_socket):
    global in_chat
    while in_chat:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                in_chat = False
                print("\nConnection lost.")
                break
            if message == "Leave chat": 
                in_chat = False
            else:
                print(message)
        except:
            in_chat = False
            print("\nConnection lost.")
            break

        
def run_client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    server_ip = "127.0.0.1" 
    server_port = 8000
    
    client.connect((server_ip,server_port))
    os.system('cls')
    print("--------------------------------")
    print("|      Connected to server     |")
    print("--------------------------------")
    print()
    client_name = input("What is your name? ")
    client.send(client_name.encode("utf-8"))
    
    global in_chat
    
    while True:
        os.system('cls')
        print('1 - Calculator')
        print('2 - Chat Room')
        print('3 - List Clients Connected')
        print('4 - Quit')
        
        opt = int(input('Choose an option:'))
        
        if opt == 1:
            os.system('cls')
            while not in_chat:
                os.system('cls')
                print("Write the mathematic expression u want to do (if u want to go back to menu type 'close'): ")
                expression = input()

                if expression.lower() == "close":
                    break

                client.send(f"calculate: {expression}".encode("utf-8"))
                response = client.recv(1024).decode("utf-8")

                if response.startswith("Result: "):
                    os.system('cls')
                    result = response[len("Result: "):]
                    print(f"The result of the expression is: {result}".encode("utf-8"))
                    input("Press Enter to continue...")
                    
                else:
                    print(f"Something went wrong: {response}".encode("utf-8"))
                    
        elif opt == 2:
            os.system('cls')
            client.send("Enter chat".encode("utf-8"))
            print("You entered the chat. Type 'close' to leave the chat.")
            in_chat = True
            receive_thread = threading.Thread(target=receive_messages, args=(client,))
            receive_thread.start()
            while in_chat:
                message = input()
                if message.lower() == "close":
                    client.send("Leave chat".encode("utf-8"))
                    print("You left the chat.")
                    in_chat = False
                    receive_thread.join()
                else:
                    client.send(message.encode("utf-8"))


        elif opt == 3:
            os.system('cls')
            client.send("Request client list".encode("utf-8"))
            response = client.recv(1024).decode("utf-8")
            print("Connected clients:\n")
            print(response)
            input("\nPress Enter to continue...")
                       
        elif opt == 4:
            os.system('cls')
            print("Do you really want to close session?(yes/no)")
            answer = input()
            if answer.lower() == "yes":
                os.system('cls')
                print("Session closed! Thanks for visiting us!")
                client.send(f"Close session".encode("utf-8"))
                client.close()
                break
            else:
                os.system('cls')
                continue
                                    
        
    print("Connection to server closed")
        
run_client()