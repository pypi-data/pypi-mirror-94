"""Wrap the git command and execute in the notes directory."""
import os
from bronotes.actions.base_action import BronoteAction


class ActionGit(BronoteAction):
    """Execute git commands in the notes directory."""

    action = 'git'
    arguments = {}
    flags = {}

    def init(self, args):
        """Construct the action."""
        pass

    def process(self, extra_args):
        """Process the action."""
        git_args = ' '.join(extra_args)
        os.chdir(self.cfg.notes_dir)
        result = os.system(f"git {git_args}")

        return result
