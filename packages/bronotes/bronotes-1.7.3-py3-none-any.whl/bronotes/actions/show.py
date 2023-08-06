"""Action to show the contents of a note."""
import os
import logging
import pyperclip
from pathlib import Path
from bronotes.actions.base_action import BronoteAction
from bronotes.config import Text


class ActionShow(BronoteAction):
    """Show the contents of a note."""

    action = 'show'
    arguments = {
        'note': {
            'help': 'The note to show.',
            'nargs': None
        }
    }
    flags = {
        '--copy': {
            'short': '-c',
            'action': 'store_true',
            'help': 'Copy file contents to clipboard.'
        },
        '--search': {
            'short': '-s',
            'action': 'store_true',
            'help': 'Search for a file instead of using a hard path.'
        }
    }

    def init(self, args):
        """Construct the action."""
        self.set_attributes(args)

        if not self.search:
            self.note = Path(os.path.join(
                self.cfg.notes_dir, self.note))
        else:
            self.note = self.find_note(self.note)

    def open(self, note):
        """Return the contents of a note."""
        with open(note) as n:
            contents = n.read()

            if self.copy:
                pyperclip.copy(contents)

            return contents

    def process(self):
        """Process this action."""
        try:
            if os.path.isfile(self.note):
                return self.open(self.note)
            else:
                search_result = self.find_note(self.note.name)

                if search_result:
                    return self.open(search_result)

                return Text.E_NO_SUCH.value
        except Exception as exc:
            logging.debug(exc)
            return 'Error opening note.'
