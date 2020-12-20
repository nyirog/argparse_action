"Short option can be defined with single character function argument"
import sys
import argparse
import argparse_action

def main():
    namespace = parser.parse_args()
    namespace.action(namespace)

parser = argparse.ArgumentParser(description=__doc__)
action = argparse_action.Action(parser)

@action.add()
def echo(word, u=False):
    print(word.upper() if u else word)

if __name__ == "__main__":
    main()
