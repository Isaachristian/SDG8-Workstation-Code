from utils.utils import *


ACK_CONNECTION = 'ack_connection'

init()
tcpListenSocket = setupConnection()
while True:
  print(f'Listening on {getIPAddress()}:{DEFAULT_PORT}...')

  try:
    # Establish connection with client. (connetion is a socket)
    connection, address = tcpListenSocket.accept()      

    print(f"Got connection from {address}; sending response")
    connection.sendall(ACK_CONNECTION.encode())

    receiveFile('data/photos.zip', connection)

    # Close the connection
    connection.close()

    # unzip the folder
    unzipFolder('data/photos.zip', 'data/')

    # pass it to meshroom
    runMeshroom()

    # 

  except Exception as e:
    print(f'Main Loop: {e}\n')