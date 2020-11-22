"""
    ss13-tools.py
    ------------------

    Runs the project.

    :copyrgiht: 2019 MislavJaksic
    :license: MIT License
"""
import sys

from ss13_tools.package_one import module_one


def main(args):
    """main() will be run if you run this script directly"""
    pass


def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()
