"""Contain the main function of bronotes."""
import argparse
import logging
import sys
from bronotes.config import cfg
from bronotes.actions.add import ActionAdd
from bronotes.actions.rm import ActionDel
from bronotes.actions.edit import ActionEdit
from bronotes.actions.list import ActionList
from bronotes.actions.mv import ActionMove
from bronotes.actions.set import ActionSet
from bronotes.actions.completions import ActionCompletions
from bronotes.actions.show import ActionShow
from bronotes.actions.sync import ActionSync
from bronotes.actions.git import ActionGit

actions = [
    ActionAdd(cfg),
    ActionDel(cfg),
    ActionList(cfg),
    ActionEdit(cfg),
    ActionMove(cfg),
    ActionSet(cfg),
    ActionCompletions(cfg),
    ActionShow(cfg),
    ActionSync(cfg),
    ActionGit(cfg),
]
actionlist = [action.action for action in actions]


def get_main_parser():
    """Get the main parser."""
    cfg.init()
    parser = argparse.ArgumentParser(prog='bnote')
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Set loglevel to debug.'
    )
    subparsers = parser.add_subparsers(
        help='Bronote actions.', metavar='action')

    for action in actions:
        action.add_subparser(subparsers)

    return parser


def main():
    """Entry point for bronotes."""
    parser = get_main_parser()

    if (len(sys.argv) == 2 and sys.argv[1][0] != '-' and
            sys.argv[1] not in actionlist):
        (args, extra_args) = parser.parse_known_args(
            [cfg.default_action, sys.argv[1]])
    else:
        (args, extra_args) = parser.parse_known_args()

    if not hasattr(args, 'action'):
        list_action = ActionList(cfg)
        args.action = list_action
        args.dir = ''

    args.action.init(args)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    try:
        if args.action.action == 'completions':
            print(args.action.process(parser))
        elif args.action.action == 'git':
            print(args.action.process(extra_args))
        else:
            print(args.action.process())
    except Exception as exc:
        logging.debug(exc)
        print("There was an uncaught exception, \
use --debug to show more info. And throw some output and what you \
were doing to the dev while you're at it.")
