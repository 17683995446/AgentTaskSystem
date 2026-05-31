import uuid
import hashlib


class IdUtil:

    @staticmethod
    def generate_uuid() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def generate_short_id() -> str:
        return str(uuid.uuid4())[:8]

    @staticmethod
    def generate_hash(content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()
