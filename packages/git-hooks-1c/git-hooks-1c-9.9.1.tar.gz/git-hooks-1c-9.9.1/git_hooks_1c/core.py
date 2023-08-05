# -*- coding: utf-8 -*-
import sys

from cjk_commons.logging_ import add_loggers
from git_hooks_1c import logger
from git_hooks_1c.cli import get_argparser


def run() -> None:
    argparser = get_argparser()
    args = argparser.parse_args(sys.argv[1:])
    add_loggers(args, logger)
    args.func(args)
