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
    writer.write(to_hex(len(data)).encode())
    writer.write(data.encode())

    await writer.drain()

async def receive_long_message(reader: asyncio.StreamReader):
    # First we receive the length of the message: this should be 8 total hexadecimal digits!
    # Note: `socket.MSG_WAITALL` is just to make sure the data is received in this case.
    data_length_hex = await reader.readexactly(8)

    # Then we convert it from hex to integer format that we can work with
    data_length = int(data_length_hex, 16)

    full_data = await reader.readexactly(data_length)
    return full_data.decode()


async def handle_client(reader, writer):
    auth = False
    for i in range(3):
        await send_long_message(writer, "PROMPT")
        await send_long_message(writer, "Please enter your password: ")
        if await receive_long_message(reader) == PASSWORD:
            auth = True
            break

    if auth:
        while True:
            # Let client know that we are waiting for command
            await send_long_message(writer, "PROMPT")
            await send_long_message(writer, "Enter a command")
            msg = await receive_long_message(reader)
            print(msg)
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
