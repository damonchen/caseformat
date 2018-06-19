from enum import Enum
from functools import partial

class _CaseForamt(object):
    @classmethod
    def _case_format(cls, fields, format_method, join_field=''):
        r = []
        for field in fields:
            field = format_method(field)
            r.append(field)

        r = join_field.join(r)
        return r

    @classmethod
    def _split_fields(cls, value, validate):
        fields = []
        d = ''
        for v in value:
            if validate(v):
                fields.append(d.lower())
                d = v
            else:
                d += v

        if not d:
            fields.append(d.lower())

        return fields


class LowerCamel(_CaseForamt):
    @classmethod
    def _from(cls, fields):
        r = cls._case_format(fields, lambda v: v.lower(), join_field='')
        return r[0].lower() + r[1:]

    @classmethod
    def to(cls, format, value):
        fields = cls._split_fields(value, validate=lambda v: v.isupper())
        return format._from(fields)

    @classmethod
    def convert_to(cls, format):
        pass


class LowerHyphen(_CaseForamt):
    @classmethod
    def _from(cls, values):
        r = cls._case_format(values, lambda v: v.lower(), join_field='-')
        return r

    @classmethod
    def to(cls, format, value):
        fields = cls._split_fields(value, validate=lambda v: v == '-')
        return format._from(fields)

    @classmethod
    def convert_to(cls, format):
        pass


class LowerUnderScore(_CaseForamt):
    @classmethod
    def _from(cls, values):
        r = cls._case_format(values, lambda v: v.lower(), join_field='_')
        return r

    @classmethod
    def to(cls, format, value):
        fields = cls._split_fields(value, validate=lambda v: v == '_')
        return format._from(fields)

    @classmethod
    def convert_to(cls, format):
        pass


class UpperCamel(_CaseForamt):
    @classmethod
    def _from(cls, values):
        r = cls._case_format(values, lambda v: v.upper(), join_field='')
        return r

    @classmethod
    def to(cls, format, value):
        first_upper = True

        def validate(first_upper, v):
            if not first_upper and v.upper():
                return True
            elif v.upper():
                first_upper = False
                return False
            else:
                return False

        fields = cls._split_fields(value, validate=partial(validate, first_upper))
        return format._from(fields)

    @classmethod
    def convert_to(cls, format):
        pass


class UpperUnderscore(_CaseForamt):
    @classmethod
    def _from(cls, values):
        r = cls._case_format(values, lambda v: v.upper(), join_field='_')
        return r

    @classmethod
    def to(cls, format, value):
        fields = cls._split_fields(value, validate=lambda v: v == '_')
        return format._from(fields)

    @classmethod
    def convert_to(cls, format):
        pass


class CaseFormat(object):
    LOWER_CAMEL = LowerCamel()
    LOWER_HYPHEN = LowerHyphen()
    LOWER_UNDERSCORE = LowerUnderScore()
    UPPER_CAMEL = UpperCamel()
    UPPER_UNDERSCORE = UpperUnderscore()


if __name__ == '__main__':
    assert CaseFormat.UPPER_UNDERSCORE.to(CaseFormat.LOWER_CAMEL, "CONSTANT_NAME"), 'constantName'
