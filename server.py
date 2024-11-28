import socket
import sys
import time
import os
import struct

"""
Initialize socket pre-reqs
Then create socket connection

"""

tcp_ip = '127.0.0.1' 
tcp_port = 2371
buffer_size = 1024

socket_connection =socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Indicates this is socket is TCP (connection-oriented protocol)
socket_connection.bind((tcp_ip,tcp_port))


socket_connection.listen(1)

connection,address = socket_connection.accept()
print('\nConnected to by address: {}'.format(address))

"""
Upload Function:
- Establish connection
- Receives file size and processes content inside file
- Send upload details
"""

def upload() -> None:
    connection.send('1')

    file_name_size = struct.unpack('h',connection.recv(2))[0]
    file_name = connection.recv(file_name_size)

    connection.send('1')
   
    file_size = struct.unpack("i", conn.recv(4))[0]
    
    start_time = time.time()
    output_file = open(file_name, "wb")
    
    bytes_received = 0
    
    print("\nReceiving...")

    while bytes_received < file_size:
        l = connection.recv(buffer_size)
        output_file.write(l)
        bytes_received += buffer_size
        output_file.close()

    print("\nReceived file: {}".format(file_name))
    
    connection.send(struct.pack("f", time.time() - start_time))
    connection.send(struct.pack("i", file_size))
    return
