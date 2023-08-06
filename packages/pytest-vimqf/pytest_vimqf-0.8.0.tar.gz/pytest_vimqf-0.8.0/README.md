[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/carlodepieri/pytest-vimqf/CI?logo=github)](https://github.com/CarloDePieri/pytest-vimqf/actions)
[![PyPI](https://img.shields.io/pypi/v/pytest-vimqf)](https://pypi.python.org/pypi/pytest-vimqf)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-vimqf)](https://pypi.python.org/pypi/pytest-vimqf)
[![Build system: poetry](https://img.shields.io/badge/build%20system-poetry-blue)](https://github.com/python-poetry/poetry)

A simple pytest plugin that will shrink pytest output when specified, to fit the
vim quickfix window.

## The problem

The vim quickfix window prepends `||` to commands output lines, to differentiate
from its actual fix elements. This behaviour is intended and not configurable.

Pytest default terminal reporter calculates the available terminal width and
organize its layout accordingly, often printing characters to the far right of
the screen.

When running pytest in vim (for example using [pytest-vim-compiler](https://github.com/CarloDePieri/pytest-vim-compiler)
inside [vim-dispatch](https://github.com/tpope/vim-dispatch)),
its output in the quickfix window will show a broken layout (since there
actually are less columns available than pytest calculated).

This issue is exacerbated if `signcolumn` is set.

<img src="https://user-images.githubusercontent.com/5459291/107146685-03f7cd00-694a-11eb-94b4-1efae06acb4d.png" width="400">

## The solution

Pytest-vimqf simply trick pytest's terminal reporter in thinking the terminal is
slightly smaller. This will allows it to fit nicely in the vim quickfix window.

<img src="https://user-images.githubusercontent.com/5459291/107146686-04906380-694a-11eb-8610-57a9292f4ce3.png" width="400">

## Installation

Install using pip:

```console
# pip install pytest-vimqf
```

## Usage

The plugin is disabled by default, allowing pytest to use the whole terminal when
called normally.

From inside vim, simply add the flag `--vim-quickfix` to pytest. For example:

```bash
:Dispatch pytest --vim-quickfix
```
