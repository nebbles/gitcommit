from prompt_toolkit.completion import (
    Completer,
    Completion,
    FuzzyCompleter,
    WordCompleter,
)


class FuzzyWordCompleter(Completer):
    """
    Fuzzy completion on a list of words.
    (This is basically a `WordCompleter` wrapped in a `FuzzyCompleter`.)
    :param words: List of words or callable that returns a list of words.
    :param meta_dict: Optional dict mapping words to their meta-information.
    :param WORD: When True, use WORD characters.
    """

    def __init__(self, words, meta_dict=None, WORD=False):
        # assert callable(words) or all(isinstance(w, string_types) for w in words)

        self.words = words
        self.meta_dict = meta_dict or {}
        self.WORD = WORD

        self.word_completer = WordCompleter(
            words=lambda: self.words, WORD=self.WORD, meta_dict=self.meta_dict
        )

        self.fuzzy_completer = FuzzyCompleter(self.word_completer, WORD=self.WORD)

    def get_completions(self, document, complete_event):
        return self.fuzzy_completer.get_completions(document, complete_event)


class TypeCompleter(FuzzyWordCompleter):
    def __init__(self):
        self.meta_dict = {
            "feat": "production code feature",
            "fix": "production code fixing",
            "chore": "build system / dependencies / config / scripts",
            "docs": "documentation / comments",
            "perf": "improves performance",
            "refactor": "renaming / restructuring",
            "revert": "revert previously commited code",
            "style": "white-space, formatting, semi-colons, etc.",
            "test": "any work to tests",
            "wip": "work in progress / might not build",
        }
        super().__init__(self.meta_dict.keys(), meta_dict=self.meta_dict, WORD=False)


class FooterCompleter(FuzzyWordCompleter):
    def __init__(self):
        self.github_meta_info = "Closes GitHub #issue"
        self.footer_meta_dict = {
            "Close #": self.github_meta_info,
            "Closes #": self.github_meta_info,
            "Closed #": self.github_meta_info,
            "Fix #": self.github_meta_info,
            "Fixes #": self.github_meta_info,
            "Fixed #": self.github_meta_info,
            "Resolve #": self.github_meta_info,
            "Resolves #": self.github_meta_info,
            "Resolved #": self.github_meta_info,
            "Clubhouse [ch": "Associates commit with ticket",
            "Clubhouse [branch ch": "Associates branch with ticket",
        }
        super().__init__(
            self.footer_meta_dict.keys(), meta_dict=self.footer_meta_dict, WORD=False
        )
