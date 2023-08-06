import sys


def main():
    try:
        arg = sys.argv[1]
        print('Hello ' + arg)
    except Exception:
        print("cmd : hello <some text>")

