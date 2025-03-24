class MockConfig:
    app_client_id = "client_id"
    app_client_secret = "client_secret"


class MockCache:
    def exists(self, _: str) -> bool:
        return False

    def set(self, _: str, __: str):
        pass

    def get(self, _: str, __: str) -> str:
        return ""

    def expire(self, _: str, __: int):
        pass
