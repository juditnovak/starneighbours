class StarNeighboursError(Exception):
    """Dedicated exception for the business logic with fixed message."""

    msg = ""

    def __init__(self, *args):
        super().__init__(self.msg, *args)
