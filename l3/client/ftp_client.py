import os
import socket
from time import sleep
from threading import Thread
import asyncio

IP, DPORT = 'localhost', 8080

os.chdir('myfiles')

# Helper function that converts integer into 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

async def send_long_message(writer: asyncio.StreamWriter, data):
    writer.write(to_hex(len(data)).encode())
    writer.write(data.encode())

    await writer.drain()

async def receive_long_message(reader: asyncio.StreamReader):
    data_length_hex = await reader.readexactly(8)
    data_length = int(data_length_hex, 16)

    full_data = await reader.readexactly(data_length)
    return full_data.decode()

async def connect(i):
    reader, writer = await asyncio.open_connection(IP, DPORT)

    newMsg = ""
    while True:
        code = await receive_long_message(reader)
        msg = await receive_long_message(reader)
        if code == "CLOSE":
            return 0
        # Server is sending file
        if code == "PUT":
            with open(newMsg.split()[1], "w") as file:
                file.write(msg)
        # Server is requesting file
        elif code == "GET":
            msg = "RESET"
            try:
                with open(newMsg[1], "r") as file:
                    msg = file.read()
            except FileNotFoundError:
                print("File not found.")
            except PermissionError:
                print("Permission denied.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            await send_long_message(writer, msg)
        elif code != "PROMPT":
            print(msg)
        else:
            print(msg)
            newMsg = input("> ")
            await send_long_message(writer, newMsg)

async def main():
    tasks = []
    for i in range(1):
        tasks.append(connect(str(i).rjust(8, '0')))

    await asyncio.gather(*tasks)

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
