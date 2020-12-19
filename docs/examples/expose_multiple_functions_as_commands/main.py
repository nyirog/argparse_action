"Expose multiple functions as commands"
import sys
import argparse
import argparse_action

def main():
    namespace = parser.parse_args()
    namespace.action(namespace)

parser = argparse.ArgumentParser(description=__doc__)
action = argparse_action.Action(parser)

@action.add()
def echo(parameter):
    "echo the cli argument"
    print(parameter)

@action.add()
def oche(parameter):
    "echo the revered cli argument"
    acc = list(parameter)
    acc.reverse()
    print("".join(acc))

if __name__ == "__main__":
    main()
