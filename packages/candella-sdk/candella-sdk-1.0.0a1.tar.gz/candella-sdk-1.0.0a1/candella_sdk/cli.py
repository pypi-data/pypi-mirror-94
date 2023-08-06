#
# cli.py
# Candella SDK
#
# (C) 2021 Marquis Kurt.
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from sys import argv
from argparse import ArgumentParser
from typing import List, Optional
from datetime import datetime as dt
from cookiecutter.main import cookiecutter
from click.exceptions import Abort
from . import sdk
import os


def get_args(override: Optional[List[str]] = None):
    """Returns the namespace of parsed arguments.

    Arguments:
        override (list): A list of strings containing arguments to parse. Defaults to None and will use `sys.argv` if
            undefined.

    Returns:
        arguments (any): The parsed arguments as a namespace.
    """
    arguments = ArgumentParser(
        description="Boostrap Candella frameworks and apps.")
    arguments.add_argument(
        "--action", help="The action to run.", required=True)
    arguments.add_argument(
        "--type", help="The type of project to create.", nargs=1, default="application")
    arguments.add_argument(
        "--project", help="The path to the project to validate.", nargs=1, required=False)
    return arguments.parse_args(override if override else argv[1:])


def main():
    """Runs the main code for the SDK manager."""
    OPTIONS = get_args()

    if OPTIONS.action == "create":
        try:
            sdk.create(sdk.CandellaProjectType(OPTIONS.type[0]))
        except Abort:
            print("\nAbort.")
    elif OPTIONS.action == "validate" and "project" in OPTIONS:
        try:
            print(f"Validating project at {OPTIONS.project[0]}.")
            validation, reason = sdk.validate(OPTIONS.project[0])

            now = dt.now().strftime("%d %b %Y ad %H:%M:%S")
            print(f"\nValidation check performed on {now}.")

            valid_str = "succeeded" if validation else "failed"
            valid_clr = "\u001b[31m\u001b[1m" if not validation else ""
            proj_name = os.path.split(OPTIONS.project[0])[-1:][0]

            print(
                f"{valid_clr}Validation of {proj_name} {valid_str}.\u001b[0m")
            if not validation:
                print(f"Reason: {reason}")
            else:
                print("""
Remember that project validation is not a subsitution for thorough testing, nor does
it guarantee that your project will work correctly with Candella.

Always remember to thoroughly test your projects and how they work in the most recent
versions of Candella alongside the most recent versions of the frameworks and core
services included.
                """)
        except Abort:
            print("\nAbort.")


if __name__ == "__main__":
    main()
