from prompt_toolkit.validation import Validator, ValidationError


class TypeValidator(Validator):
    def __init__(self, valid_types: list):
        self.valid_types = valid_types
        super().__init__()

    def validate(self, document):
        text = document.text
        if text not in self.valid_types:
            raise ValidationError(message="That is not a valid type.")


class YesNoValidator(Validator):
    def validate(self, document):
        text = document.text
        if text.lower().strip() not in ["", "y", "n", "yes", "no"]:
            raise ValidationError(message="Answer must be yes/no.")


class DescriptionValidator(Validator):
    def __init__(self, maximum_chars: int):
        if maximum_chars < 0:
            raise ValueError("Cannot have sub-zero maximum")
        self.max_chars_allowed = maximum_chars
        super().__init__()

    def validate(self, document):
        text = document.text

        if text.strip() == "":
            raise ValidationError(message="You must write a description.")

        if len(text) > self.max_chars_allowed:
            num_chars_overflowed = len(text) - self.max_chars_allowed
            raise ValidationError(
                message=f"You are {num_chars_overflowed} characters over the limit."
            )
