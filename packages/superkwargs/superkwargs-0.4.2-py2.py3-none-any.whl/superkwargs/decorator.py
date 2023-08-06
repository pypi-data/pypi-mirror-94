#!/usr/bin/env python
# -*- coding: utf8 -*-

import inspect
try:
    from superkwargs import exceptions
    from superkwargs import inject_kwargs, restore_function
    from superkwargs import annotations
except ImportError:
    import exceptions
    import annotations
    from inject import inject_kwargs, restore_function


def kwarg(name, required=False, default=None, invoke_default=True,
          choices=None, validate=None, types=None):
    def decorator(function):
        def configure(*args, **kwargs):
            if required and name not in kwargs:
                raise exceptions.MissingRequiredKwargException(
                    'Keyword argument \'{arg}\' required to invoke \'{func}\''.format(
                        arg=name, func=function.__name__))

            if name not in kwargs:
                default_val = default
                if invoke_default and hasattr(default_val, '__call__'):
                    default_val = default(kwargs)

                kwargs[name] = default_val

            if (types is not None) and \
               (kwargs[name] is not None) and \
               (type(kwargs[name]).__name__ not in types):

                raise exceptions.WrongKwargValueTypeException(
                    'Keyword argument \'{arg}\' value \'{value}\' type \'{value_type}\' does not in expected types \'{expected_types}\''.format(
                        arg=name,
                        value=kwargs[name],
                        value_type=type(kwargs[name]).__name__,
                        expected_types=types
                    )
                )

            if choices is not None and kwargs[name] not in choices:
                raise exceptions.InvalidKwargValueException(
                    'Keyword argument \'{arg}\' value \'{value}\' not in available choices {choices}'.format(
                        arg=name,
                        value=kwargs[name],
                        choices=choices
                    )
                )

            if validate is not None and not validate(kwargs[name]):
                raise exceptions.KwargValueValidationException(
                    'Keyword argument \'{arg}\' value \'{value}\' failed validation test'.format(
                        arg=name,
                        value=kwargs[name]
                    )
                )

            return function(*args, **kwargs)

        configure.__superkwargs__ = annotations.Metadata(
            function,
            annotations.Kwarg(
                name,
                required,
                default,
                invoke_default,
                choices,
                validate,
                types,
            )
        )

        return configure
    return decorator


def superkwarg(inject=False):
    def decorator(function):
        def configure(*args, **kwargs):
            func_args = inspect.getargspec(function).args
            if len(args) > (1 if (len(func_args) > 0 and func_args[0] in ['self', 'cls'])  else 0):
                raise exceptions.PositionalArgsIncludedException(
                    'Positional argument \'{arg}\' not allowed; kwargs are required'.format(
                        arg=args[0]
                    ))

            if inject:
                try:
                    _blank, state = inject_kwargs(kwargs, function)
                    return function(*args)
                finally:
                    restore_function(function, _blank, state)

            return function(*args, **kwargs)
        return configure
    return decorator
