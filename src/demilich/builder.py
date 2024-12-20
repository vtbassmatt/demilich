from demilich.restrictions import Restriction


class SkeletonBuilder():
    def create_keywords(self, **kwargs: str): return self
    def create_races(self, **kwargs: str): return self
    def create_classes(self, **kwargs: str): return self
    def common(self): return self

    def white(self, slots: int): return self
    def blue(self, slots: int): return self
    def black(self, slots: int): return self
    def red(self, slots: int): return self
    def green(self, slots: int): return self
    def artifact(self, slots: int): return self

    def creatures(self): return self
    def mana_values(self, *args: list[int|tuple[int, ...]]): return self
    def sizes(self, *args: list[tuple[int,int]]): return self
    def with_keywords(self, **kwargs: int|float): return self
    def from_races(self, **kwargs: int|float): return self
    def from_classes(self, none=int|float, **kwargs: int|float): return self
    def restrict(self, **kwargs: Restriction): return self

    def spells(self): return self
    def instruction(self, text: str, mana: str|None = None): return self
    def card(self, name: str, text: str, mana: str): return self
