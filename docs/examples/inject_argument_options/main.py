"inject argpasre argument options"
import sys
import argparse
import argparse_action

def main():
    namespace = parser.parse_args()
    namespace.action(namespace)

parser = argparse.ArgumentParser(description=__doc__)
action = argparse_action.Action(parser)

@action.add(n={"action": "count"})
def repeat(word, n=0):
    "repeat the word"
    print(word * n)

if __name__ == "__main__":
    main()
