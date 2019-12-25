import requests
import re
import os
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style
from .ansi import ANSI as Ansi
import pyperclip  # pylint: disable=import-error
from packaging import version


def get_github_tags():
    resp = requests.get("https://api.github.com/repos/nebbles/gitcommit/tags")
    if resp.status_code == requests.codes["ok"]:
        tags_json = resp.json()
        tags = [tag["name"] for tag in tags_json]
        return tags
    else:
        print("Error fetching tags from GitHub")
        resp.raise_for_status()


def find_version():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    version_file_path = os.path.join(dir_path, "__version__.py")
    with open(version_file_path, "r") as f:
        version_file = f.read()
        version_match = re.search(
            r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
        )
        if version_match:
            version = version_match.group(1)
            return version
        raise RuntimeError("Unable to find version string in __version__.py.")


def check_for_update():
    tags = get_github_tags()
    latest_tag_version = tags[0][1:]
    cur_version = find_version()

    if version.parse(cur_version) < version.parse(latest_tag_version):
        Ansi.print_ok("There is an update available for conventional-commit.")
        upgrade_command = "pip install --upgrade conventional-commit"
        pyperclip.copy(upgrade_command)

        style = Style.from_dict(
            {"green": "#a0d762 bold", "red": "#e67061 bold", "command": "#f78ae0 bold"}
        )
        text = FormattedText(
            [
                ("", "Version "),
                ("class:red", cur_version),
                ("", " → "),
                ("class:green", latest_tag_version),
                ("", "\nAdded to your clipboard: "),
                ("class:command", upgrade_command),
            ]
        )
        print_formatted_text(text, style=style)
