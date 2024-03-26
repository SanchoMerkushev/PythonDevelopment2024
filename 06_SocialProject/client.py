import sys
import socket
import cmd
import threading
import asyncio
import readline

class CowSayClientCmd(cmd.Cmd):

    prompt = "cowsay>> "
    host = "localhost"
    port = 1337
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    def do_login(self, arg):
        self.s.send(f"login {arg}\n".encode())


def get_response(cow_cmd):
    while True:
        msg = cow_cmd.s.recv(1024).decode()
        if msg:
            print(msg.strip())
            print(f"{cow_cmd.prompt}{readline.get_line_buffer().strip()}", end="", flush=True)


cow_cmd = CowSayClientCmd()
client = threading.Thread(target=get_response, args=(cow_cmd,))
client.start()
cow_cmd.cmdloop()

