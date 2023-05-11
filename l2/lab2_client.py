import socket
import threading
import sys

IP, DPORT = 'localhost', 8080

long_message = b"A server once stood tall and proud,//Awaiting clients with a crowd.//Its socket bound to localhost,//With port number 8080 foremost.////A multi-threaded hero brave,//To handle clients with a wave,//When a connection came to call,//It spawned a thread to handle all.////The function that would bear the load,//Would handle clients with a code,//And send an introduction grand,//To clients on this digital land.////The message would proclaim with glee,//The names of owners, bold and free,//Whose major in CS was known,//For all the world to hear and own.////The client then would send a plea,//A long message, they wished to see,//In chunks of size one hundred bytes,//To fill the server's waiting sights.////The server received the message grand,//With length in hex, for all to stand,//And convert it to an integer bright,//To loop and receive with all its might.////Until the message was complete,//And all its bytes had been a treat,//The server would receive it all,//And print it to the console's call.////And so the server stands there still,//Ready to handle every thrill,//A hero to clients all around,//With threads to keep them safe and sound.//"
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
def send_long_message(conn):
    
    # Send the length of the message: this should be 8 total hexadecimal digits
    length = to_hex(len(long_message))
    conn.sendall(str.encode(length))

    # Send the message itself to the server.
    conn.sendall(long_message)

def handle_message():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((IP, int(DPORT)))
        # Receive the introduction message
        intro = recv_intro_message(conn)
        # Print the received message to the screen
        print(intro)
        # Send message to the server
        send_long_message(conn)
        # Close the connection
        conn.close()

def main():
    for i in range(int(sys.argv[1])):
        thread = threading.Thread(target=handle_message)
        thread.start()

    ## Wait for all threads to finish
    #for thread in threading.enumerate():
    #    if thread != threading.current_thread():
    #        thread.join()
    #return 0

# Run the `main()` function
if __name__ == "__main__":
    main()
