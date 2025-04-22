class BaseTool:
    def can_handle(self, step: dict) -> bool:
        raise NotImplementedError

    def execute(self, step: dict):
        raise NotImplementedError
