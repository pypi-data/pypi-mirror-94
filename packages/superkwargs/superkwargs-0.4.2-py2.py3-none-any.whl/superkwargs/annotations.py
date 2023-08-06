#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
import inspect


Kwarg = namedtuple(
    'Kwarg',
    ('name', 'required', 'default', 'invoke_default', 'choices', 'validate',
     'types')
)

Metadata = namedtuple(
    'Metadata',
    ('wrapped', 'kwargs')
)


def parse_kwargs(function):
    kwargs = []

    while True:
        try:
            kwargs.append(function.__superkwargs__.kwargs)
            function = function.__superkwargs__.wrapped
        except AttributeError:
            break

    return kwargs


def parse(callable):
    if inspect.isclass(callable):
        return parse_kwargs(callable.__init__)

    return parse_kwargs(callable)