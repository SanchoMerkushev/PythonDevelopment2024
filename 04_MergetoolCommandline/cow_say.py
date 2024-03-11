import cmd
import shlex
import cowsay

class CowSayCMd(cmd.Cmd):
    prompt = "cowsay>> "

    def do_list_cows(self, arg):
        '''
        List_cows show names of default avilaible cows
        list_cows PATH show names of avilaible cows in the directory PATH
        '''
        if arg:
            print(cowsay.list_cows(arg))
        else:
            print(cowsay.list_cows())
    
    
    def do_make_bubble(self, arg):
        '''
        Make a bubble with message (string)
        Optional define width of message (int)
        Example of using: make_bubble "Hello, world" 5
        '''
        arguments = shlex.split(arg)
        if not arguments:
            return
        dict_args = {}
        if len(arguments) > 1:
            dict_args["width"] = int(arguments[1])
        print(cowsay.make_bubble(arguments[0], **dict_args))


if __name__ == '__main__':
    CowSayCMd().cmdloop() 

