from uuid import UUID

import uuid6


class UuidIdGenerator:
    def __call__(self) -> UUID:
        return uuid6.uuid7()
