"Enum annotation register argument choices"
import sys
import enum
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
    error = enum.auto()

@action.add()
def log(word, level: Level=Level.info):
    if level == Level.debug:
        print(f"D: {word}")

    elif level == Level.info:
        print(f"I: {word}")

    elif level == Level.error:
        print(f"E: {word}")

    else:
        print(word)

if __name__ == "__main__":
    main()
