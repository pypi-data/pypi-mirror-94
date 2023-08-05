# -*- coding: utf-8 -*-
"""
Base class for Scrapy commands
"""
import os
from optparse import OptionGroup
from twisted.python import failure

from scrapy.utils.conf import arglist_to_dict
from scrapy.exceptions import UsageError


class ScrapyCommand:

    requires_project = False
    crawler_process = None

    # default settings to be used for this command instead of global defaults
    default_settings = {}

    exitcode = 0

    def __init__(self):
        self.settings = None  # set in scrapy.cmdline

    def set_crawler(self, crawler):
        if hasattr(self, '_crawler'):
            raise RuntimeError("crawler already set")
        self._crawler = crawler

    def syntax(self):
        """
        Command syntax (preferably one-line). Do not include command name.
        """
        return ""

    def short_desc(self):
        """
        A short description of the command
        """
        return ""

    def long_desc(self):
        """A long description of the command. Return short description when not
        available. It cannot contain newlines, since contents will be formatted
        by optparser which removes newlines and wraps text.
        """
        return self.short_desc()

    def help(self):
        """An extensive help for the command. It will be shown when using the
        "help" command. It can contain newlines, since no post-formatting will
        be applied to its contents.
        """
        return self.long_desc()

    def add_options(self, parser):
        """
        Populate option parse with options available for this command
        """
        group = OptionGroup(parser, "Global Options")
        group.add_option("--logfile", metavar="FILE",
            help="log file. if omitted stderr will be used")
        group.add_option("-L", "--loglevel", metavar="LEVEL", default=None,
            help="log level (default: %s)" % self.settings['LOG_LEVEL'])
        group.add_option("--nolog", action="store_true",
            help="disable logging completely")
        group.add_option("--profile", metavar="FILE", default=None,
            help="write python cProfile stats to FILE")
        group.add_option("--pidfile", metavar="FILE",
            help="write process ID to FILE")
        group.add_option("-s", "--set", action="append", default=[], metavar="NAME=VALUE",
            help="set/override setting (may be repeated)")
        group.add_option("--pdb", action="store_true", help="enable pdb on failure")

        parser.add_option_group(group)

    def process_options(self, args, opts):
        try:
            self.settings.setdict(arglist_to_dict(opts.set),
                                  priority='cmdline')
        except ValueError:
            raise UsageError("Invalid -s value, use -s NAME=VALUE", print_help=False)

        if opts.logfile:
            self.settings.set('LOG_ENABLED', True, priority='cmdline')
            self.settings.set('LOG_FILE', opts.logfile, priority='cmdline')

        if opts.loglevel:
            self.settings.set('LOG_ENABLED', True, priority='cmdline')
            self.settings.set('LOG_LEVEL', opts.loglevel, priority='cmdline')

        if opts.nolog:
            self.settings.set('LOG_ENABLED', False, priority='cmdline')

        if opts.pidfile:
            with open(opts.pidfile, "w") as f:
                f.write(str(os.getpid()) + os.linesep)

        if opts.pdb:
            failure.startDebugMode()

    def run(self, args, opts):
        """
        Entry point for running commands
        """
        raise NotImplementedError
