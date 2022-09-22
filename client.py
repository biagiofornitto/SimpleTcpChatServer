import socket
import threading
import configparser

config_parser = configparser.ConfigParser()
config_parser.read('./resources/configuration.ini')

# Connection Data
host = config_parser.get('CONNECTION_DATA', 'host')
port = int(config_parser.get('CONNECTION_DATA', 'port'))


# Choosing Username
username = input("Choose your username: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


# Listening to Server and Sending Username
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'USERNAME' Send Username
            message = client.recv(1024).decode('ascii')
            if message == 'USERNAME':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break
            
# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(username, input(''))
        client.send(message.encode('ascii'))
        
# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
