"Default log handler can be defined"
import argparse
import argparse_action
import logging

parser = argparse.ArgumentParser(description=__doc__)
action = argparse_action.Action(parser)

def main():
    argparse_action.add_log_arguments(parser)
    args = parser.parse_args()
    argparse_action.init_logging(
        args, default_handler=argparse_action.create_syslog_handler()
    )
    return args.action(args)

@action.add()
def emit_debug(message):
    logging.debug(message)

if __name__ == "__main__":
    exit(main())
