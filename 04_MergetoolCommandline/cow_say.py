import cmd
import shlex
import cowsay

class CowSayCMd(cmd.Cmd):
    prompt = "cowsay>> "

    def do_list_cows(self, arg):
        '''
        List_cows show names of default available cows
        list_cows PATH show names of available cows in the directory PATH
        '''
        if arg:
            print(cowsay.list_cows(arg))
        else:
            print(cowsay.list_cows())

    def do_make_bubble(self, arg):
        '''
        Make a bubble with message
        Optional define width of message, default=40
        Example of using: make_bubble "Hello, world" 5
        '''
        arguments = shlex.split(arg)
        if not arguments:
            return
        dict_args = {}
        if len(arguments) > 1:
            dict_args["width"] = int(arguments[1])
        print(cowsay.make_bubble(arguments[0], **dict_args))

    def do_cowsay(self, arg):
        '''
        Cow say a message
        Optional arguments [-e eyes] [-t tongue] [-c cow]
        Format of command: cowsay message [-e eyes] [-t tongue] [-c cow]
        '''
        dict_args = {}
        available_options = ["-e", "-t", "-c"]
        options = {"-e" : "eyes", "-t" : "tongue", "-c" : "cow"}
        arguments = shlex.split(arg)
        if not arguments:
            return
        for i in range(1, len(arguments) - 1):
            if arguments[i] in available_options:
                dict_args[options[arguments[i]]] = arguments[i + 1]
        print(cowsay.cowsay(arguments[0], **dict_args))
    
    def do_cowthink(self, arg):
        '''
        Cow think about a message
        Optional arguments [-e eyes] [-t tongue] [-c cow]
        Format of command: cowsay message [-e eyes] [-t tongue] [-c cow]
        '''
        dict_args = {}
        available_options = ["-e", "-t", "-c"]
        options = {"-e" : "eyes", "-t" : "tongue", "-c" : "cow"}
        arguments = shlex.split(arg)
        if not arguments:
            return
        for i in range(1, len(arguments) - 1):
            if arguments[i] in available_options:
                dict_args[options[arguments[i]]] = arguments[i + 1]
        print(cowsay.cowthink(arguments[0], **dict_args))
        

if __name__ == '__main__':
    CowSayCMd().cmdloop() 

