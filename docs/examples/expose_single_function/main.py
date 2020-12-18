"Example script for argparse_action"
import argparse
import argparse_action


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    argparse_action.add_action(parser, echo)
    namespace = parser.parse_args()
    namespace.action(namespace)


def echo(word):
    print(word)


if __name__ == "__main__":
    main()
