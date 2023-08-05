"""
    define utility classes and metaclasses
"""


from collections import namedtuple
import collections
from itertools import starmap
from inspect import Parameter, Signature


class Constant(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Constant({0})'.format(self.name)


MANDATORY = Constant('MANDATORY')


def tmap(func, iterables):
    return tuple(map(func, iterables))


tmap = lambda *x: tuple(map(*x))


# ClassField = namedtuple('ClassField','name, default, kwo')
class ClassField(object):
    """
    easy field creation for classes and subclasses
    """
    def __init__(self, name, default=MANDATORY, kwo=False):
        self.name = name
        self.default = default
        self.kwo = kwo
        self.ignore = False

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        if value == "MANDATORY":
            value = MANDATORY
        self._default = value

    def _create_parameter(self):
        kwargs = {'name': self.name}

        if self.default is not MANDATORY:
            kwargs.update(default=self.default)
        if self.kwo:
            kwargs.update(kind=Parameter.KEYWORD_ONLY)
        else:
            kwargs.update(kind=Parameter.POSITIONAL_OR_KEYWORD)

        self._parameter = Parameter(**kwargs)

    @property
    def parameter(self):
        try:
            return self._parameter
        except AttributeError:
            self._create_parameter()
            return self.parameter

    @classmethod
    def isinstance(cls, other):
        return isinstance(other, cls)

    def __repr__(self):
        return ('ClassField(name={0}, default={1}, kwo={2})'
                ''.format(self.name, self.default, self.kwo))

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        for attr in ('name', ):
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True


class UniqueList(collections.abc.Set):
    TypeError = TypeError()

    def __init__(self, tested_attr, accepted_class=None, iterable=None):
        self.accepted_class = accepted_class
        self.tested_attr = tested_attr

        self.elements = lst = []

        if iterable is not None:
            self.extend(iterable)

    def extend(self, other):
        for value in other:
            self.append(value)

    def update(self, other):
        self.extend(other)

    def append(self, value):
        if not(self.test_class(value) and self.test_attr(value)):
            raise self.TypeError

        if value in self:
            self.remove(value)
        self.elements.append(value)

    def remove(self, value):
        self.elements.remove(value)

    @property
    def accepted_class(self):
        return self._accepted_class

    @accepted_class.setter
    def accepted_class(self, value):
        if value is not None:
            self.TypeError = TypeError('Elements must be of type {}'
                                       ''.format(value.__name__))
        self._accepted_class = value

    @property
    def tested_attr(self):
        return self._tested_attr

    @tested_attr.setter
    def tested_attr(self, value):
        if not isinstance(value, str):
            raise TypeError('tested_attr must be string')

        if self.accepted_class is None:
            self.TypeError = TypeError('Elements must have {} attribute'
                                       ''.format(value))
        self._tested_attr = value

    def test_class(self, other):
        ac = self.accepted_class
        if ac is None or isinstance(other, ac):
            return True
        return False

    def test_attr(self, other):
        if hasattr(other, self.tested_attr):
            return True
        return False

    def __iter__(self):
        return iter(self.elements)

    def __contains__(self, value):
        try:
            return value.name in [element.name for element in self.elements]
        except AttributeError:
            raise self.TypeError

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        msg = ', '.join([str(element) for element in self.elements])
        msg = msg.join(['UniqueList(', ')'])
        return msg


class MetaFields(type):
    """
        Enables the seamless dynamic creation of appropriate signatures from inherited
        and explicitly defined '_class_fields' attributes.

        _class_fields must be a list of ClassField objects
        _mandatory_fields must be a sequence of strings -> ClassField(string,
                                                                      default=MANDATORY,
                                                                      kwo=False)
        _optional_fields must be a sequence of tuples -> ClassField(name=t[0],
                                                                    default=t[1]
                                                                    kwo=t[2])
        if t[2] is omitted, default of False will be used.

    """
    def __new__(mcs, clsname, bases, clsdict):
        _mandatory_fields = clsdict.pop('_mandatory_fields', () )
        _optional_fields = clsdict.pop('_optional_fields', () )

        new_class = super().__new__(mcs, clsname, bases, clsdict)

        _class_fields = mcs.build_class_fields(new_class=new_class)

        _class_fields = mcs.fields_from_specs(_class_fields,
                                              _mandatory_fields,
                                              _optional_fields)

        new_class._class_fields = _class_fields

        new_class.__init__.__signature__ = mcs.signature_from_fields(_class_fields)

        return new_class

    def __init__(cls, name, bases, attrs, **kwargs):
        for cf in cls._class_fields:
            if not hasattr(cf, '_class'):
                cf._init_class = cls
        return super().__init__(name, bases, attrs)

    @classmethod
    def build_class_fields(mcs, new_class):
        _class_fields = UniqueList(tested_attr='name', accepted_class=ClassField)
        for base in reversed(new_class.mro()):
            # skip unrelated parents and mix-ins.
            if not isinstance(base, mcs):
                continue
            b_class_fields = getattr(base, '_class_fields', () )
            for class_field in b_class_fields:
                class_field.base = base

            try:
                _class_fields.update(base._class_fields)
            except AttributeError:
                pass

        return _class_fields

    @staticmethod
    def fields_from_specs(_class_fields, _mandatory_fields, _optional_fields):
        """
        Create ClassField objects from `_mandatory_fields` and `_optional_fields`, and
            append to _class_fields

        :param _class_fields: set of ClassField() objects
        :param _mandatory_fields: sequence of strings
        :param _optional_fields: sequence of tuples: (name, default) or
                                                     (name, default, kwo)
        :return: tuple(ClassField(), ClassField(), ...).
        """

        assert all(map(ClassField.isinstance, _class_fields)), \
            '_class_fields must be a sequence of ClassField objects'

        def is_identifier(o):
            try:
                if str.isidentifier(o):
                    return True
            except TypeError:
                pass
            return False

        def validate_of(of):
            if not 1<len(of)<4 and is_identifier(of):
                return False
            return True

        assert all(map(is_identifier, _mandatory_fields)),\
            ('_mandatory_fields must be a sequence of strings representing valid'
             ' identifiers')
        assert all(map(validate_of, _optional_fields)),\
            ('_optional_fields must be a sequence of tuples (1 < len < 4), each t[0]'
             'must be a string representing a valid identifier')

        _class_fields.update(tmap(ClassField, _mandatory_fields))

        _class_fields.update(starmap(ClassField, _optional_fields))

        return _class_fields

    @staticmethod
    def signature_from_fields(_class_fields):
        parms = [field.parameter for field in _class_fields]
        parms.sort(key=lambda x: x.default is not x.empty)
        return Signature(parms)