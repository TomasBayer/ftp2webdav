from cerberus import Validator

_SCHEMA = {
    "ftp": {
        "type": "dict",
        "schema": {
            "host": {"type": "string", "default": "127.0.0.1"},
            "port": {
                "type": "integer",
                "coerce": int,
                "min": 1,
                "max": 65535,
                "default": 21,
            },
        },
        "default": {},
    },
    "webdav": {
        "type": "dict",
        "required": True,
        "schema": {
            "host": {"type": "string", "required": True},
            "port": {"type": "integer", "coerce": int, "min": 1, "max": 65535},
            "protocol": {
                "type": "string",
                "allowed": ["http", "https"],
                "default": "https",
            },
            "path": {"type": "string"},
            "verify_ssl": {"type": "boolean", "default": True},
            "cert": {"type": "string"},
        },
    },
    "target_dir": {"type": "string", "default": "."},
}


class ConfigurationError(Exception):
    pass


def build_configuration(raw_config):
    v = Validator(allow_unknown=False)
    if not v.validate(raw_config, _SCHEMA):
        raise ConfigurationError(v.errors)
    else:
        return v.normalized(raw_config, _SCHEMA)
