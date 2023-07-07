import socket

DEFAULT_PORT = 25000

ACK_CONNECTION = 'ack_connection'



def receive_file(filename: str, tcpSocket: socket.socket):
  """Recieves a file from the TCP connection"""
  with open(filename, 'wb') as file:
    print('File opened')

    print('Receiving data...')
    while True:
      data = tcpSocket.recv(1024)

      print(f'recieved: {data}\n\n')

      if not data:
        break

      # write data to a file
      file.write(data)
    
    print('Done recieving data, closing file...')
    file.close()

def get_ip_address():
  """Retrieves the ip address of the local machine"""
  return socket.gethostbyname(socket.gethostname())



tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSocket.bind((get_ip_address(), DEFAULT_PORT))
tcpSocket.listen(5) # Queue up to 5 requests

while True:
  print(f'Listening on {get_ip_address()}:{DEFAULT_PORT}...')

  try:
    # Establish connection with client.
    c, addr = tcpSocket.accept()      

    print("Got connection from", addr)
    
    c.sendall(ACK_CONNECTION.encode())

    receive_file('photos.zip', c)

    # Close the connection
    c.close()    

  except Exception as e:
    print(f'{e}\n')