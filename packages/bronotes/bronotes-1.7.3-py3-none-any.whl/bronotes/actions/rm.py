"""Delete a note or directory."""
import os
import shutil
from pathlib import Path
from bronotes.actions.base_action import BronoteAction
from bronotes.config import Text


class ActionDel(BronoteAction):
    """Delete a note or directory."""

    action = 'rm'
    arguments = {
        'argument': {
            'help': 'The dir or file to create.',
            'nargs': None
        }
    }
    flags = {
        '--recurse': {
            'short': '-r',
            'action': 'store_true',
            'help': 'Recursively remove parent directories.'
        }
    }

    def init(self, args):
        """Construct the action."""
        self.set_attributes(args)
        self.path = Path(os.path.join(
            self.cfg.notes_dir, self.argument))

    def process(self):
        """Process the action."""
        if self.path.is_dir():
            if self.recurse:
                shutil.rmtree(self.path)
            else:
                try:
                    self.path.rmdir()
                except OSError:
                    return Text.E_DIR_NOT_EMPTY.value
        else:
            try:
                self.path.unlink()
            except FileNotFoundError:
                return Text.E_NO_SUCH.value

        return f"Removed {self.path}."
