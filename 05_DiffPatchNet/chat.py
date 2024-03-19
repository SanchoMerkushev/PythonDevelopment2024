import asyncio
import cowsay

clients = {}
id_to_cows = {}
cows_to_id = {}

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while True:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                input_str = q.result().decode()
                if len(input_str.split()) == 0:
                    continue
                command = input_str.split()[0]
                if command == "who":
                    await clients[me].put(" ".join([*cows_to_id]))
                elif command == "cows":
                    available_cows = [*(set(cowsay.list_cows()) - set(id_to_cows.values()))]
                    await clients[me].put((" ".join(available_cows)))
                elif command == "login":
                    if me in id_to_cows:
                        await clients[me].put(f"You have previous login - {id_to_cows[me]}")
                    elif len(input_str.split()) == 1 or input_str.split()[1] not in cowsay.list_cows() or input_str.split()[1] in cows_to_id:
                        await clients[me].put("Incorrect login, use cows to get list of possible names")
                    else:
                        id_to_cows[me] = input_str.split()[1]
                        cows_to_id[id_to_cows[me]] = me
                        print(f"New user is {id_to_cows[me]}")
                        await clients[me].put(f"You name is {id_to_cows[me]}")
                elif command == "say":
                    if len(input_str.split()) > 2:
                        name_cow = input_str.split()[1]
                        if name_cow in cows_to_id:
                            await clients[cows_to_id[name_cow]].put(cowsay.cowsay(" ".join(input_str.split()[2:]), cow=id_to_cows[me]))
                elif command == "yield":
                    if me in id_to_cows:
                        for out in clients:
                            if out != me and out in id_to_cows and len(input_str.split()) > 1:
                                await clients[out].put(cowsay.cowsay(" ".join(input_str.split()[1:]), cow=id_to_cows[me]))
                elif command == "quit":
                    send.cancel()
                    receive.cancel()
                    writer.close()
                    if me in id_to_cows:
                        print(id_to_cows[me], "EXIT")
                        temp_cow = id_to_cows[me]
                        del id_to_cows[me]
                        del cows_to_id[temp_cow]
                    await writer.wait_closed()
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
