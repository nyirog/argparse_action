"Example script for argparse_action"
import sys
import argparse
import argparse_action

def main():
    namespace = parser.parse_args()
    namespace.action(namespace)

parser = argparse.ArgumentParser(description=__doc__)
action = argparse_action.Action(parser)

@action.add()
def echo(word, upper=False):
   print(word.upper() if upper else word)

if __name__ == "__main__":
    main()

