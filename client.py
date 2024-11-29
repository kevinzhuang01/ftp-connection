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