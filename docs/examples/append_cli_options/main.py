"Sequence default value invoke 'append' argparse action"
import sys
import enum
import collections.abc
import argparse
import argparse_action

def main():
    namespace = parser.parse_args()
    namespace.action(namespace)

parser = argparse.ArgumentParser(description=__doc__)
action = argparse_action.Action(parser)

class Level(enum.Enum):
    debug = enum.auto()
    info = enum.auto()

@action.add()
def log(message, level: collections.abc.Sequence[Level]=()):
    for l in level:
        print(f"{l}: {message}")

if __name__ == "__main__":
    main()

