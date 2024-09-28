from socket import *
from utils import *
import pickle
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive...")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(pickle.loads(message), clientAddress)
    modifiedMesssage = garble(message)
    serverSocket.sendto(modifiedMesssage, clientAddress)