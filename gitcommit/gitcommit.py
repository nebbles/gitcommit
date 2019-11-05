#!/usr/bin/env python
#
# gitcommit: a tool for writing conventional commits, conveniently
# Author: Ben Greenberg
# Created: 20th September 2019
#
# Implements Conventional Commit v1.0.0-beta.4
#
# TEMPLATE:
#
# <type>[(optional scope)]: <description>
#
# [BREAKING CHANGE: ][optional body / required if breaking change]
#
# [optional footer]
#
# ADDITIONAL RULES:
# - Subject line (i.e. top) should be no more than 50 characters.
# - Every other line should be no more than 72 characters.
# - Wrapping is allowed in the body and footer, NOT in the subject.
#

from __future__ import print_function
import sys
import subprocess
import textwrap
from .ansi import ANSI as Ansi
from prompt_toolkit import prompt, ANSI
from prompt_toolkit.completion import (  # pylint: disable=no-name-in-module
    FuzzyWordCompleter,
)


IS_BREAKING_CHANGE = None  # default for global variable


def add_type(commit_msg):
    valid_types = {
        "feat": "MUST be used the commit adds/builds toward a new feature",
        "fix": "MUST be used when a commit represents a bug fix",
        "chore": "Any change to build system, dependencies, config files, scripts (no production code)",
        "docs": "Changes to documentation",
        "perf": "Changes that improves performance",
        "refactor": "Refactoring production code, e.g. renaming a variable/restructuring existing logic",
        "revert": "Any commit that explicitly reverts part/all changes introduced in a previous commit",
        "style": "Changes to white-space, formatting, missing semi-colons, etc.",
        "test": "Changes to tests e.g. adding a new/missing test or fixing/correcting existing tests",
        "wip": "Any code changes that are work in progress; they may not build (use these sparingly!)",
    }
    type_completer = FuzzyWordCompleter(valid_types.keys())

    Ansi.print_info(
        "Please specify the type of this commit using one of the available keywords. Accepted types: "
    )

    type_names = sorted(valid_types.keys())
    prefixes = ["    " + str(i) + "  " + t for i, t in enumerate(type_names)]
    prefix_length = max([len(p) for p in prefixes]) + 2

    for i in range(len(type_names)):
        # Combine type name with type description
        type_print = prefixes[i].ljust(prefix_length) + valid_types[type_names[i]]
        # Wrap type name+description to maximum line length
        # type_print = "\n".join(textwrap.wrap(type_print, width=72, break_long_words=False, subsequent_indent=" "*prefix_length))
        # Print the type
        Ansi.print_warning(type_print)

    print()
    while True:
        text = Ansi.b_green("Type: ")
        c_type = prompt(ANSI(text), completer=type_completer)
        if c_type in valid_types.keys():
            break
        elif c_type in [str(n) for n in range(len(type_names))]:
            # Convert from number back to proper type name
            c_type = type_names[int(c_type)]
            break
        else:
            Ansi.print_error("That is not an accepted commit 'type'.")
            continue

    commit_msg += c_type
    return commit_msg


def add_scope(commit_msg):
    Ansi.print_info("\nWhat is the scope of this commit?")
    text = Ansi.b_green("Scope (optional): ")
    c_scope = prompt(ANSI(text)).strip()

    if c_scope != "":
        commit_msg += "({})".format(c_scope)

    return commit_msg


def check_if_breaking_change():
    global IS_BREAKING_CHANGE  # required to be able to write to variable
    contains_break = ""
    print()  # breakline from previous section
    while True:
        text = Ansi.b_yellow("Does commit contain breaking change? [y/n] ")
        contains_break = prompt(ANSI(text)).lower()
        if contains_break not in ["y", "n"]:
            Ansi.print_error("Answer must be 'y' or 'n'")
            continue
        elif contains_break == "y":
            IS_BREAKING_CHANGE = True
            return True
        else:
            IS_BREAKING_CHANGE = False
            return False


def add_description(commit_msg):
    if IS_BREAKING_CHANGE is None:
        raise ValueError("Global variable `IS_BREAKING_CHANGE` has not been set.")

    if IS_BREAKING_CHANGE:
        commit_msg += "!: "
    else:
        commit_msg += ": "

    num_chars_remaining = 50 - len(commit_msg)
    Ansi.print_info(
        "\nWhat is the commit description (i.e. title). The description is a short summary of the code changes. Note that this must be no more than {} characters.".format(
            num_chars_remaining
        )
    )
    c_descr = ""
    while c_descr == "":
        text = Ansi.b_green("Description: ")
        c_descr = prompt(ANSI(text))

        # Sanitise
        c_descr = c_descr.strip()  # remove whitespace
        c_descr = c_descr.capitalize()  # capital first letter
        if c_descr[-1] == ".":
            c_descr = c_descr[:-1]  # remove period if last character
            c_descr = c_descr.strip()  # remove further whitespace

        if c_descr == "":
            Ansi.print_error("You must write a description.")
        if len(c_descr) > num_chars_remaining:
            Ansi.print_error(
                "Your description is too long! ({} characters)".format(len(c_descr))
            )
            Ansi.print_error(
                "You only have {} characters available.".format(num_chars_remaining)
            )
            c_descr = ""  # reset string

    commit_msg += c_descr
    return commit_msg


def add_body(commit_msg):
    if IS_BREAKING_CHANGE is None:
        raise ValueError("Global variable `IS_BREAKING_CHANGE` has not been set.")

    if IS_BREAKING_CHANGE:
        Ansi.print_info(
            "\nPlease explain what has changed in this commit to cause breaking changes."
        )
        c_body = ""
        while c_body == "":
            text = Ansi.b_green("Body (required): ")
            c_body = prompt(ANSI(text))
            if c_body == "":
                Ansi.print_error("You must explain your breaking changes.")
    else:
        Ansi.print_info(
            "\nYou may provide additional contextual information about the code changes here."
        )
        text = Ansi.b_green("Body (optional): ")
        c_body = prompt(ANSI(text))

    full_body = ""
    if IS_BREAKING_CHANGE:
        full_body = "BREAKING CHANGE: " + c_body
    elif c_body != "":
        full_body = c_body

    full_body = "\n".join(
        textwrap.wrap(full_body.strip(), width=72, break_long_words=False)
    )

    if full_body != "":
        commit_msg += "\n\n" + full_body
    return commit_msg


def add_footer(commit_msg):
    Ansi.print_info(
        "\nThe footer MUST contain meta-information about the commit, e.g., related pull-requests, reviewers, breaking changes, with one piece of meta-information per-line. To enter a new line, use the \\ character, NOT the 'Enter' key.'"
    )
    text = Ansi.b_green("Footer (optional): ")
    c_footer = prompt(ANSI(text)).strip()
    if c_footer != "":

        # divide by user defined line breaks
        footer_lines = c_footer.split("\\")
        for i, line in enumerate(footer_lines):
            line = line.strip()  # clean up extraneous whitespace

            # format each user line with forced line breaks to maintain maximum line length
            footer_lines[i] = "\n".join(
                textwrap.wrap(
                    line, width=72, break_long_words=False, subsequent_indent="  "
                )
            )

        # recombine all user defined footer lines
        formatted_footer = "\n".join(footer_lines)
        commit_msg += "\n\n" + formatted_footer

    return commit_msg


def run():
    # print(sys.version + "/n")

    Ansi.print_ok("Starting a conventional git commit...")

    commit_msg = ""
    commit_msg = add_type(commit_msg)
    commit_msg = add_scope(commit_msg)
    check_if_breaking_change()
    commit_msg = add_description(commit_msg)
    commit_msg = add_body(commit_msg)
    commit_msg = add_footer(commit_msg)

    Ansi.print_ok("\nThis is your commit message:")
    print()
    print(commit_msg)
    print()

    # print("\nNOTE: This was a dry run and no commit was made.\n")

    argv_passthrough = []  # by default add no extra arguments

    while True:
        # Warn of extra command line arguments
        if len(sys.argv) > 1:
            Ansi.print_warning(
                "The following additional arguments will be passed to git commit: ",
                end="",
            )
            Ansi.print_warning(sys.argv[1:])
            argv_passthrough = sys.argv[1:]  # overwrite default list

        # Ask for confirmation to commit
        text = Ansi.b_yellow("Do you want to make your commit? [y/n] ")
        confirm = prompt(ANSI(text)).lower()

        if confirm == "y":
            print()
            cmds = ["git", "commit", "-m", commit_msg] + argv_passthrough
            subprocess.call(cmds)
            Ansi.print_ok("\nCommit has been made to conventional commits standards!")
            return

        elif confirm == "n":
            print("Aborting the commit.")
            return

        else:
            Ansi.print_error("Answer must be 'y' or 'n'")
            continue


def main():
    try:
        run()
    except KeyboardInterrupt:
        print("\nAborted.")
