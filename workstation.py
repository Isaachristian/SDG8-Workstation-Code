import socket

ACK_CONNECTION = b'ack_connection'


def receive_file(filename, s):
  with open(filename, 'wb') as f:
    print('file opened')
    while True:
      print('receiving data...')
      data = s.recv(1024)
      print(f'data={data}')
      if not data:
        break

      # write data to a file
      f.write(data)


# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Get local machine name
host = '192.168.1.28'

# Reserve a port for your service.
port = 25000

# Bind to the port
s.bind((host, port))

# Queue up to 5 requests
s.listen(5)                                           

while True:
  print(f'Listening on {host}:{port}...')

  # Establish connection with client.
  c, addr = s.accept()      

  print("Got connection from", addr)
  c.send(ACK_CONNECTION)

  receive_file('photos.zip', s)

  # Close the connection
  c.close()    