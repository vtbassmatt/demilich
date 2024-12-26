from random import choice


class Restriction():
    def passes(self, value):
        return True
    
    def fix(self, value):
        raise NotImplementedError()


class ToRacesRestriction(Restriction):
    def __init__(self, legal_races: list):
        self.legal_races = legal_races

    def passes(self, value: str|tuple[str]):
        if isinstance(value, str) and value in self.legal_races:
            return True
        elif any([x in self.legal_races for x in value]):
            return True
        
        return False
    
    def fix(self, value: str|tuple[str]):
        if isinstance(value, str):
            return (value, choice(self.legal_races))
        else:
            return (*value, choice(self.legal_races))


class HaveKeywordsRestriction(Restriction):
    def __init__(self, keywords: list):
        self.required_keywords = keywords

    def passes(self, value: str|tuple[str]):
        if isinstance(value, str):
            value = (value,)
        return all([x in value for x in self.required_keywords])
    
    def fix(self, value: str|tuple[str]):
        if isinstance(value, str):
            return list(set((value, *self.required_keywords)))
        else:
            return list(set((*value, *self.required_keywords)))


def to_races(*args: str) -> Restriction:
    """
    if this keyword appears, the race must be from this list
    """
    return ToRacesRestriction(args)


def must_have(*args: str) -> Restriction:
    """
    if this race appears, the slot must have these keywords
    """
    return HaveKeywordsRestriction(args)


def to_power(under: int|None = None, over: int|None = None) -> Restriction:
    pass


def to_toughness(under: int|None = None, over: int|None = None) -> Restriction:
    pass
