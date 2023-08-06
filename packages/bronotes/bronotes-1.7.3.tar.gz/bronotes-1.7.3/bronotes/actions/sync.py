"""Action to sync the notes dir with git."""
from bronotes.actions.base_action import BronoteAction


class ActionSync(BronoteAction):
    """Sync the notes dir with git."""

    action = 'sync'
    arguments = {}
    flags = {}

    def init(self, args):
        """Construct the action."""
        pass

    def process(self):
        """Process this action."""
        repo = self.sync()

        return repo
