class DotDict:
    """
    DotDict simple dictionary .dot notation access."""

    def __init__(self, dictionary: dict = {}):
        """
        **dictionary** is a dictionary type variable.
        """

        for name, value in dictionary.items():
            # check if name contains spaces
            # replace 'em with underscores
            if " " in name:
                name = name.replace(" ", "_")

            # check if value is a dictionary
            # return a recusive instance
            if isinstance(value, dict):
                super().__setattr__(name, DotDict(value))
            else:
                super().__setattr__(name, value)

    def __getattr__(self, name: str):
        """Custom get_attr AttributeError"""
        value = self.__dict__.get(name)

        if not value:
            raise AttributeError(f"Unknown attribute variable `{name}`")

        return value