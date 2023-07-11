import socket


DEFAULT_PORT = 25000
ACK_CONNECTION = 'ack_connection'


def receiveFile(filename: str, tcpSocket: socket.socket):
  """Recieves a file from the TCP connection"""

  with open(filename, 'wb') as file:
    print('File opened; Receiving data...')

    recieving = True
    while recieving:
      data = tcpSocket.recv(1024)
      if not data:
        recieving = False

      file.write(data)
    
    print('Done recieving data, closing file...\n\n')
    file.close()


def getIPAddress():
  """Retrieves the ip address of the local machine"""
  return socket.gethostbyname(socket.gethostname())



tcpListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpListenSocket.bind((getIPAddress(), DEFAULT_PORT))
tcpListenSocket.listen(5) # Queue up to 5 requests

while True:
  print(f'Listening on {getIPAddress()}:{DEFAULT_PORT}...')

  try:
    # Establish connection with client. (connetion is a socket)
    connection, address = tcpListenSocket.accept()      

    print(f"Got connection from {address}; sending response")
    connection.sendall(ACK_CONNECTION.encode())

    receiveFile('photos.zip', connection)

    # Close the connection
    connection.close()    

  except Exception as e:
    print(f'{e}\n')