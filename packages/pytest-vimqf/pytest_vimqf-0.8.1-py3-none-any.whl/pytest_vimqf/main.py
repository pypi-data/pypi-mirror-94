# -*- coding: utf-8 -*-
import sys

from _pytest.terminal import TerminalReporter
import pytest


__version__ = '0.8.0'


def pytest_addoption(parser):
    group = parser.getgroup('vim-quickfix options')
    group.addoption(
        '--vim-quickfix',
        action='store_true',
        dest='vim_quickfix',
        help='Signal pytest that the output is a vim quickfix window, so that it can shrink the window accordingly.',
    )


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if config.getoption('vim_quickfix'):
        # Unregister the default terminal reporter.
        config.pluginmanager.unregister(name="terminalreporter")

        # Create a new terminal reporter with a modified max width
        reporter = TerminalReporter(config, sys.stdout)
        reporter._tw.fullwidth = reporter._tw.fullwidth - 10

        # Register the new reporter
        config.pluginmanager.register(reporter, "terminalreporter")
