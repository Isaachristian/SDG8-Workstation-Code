import socket
import os
import zipfile
import subprocess


DEFAULT_PORT = 25000
MESHROOM_PATH = 'C:\\"Program Files"\Meshroom-2023.2.0\meshroom_batch.exe'


def init():
  # Let the user know if meshroom is not installed

  if not os.path.exists('data'):
    os.makedirs('data')


def setupConnection():
  tcpListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcpListenSocket.bind((getIPAddress(), DEFAULT_PORT))
  tcpListenSocket.listen(1) # Queue up to 5 requests

  return tcpListenSocket 


def receiveFile(filename: str, tcpSocket: socket.socket):
  """Recieves a file from the TCP connection"""

  with open(filename, 'wb') as file:
    print('File opened; Receiving data...')

    recieving = True
    count = 0
    while recieving:
      # print(f'recieving packet {count}...')
      count += 1

      data = tcpSocket.recv(1024)
      print(f'data {count}; len: {len(data)}')
      if not data:
        recieving = False

      file.write(data)
    
    print('Done recieving data, closing file...\n\n')
    file.close()


def getIPAddress():
  """Retrieves the ip address of the local machine"""
  return socket.gethostbyname(socket.gethostname())


def unzipFolder(zipFilepath: str, destinationDir: str):
  with zipfile.ZipFile(zipFilepath, 'r') as zip_ref:
    zip_ref.extractall(destinationDir)

  try:
    os.remove('data/photos.zip')
  except:
    print("failed to remove photos")

def runMeshroom():
  dirs = os.listdir("data")

  dirs.sort()
  dirs.reverse()

  print(dirs)

  try:
    subprocess.run(
      [
        'powershell.exe', 
        '-Command', 
        f"& {MESHROOM_PATH} --input data/{dirs[0]}"
      ], 
      check=True
    )

  except Exception as e:
    print(f'\nSomething went wrong\n')