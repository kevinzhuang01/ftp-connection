import socket # Used for socket connection
import sys # Used to get size of object in bytes
import os # Used for Operating System functions
import struct # Used for data exchange with external sources( Files/ Network Connections)


print("\nWelcome to the FTP server.\n\nTo get started, connect a client.")

"""
Initialize socket pre-reqs
Then create socket connection

"""

tcp_ip = '127.0.0.1' 
tcp_port = 2371
buffer_size = 1024

socket_connection =socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Indicates this is socket is TCP (connection-oriented protocol)

def connect() -> None:
    print('Sending server request')

    try:
        socket_connection.connect((tcp_ip,tcp_port))
        print('Connection Succeeded!')
    except:
        print('Connection Unsuccessful. Check if server is online!')

#TO-DO: Upload File
def upload_file(file_name)-> None:
    print("\nUploading file: {}...".format(file_name))
    try:
        if socket_connection:
            socket_connection.send(file_name.encode())
            print(f'File uploaded: {file_name}')
        else:
            print('Socket is not connected')
    except Exception as e:
        print(f'An error occured while uploading your file!:{e}')
        
    return

    

