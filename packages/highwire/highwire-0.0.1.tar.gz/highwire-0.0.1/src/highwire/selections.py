from typing import TypeVar
from highwire.events import Event


S = TypeVar("S")


def minimum(x: Event[float], y: Event[float]) -> Event[float]:
    if x.value <= y.value:
        return x
    return y


def maximum(x: Event[float], y: Event[float]) -> Event[float]:
    if x.value >= y.value:
        return x
    return y


def first(x: Event[S], y: Event[S]) -> Event[S]:
    if x.occurred_at <= y.occurred_at:
        return x
    return y
