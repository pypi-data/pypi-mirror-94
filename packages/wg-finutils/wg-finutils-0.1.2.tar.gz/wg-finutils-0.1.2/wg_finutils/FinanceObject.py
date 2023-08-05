import collections
import csv
import decimal
from inspect import Signature
from itertools import repeat
import os

from .utilityclasses import MetaFields, ClassField


# Standard Library setup
decimal_context = decimal.getcontext()
decimal_context.prec = 8
D = decimal.Decimal


class FinanceObjectMC(object, metaclass=MetaFields):

    # list of class field objects.  each member will be given attribute
    #   of `_init_class` by metaclass.  This will be a reference to the class in which the
    #   field is specified.  `__init__` references self.signature.
    #
    # `_class_fields` will become a set which includes inherited fields not
    #   overwritten here upon definition.

    _class_fields = (ClassField(name='name', default=None), )

    def __init__(self, *args, **kwargs):
        bound_values = self._bind_arguments(args, kwargs)
        for name, value in bound_values.arguments.items():
            setattr(self, name, value)
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            pass
    '''
    def digest_args(self, *args, **kwargs):
        bound_values = self.signature.bind(*args, **kwargs)
    '''

    @property
    def _signature(self):
        """

        """
        try:
            return self._sig
        except AttributeError:
            _cfs = self._class_fields

            parms = [field.parameter for field in _cfs]
            parms.sort(key=lambda x: x.default is not x.empty)
            self._sig = Signature(parms)
            return self._sig

    def _bind_arguments(self, args, kwargs):
        sig = self._signature
        bound_values = sig.bind(*args, **kwargs)
        for param in sig.parameters.values():
            if (param.name not in bound_values.arguments
                    and param.default is not param.empty):
                bound_values.arguments[param.name] = param.default

        return bound_values


class FinanceObject:
    pass
