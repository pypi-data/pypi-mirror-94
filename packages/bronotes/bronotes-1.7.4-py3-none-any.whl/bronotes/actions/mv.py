"""Move a note or directory."""
import os
import shutil
from bronotes.actions.base_action import BronoteAction


class ActionMove(BronoteAction):
    """Move a note or directory."""

    action = 'mv'
    arguments = {
        'origin': {
            'help': 'Origin file or dir.',
            'nargs': None
        },
        'destination': {
            'help': 'Destination file or dir.',
            'nargs': None
        }
    }
    flags = {}

    def init(self, args):
        """Construct the action."""
        self.origin = os.path.join(self.cfg.notes_dir, args.origin)
        self.destination = os.path.join(
            self.cfg.notes_dir, args.destination)

    def process(self):
        """Process the action."""
        shutil.move(self.origin, self.destination)

        if self.cfg.autosync:
            self.sync()

        return f"Moved {self.origin} to {self.destination}."
