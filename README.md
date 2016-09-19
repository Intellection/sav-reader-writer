# Sav Reader Writer

[![CircleCI](https://circleci.com/gh/Intellection/sav-reader-writer.svg?style=shield)](https://circleci.com/gh/Intellection/sav-reader-writer)

A cross-platform Python interface to the IBM SPSS Statistics Input Output Module. Read or Write SPSS system files (`.sav`, `.zsav`).

Works with Python 2.7, 3.3, 3.4, 3.5 and pypy.

Forked from https://bitbucket.org/fomcl/savreaderwriter.

## Installation

    python setup.py install

Or alternatively:

    pip install savReaderWriter

## Getting Upstream Changes

Sometimes you may need to fetch changes that are made in the original version of this fork and merge them in.

You can sync upstream changes with the following commands:

    git remote add upstream https://bitbucket.org/fomcl/savreaderwriter.git
    git fetch upstream
    git checkout master
    git merge upstream/master

If you need to add a tag / branch from upstream:

    git fetch upstream
    git push v3.5.0
