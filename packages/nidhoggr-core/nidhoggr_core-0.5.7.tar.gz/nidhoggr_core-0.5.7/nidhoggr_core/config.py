from typing import NamedTuple

from nidhoggr_core.crypto import KeyPair


class BLConfig(NamedTuple):
    key_pair: KeyPair
    strict: bool = False
    simple_login: bool = True
    legacy_compat: bool = True
