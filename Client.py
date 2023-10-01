import socket
import os

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
    
    while True:
        os.system('cls')
        print('1 - Send message')
        print('2 - Calculator')
        print('3 - Quit')
        
        opt = int(input('Choose an option:'))
        
        if opt == 1:
            os.system("cls")
            while True:
                print(f"Write a message (if u want to go back to menu type 'close'):")
                message = input()
                
                if message.lower() == "close":
                    break
                
                client.send("message".encode("utf-8")) 
                client.send(f"{client_name} - {message}".encode("utf-8"))
                response = client.recv(1024).decode("utf-8")
                print(response)

        elif opt == 2:
            os.system('cls')
            while True:
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
                else:
                    print(f"Something went wrong: {response}".encode("utf-8"))
                    
        elif opt == 3:
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