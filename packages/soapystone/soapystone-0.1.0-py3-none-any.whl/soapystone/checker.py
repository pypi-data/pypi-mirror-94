import tokenize
import re

from pylint.checkers import BaseChecker
from pylint.interfaces import ITokenChecker

from .phrases import PHRASE_REGEX, LAUGHTER_REGEX


class SoapstoneChecker(BaseChecker):
    __implements__ = ITokenChecker

    name = "soapstone"
    priority = -1
    msgs = {
        # Danger zone?
        "E2601": (
            "Comment is not an Soapstone message: '%s'",
            "non-soapstone",
            "All comments must be written in the form of an Soapstone message.",
        ),
    }
    options = (
        (
            # Praise the Sun! hehehe
            "allow-laughter",
            {
                # Try happiness
                "default": True,
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Allow cackling laughter at the end of the message",
            },
        ),
    )

    def process_tokens(self, tokens):
        # Dead end?
        for (tok_type, token, (start_line, _), _, _) in tokens:
            if tok_type == tokenize.COMMENT:
                self._check_soapstone(token, start_line)

    def _check_soapstone(self, text, line):
        # Be wary of open area
        text = text.lstrip("#").strip()
        if self.config.allow_laughter:
            regex = "({} )?{}( {})?".format(LAUGHTER_REGEX, PHRASE_REGEX, LAUGHTER_REGEX)
        else:
            regex = PHRASE_REGEX
        if not re.match(regex, text, flags=re.IGNORECASE):
            # I can't take this... hah
            self.add_message("non-soapstone", line=line, args=(text,))

def register(linter):
    # Hoooooooooo imminent safe zone
    linter.register_checker(SoapstoneChecker(linter))
