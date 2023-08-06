CLI_CONFIG = {
    "host": {},
    "port": {},
    "server": {},
    "prefix": {},
    "matcher": {},
    "refs": {},
}
CONFIG = {
    "host": {
        "default": "0.0.0.0",
        "type": str,
        "help": "The host interface to bind to.",
    },
    "port": {"default": 8080, "type": int, "help": "The port to bind to"},
    "server": {"default": "starlette", "help": "The server plugin interface to use"},
    "prefix": {
        "default": None,
        "type": str,
        "help": "The prefix for hub references that can be exposed",
    },
    "matcher": {
        "default": "glob",
        "type": str,
        "help": "The matcher plugin that will be used on the refs",
    },
    "refs": {
        "default": ["gate.init.test"],
        "help": "The hub references to expose",
        "nargs": "*",
    },
}
SUBCOMMANDS = {}
DYNE = {
    "gate": ["gate"],
}
