#!/user/bin/env python3
# encoding utf-8
"""
main.py - example of a Python 3 application
"""
import argparse
import sys
from person import Person


def parse_sys_args(sys_args: list) -> argparse:
    """
    Use argparse to procss any commandline arguments that were
    passed into the python file.
    Also enable '-h' argument for users that prefer a cli feel
    :param sys_args: list of command line arguments
    :return: argparse object
    """
    parser = argparse.ArgumentParser(description="Example Python 3 Program")

    parser.add_argument("--name", "-n", type=str, help="Person's name")

    return parser.parse_args(sys_args)


def print_hi(name: str):
    print(f'Hi, {name}')


def main(sys_args: list) -> int:
    """
    Entry function
    :param sys_args: list of strings passed after the python file name
    :return: 0 if successful run or 1 if failure
    """
    response = 1

    try:
        arguments = parse_sys_args(sys_args)
        if not arguments.name:
            print('A --name argument must be provided to this program')
            return response

        person1 = Person(arguments.name)

        print_hi(person1.name)

        return 0
    except ValueError as e:
        print(f'Unable to continue: {e}')
        return response


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
