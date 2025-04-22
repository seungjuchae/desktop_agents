class BaseAgent:
    def can_handle(self, step: dict) -> bool:
        """
        Determine if this agent can handle the given step.
        Must be implemented by each subclass.
        """
        raise NotImplementedError

    def execute(self, step: dict):
        """
        Execute the given step.
        """
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__
 