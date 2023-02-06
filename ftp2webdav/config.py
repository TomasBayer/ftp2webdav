import os

from cerberus import Validator


def _file_validator(field, value, error):
    if not os.path.isdir(value):
        error(field, "Must be an existing file")


def _build_schema():
    string = dict(type='string')
    boolean = dict(type='boolean')
    integer = dict(type='integer', coerce=int)

    file = dict(type='string', coerce=os.path.expanduser, validator=_file_validator)

    port = dict(integer, min=1, max=65535)

    sub_dict = lambda **d: dict(type='dict', schema=d)
    required = lambda schema: dict(schema, required=True)
    with_default = lambda schema, default: dict(schema, default=default)

    return dict(
        ftp=with_default(sub_dict(
            host=with_default(string, "127.0.0.1"),
            port=with_default(port, "21")
        ), {}),
        webdav=required(sub_dict(
            host=required(string),
            port=port,
            protocol=with_default(dict(string, allowed=['http', 'https']), "https"),
            path=string,
            verify_ssl=with_default(boolean, True),
            cert=file
        )),
        target_dir=with_default(string, "."),
    )


_SCHEMA = _build_schema()


class ConfigurationError(Exception):
    pass


def build_configuration(raw_config):
    v = Validator(allow_unknown=False)
    if not v.validate(raw_config, _SCHEMA):
        raise ConfigurationError(v.errors)
    else:
        return v.normalized(raw_config, _SCHEMA)
