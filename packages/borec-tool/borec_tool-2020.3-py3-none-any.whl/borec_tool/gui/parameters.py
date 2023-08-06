from dataclasses import dataclass


@dataclass
class StringBoxParams:
    values: list
    label: str


@dataclass
class SpinBoxParams:
    max: int
    value: int
    label: str
    min: int=0
    step: int=1