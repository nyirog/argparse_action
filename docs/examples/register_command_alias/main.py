"Example script for argparse_action"
import sys
import argparse
import argparse_action

def main():
    namespace = parser.parse_args()
    namespace.action(namespace)

parser = argparse.ArgumentParser(description=__doc__)
action = argparse_action.Action(parser)

@action.add("print", "p")
def echo(parameter):
    "echo the cli argument"
    print(parameter)

if __name__ == "__main__":
    main()
