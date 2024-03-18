#!/usr/bin/env python3
import asyncio
import cowsay


clients = {}
cows = {}

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                input_str = q.result().decode()
                command = input_str.split()[0]
                if command == "who":
                    await clients[me].put(cows.values())
                elif command == "cows":
                    await clients[me].put((set(cowsay.list_cows()) - set(cows.values())))
                elif command == "login":
                    if me in cows:
                        await clients[me].put(f"You have previous login - {cows[me]}")
                    elif len(input_str.split()) == 1 or input_str.split()[1] not in cowsay.list_cows():
                        await clients[me].put("Incorrect login, use cows to get list of possible names")
                    else:
                        cows[me] = input_str.split()[1]
                        print(f"New user is {cows[me]}")
                        await clients[me].put(f"You name is {cows[me]}")
                else:
                    if me in cows:
                        for out in clients:
                            if out != me and out in cows:
                                await clients[out].put(cowsay.cowsay(q.result().decode(), cow=cows[me]))
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())

