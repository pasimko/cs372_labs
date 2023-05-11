import socket

IP, DPORT = 'localhost', 8081

# Helper function that converts an integer into a string of 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

##################################
# TODO: Implement me for Part 1! #
##################################
def recv_intro_message(conn):
    
    full_data = b""
    data = b""

    # Receive data bytes one by one until a newline ('\n') is received
    while data != b'\n':
        data = conn.recv(1)
        full_data += data

    return full_data.decode()
    


##################################
# TODO: Implement me for Part 2! #
##################################
def send_long_message(conn, message):
    
    # Send the length of the message: this should be 8 total hexadecimal digits
    length = to_hex(len(message))
    conn.sendall(str.encode(length))

    # Send the message itself to the server.
    conn.sendall(str.encode(message))


def main():

    # Configure a socket object to use IPv4 and TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:

        # Connect to the server
        conn.connect((IP, int(DPORT)))

        """
        Part 1: Introduction
        """
        # Receive the introduction message
        intro = recv_intro_message(conn)

        # Print the received message to the screen
        print(intro)

        """
        Part 2: Long Message Exchange Protocol
        """
        long_msg = input("Please enter a message to send to the server: ")

        # Send message to the server
        send_long_message(conn, long_msg)


    print("Sent:", long_msg)
    return 0

# Run the `main()` function
if __name__ == "__main__":
    main()
