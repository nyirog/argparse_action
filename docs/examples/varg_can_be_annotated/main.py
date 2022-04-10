"Arbitrary argument can be annoted"
import sys
import argparse
import argparse_action

def main():
    namespace = parser.parse_args()
    namespace.action(namespace)

parser = argparse.ArgumentParser(description=__doc__)
action = argparse_action.Action(parser)

@action.add()
def summa(*num: int):
    print(sum(num))

if __name__ == "__main__":
    main()

