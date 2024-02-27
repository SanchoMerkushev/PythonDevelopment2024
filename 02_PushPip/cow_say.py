from cowsay import cowsay
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("message", \
    help="A string to wrap in the text bubble")
parser.add_argument("-c", "--cow", default='default', \
    help="The name of the cow (valid names from list_cows by option -l)")
parser.add_argument("-p", "--preset", \
    help="The original cowsay presets: -bgpstwy")
parser.add_argument("-e", "--eyes", default="oo", \
    help="A custom eye string")
parser.add_argument("-t", "--tongue", default="  ", \
    help="A cuslist_cowstom tongue string")
parser.add_argument("-w", "--width", type=int, default=40, \
    help="The width of the text bubble")
parser.add_argument("-cw", "--cowfile", \
    help="A custom string representing a cow")
args = parser.parse_args()
args_dict = vars(args)
print(cowsay(**args_dict))


