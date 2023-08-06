"""Generate zsh autocompletions."""
import shtab
from bronotes.actions.base_action import BronoteAction


class ActionCompletions(BronoteAction):
    """Generate zsh autocompletions."""

    action = 'completions'
    arguments = {}
    flags = {}

    def init(self, args):
        """Construct the action."""
        pass

    def process(self, parser):
        """Process the action."""
        return shtab.complete_zsh(parser)
