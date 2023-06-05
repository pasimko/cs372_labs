import os
import socket
import asyncio

INTERFACE, SPORT = 'localhost', 8080
CHUNK = 100

PASSWORD = "Juicyjews"

os.chdir('myfiles')

# TODO: Implement me for Part 1!
def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

async def send_long_message(writer: asyncio.StreamWriter, data):
    print("Sending message:")
    print(data)
    writer.write(to_hex(len(data)).encode())
    writer.write(data.encode())

    await writer.drain()

async def receive_long_message(reader: asyncio.StreamReader):
    # First we receive the length of the message: this should be 8 total hexadecimal digits!
    data_length_hex = await reader.readexactly(8)
    data_length = int(data_length_hex, 16)

    full_data = await reader.readexactly(data_length)
    print(full_data.decode())
    return full_data.decode()

async def handle_command(argv, reader, writer):
    code = "NAK"
    msg = None
    if argv[0] == "list":
        code = "ACK"
        msg = ' '.join(os.listdir())
    elif argv[0] == "remove":
        try:
            os.remove(argv[1])
            code = "ACK"
            msg = "File successfully removed."
        except FileNotFoundError:
            msg = "File not found."
        except PermissionError:
            msg = "Permission denied."
        except Exception as e:
            msg = f"An error occurred: {str(e)}"
    elif argv[0] == "put":
        try:
            code = "GET"
            msg = "Server is requesting file..."
            await send_long_message(writer, code)
            await send_long_message(writer, msg)
            clientResponse = await receive_long_message(reader)
            if clientResponse == "RESET":
                code = "NAK"
                msg = "Client failed to send file."
            else:
                with open(argv[1], "w") as file:
                    file.write(clientResponse)
                    msg = "File successfully written."
                    code = "ACK"
        except FileNotFoundError:
            msg = "File not found."
        except PermissionError:
            msg = "Permission denied."
        except Exception as e:
            msg = f"An error occurred: {str(e)}"
    elif argv[0] == "get":
        try:
            with open(argv[1], "r") as file:
                msg = file.read()
                code = "PUT"
        except FileNotFoundError:
            msg = "File not found."
        except PermissionError:
            msg = "Permission denied."
        except Exception as e:
            msg = f"An error occurred: {str(e)}"
    elif argv[0] == "close":
        code = "CLOSE"
        msg = "Goodbye"
    else:
        msg = "Command not found."
    await send_long_message(writer, code)
    await send_long_message(writer, msg)

async def handle_client(reader, writer):
    auth = False
    for attempts in range(3):
        await send_long_message(writer, "PROMPT")
        await send_long_message(writer, "Please enter your password: ")
        if await receive_long_message(reader) == PASSWORD:
            auth = True
            break
        await send_long_message(writer, "NAK")
        await send_long_message(writer, "Incorrect password.")

    if auth:
        while True:
            # Let client know that we are waiting for command
            await send_long_message(writer, "PROMPT")
            await send_long_message(writer, "Enter a command")
            msg = await receive_long_message(reader)
            print(msg)
            await handle_command(msg.split(), reader, writer)
    else:
        await send_long_message(writer, "CLOSE")
        await send_long_message(writer, "Incorrect password.")

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
            handle_client,
            INTERFACE, SPORT
    )

    async with server:
        await server.serve_forever()

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
