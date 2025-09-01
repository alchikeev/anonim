import secrets
from dataclasses import dataclass, field


def generate_submission_key() -> str:
    """Generate a long random submission key.

    Uses 32 bytes of randomness, resulting in a 64-character hex string.
    """
    return secrets.token_hex(32)


@dataclass
class School:
    """Representation of a school with a random submission key."""

    name: str
    submission_key: str = field(default_factory=generate_submission_key)
