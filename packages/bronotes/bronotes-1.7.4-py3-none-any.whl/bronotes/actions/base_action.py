"""Base action for bronotes."""
import os
from datetime import datetime
from git import Repo
from git.exc import InvalidGitRepositoryError
from git.exc import GitCommandError
from pathlib import Path
from abc import ABC, abstractmethod


class BronoteAction(ABC):
    """Base bronote action."""

    @property
    @abstractmethod
    def action(self):
        """Name of the action for cli reference."""
        pass

    @property
    @abstractmethod
    def arguments(self):
        """Allow arguments for the action."""
        pass

    @property
    @abstractmethod
    def flags(self):
        """Allow flags for the action."""
        pass

    def __init__(self, cfg):
        """Construct the action."""
        self.cfg = cfg

    @abstractmethod
    def init(self):
        """Construct the child."""
        pass

    @abstractmethod
    def process(self):
        """Process the action."""
        pass

    def set_attributes(self, args):
        """Set attributes based on arguments and flags.

        Parameters:
            args: Arguments given from CLI
        """
        for flag in self.flags.keys():
            flagname = flag[2:]
            try:
                setattr(self, flagname, getattr(args, flagname))
            except AttributeError:
                setattr(self, flagname, None)

        for argument in self.arguments.keys():
            try:
                setattr(self, argument, getattr(args, argument))
            except AttributeError:
                setattr(self, argument, None)

    def add_arguments(self, subparser):
        """Add an actions arguments to a subparser."""
        for argument in self.arguments.keys():
            argdict = self.arguments[argument]

            subparser.add_argument(
                argument,
                help=argdict['help'],
                nargs=argdict['nargs']
            ).complete = {
                "zsh": f"_files -W {self.cfg.notes_dir}",
            }

    def add_flags(self, subparser):
        """Add an actions flags to a subparser."""
        for flag in self.flags.keys():
            flagdict = self.flags[flag]

            subparser.add_argument(
                flagdict['short'],
                flag,
                action=flagdict['action'],
                help=flagdict['help']
            )

    def add_subparser(self, subparsers):
        """Add a subparser based on a actions arguments and flags."""
        subparser = subparsers.add_parser(
            self.action, help=self.__doc__)

        subparser.set_defaults(action=self)
        self.add_arguments(subparser)
        self.add_flags(subparser)

    def sync(self):
        """Sync with git."""
        try:
            repo = Repo(self.cfg.notes_dir)
        except InvalidGitRepositoryError:
            return 'Not a git repo. Set one up first, use the git \
action to execute git commands in your notes directory and set things up. \
Auto-syncing can be enable through the set action.'

        try:
            if not repo.remotes:
                return 'No remotes configured, go figure it out.'
        except AttributeError:
            return 'Git is not set up correctly.'

        repo.git.remote('update')
        commits_behind = len([i for i in repo.iter_commits(
            'master..origin/master')])

        if commits_behind > 0:
            pull_result = repo.git.pull('origin', 'master')
            print(pull_result)

        if repo.is_dirty() or repo.untracked_files:
            self.push(repo)
            return 'Synced with git.'

        return 'No pushing needed.'

    def push(self, repo):
        """Push to git."""
        git = repo.git
        git.add('--all')
        try:
            print(git.commit('-m', f"Automatic sync {datetime.now()}"))
        except GitCommandError:
            pass
        git.push('origin', 'master')

    def find_note(self, filename):
        """Find first occurance of a note traversing from the base folder."""
        for node in os.walk(self.cfg.notes_dir):
            (basepath, dirs, files) = node

            for file in files:
                if filename in file:
                    return Path(f"{basepath}/{file}")
        return False
