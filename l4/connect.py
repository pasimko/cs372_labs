import socket

server_address = ('localhost', 8000)  # Replace with the actual server address and port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

request = 'GET /f.txt HTTP/1.1\r\nUser-Agent: I\'m sending this from my python client!\r\n\r\n'  # Replace with your desired HTTP request
client_socket.send(request.encode())

response = b''
while True:
    chunk = client_socket.recv(4096)  # Adjust the buffer size as per your needs
    if not chunk:
        break
    response += chunk

print(response.decode())

client_socket.close()
