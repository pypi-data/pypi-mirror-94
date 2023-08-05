from typing import NamedTuple


class KeyPair(NamedTuple):
    private: bytes
    public: bytes
