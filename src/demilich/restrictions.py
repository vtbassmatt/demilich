class Restriction():
    ...


def to_races(**kwargs: bool) -> Restriction:
    """
    A value of True means all creatures with this race must
    obey the constraint. False means they satisfy the constraint
    on the keyword, but may exist without the keyword.
    """
    pass


def to_power(under: int|None = None, over: int|None = None) -> Restriction:
    pass


def to_toughness(under: int|None = None, over: int|None = None) -> Restriction:
    pass
