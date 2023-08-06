from datetime import timedelta
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, List, Any, Union, Callable
from weakref import WeakMethod

from highwire.events import Event, project
from highwire import events, exceptions

R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")


Subscription = Any


class Signal(Generic[T], ABC):
    _subscriptions: List[WeakMethod]

    def __init__(self):
        self._subscriptions = []

    def subscribe(self, subscription: Subscription):
        self._subscriptions.append(WeakMethod(subscription))

    def _notify(self, event: Event[T]):
        for subscription in self._subscriptions:
            callback = subscription()
            if callback is not None:
                callback(event)

    @abstractmethod
    def get(self) -> Optional[T]:
        pass

    def __call__(self) -> Optional[T]:
        return self.get()

    def __sub__(self, other):
        return Difference(self, other)


class BinaryOperation(Signal[S]):
    _current: Optional[S]

    def __init__(self, first: Signal[R], second: Signal[R], op: Callable[[R, R], S]):
        super().__init__()
        self._first = first
        self._second = second
        self._op = op
        self._current = None
        self._first.subscribe(self._update)
        self._second.subscribe(self._update)

    def get(self) -> Optional[S]:
        return self._current

    def _update(self, new: Event[R]) -> S:
        x = self._first.get()
        y = self._second.get()
        if x is not None and y is not None:
            self._current = self._op(x, y)
            self._notify(project(new, lambda _: self._current))  # type: ignore
        return self._current  # type: ignore


def Difference(first: Signal[float], second: Signal[float]):
    return BinaryOperation(first, second, lambda x, y: x - y)


class LastEvent(Signal[S]):
    _current: Optional[Event[S]]

    def __init__(self):
        super().__init__()
        self._current = None

    def get(self) -> Optional[S]:
        if self._current is None:
            return None
        return self._current.value  # type: ignore

    def update(self, new: Event[S]) -> S:
        self._current = new
        self._notify(new)
        return self._current.value  # type: ignore


class Project(Generic[R, S], Signal[S]):
    _current: Optional[Event[S]]

    def __init__(self, fn: events.Project[R, S], signal: Signal[R]):
        super().__init__()
        self._current = None
        self._fn = fn
        self._signal = signal
        signal.subscribe(self._update)

    def get(self) -> Optional[S]:
        if self._current is None:
            return None
        # pylint: disable=no-member
        return self._current.value  # type: ignore

    def _update(self, new: Event[R]) -> S:
        self._current = events.project(new, self._fn)
        self._notify(self._current)
        # pylint: disable=no-member
        return self._current.value  # type: ignore


class Select(Signal[S]):
    _events: events.Queue[S]
    _current: Optional[Event[S]]
    _keep: int

    def __init__(self, signal: Signal[S], select: events.Select[S], keep: timedelta):
        super().__init__()
        self._events = events.Queue()
        self._select = select
        self._keep = int(keep.total_seconds() * 1000)
        self._current = None
        self._signal = signal
        signal.subscribe(self._update)

    def _update(self, new: Event[S]) -> S:
        if self._current is not None:
            updated = self._select(self._current, new)
        else:
            updated = new

        self._events.append(new)
        before = new.occurred_at - self._keep
        self._events.take(before)
        if updated.occurred_at < before:
            updated = self._recompute()
        if updated != self._current:
            self._current = updated
            self._notify(self._current)
        return self._current.value  # type: ignore

    def get(self) -> Optional[S]:
        if self._current is not None:
            return self._current.value  # type: ignore
        return None

    def _recompute(self) -> Event[S]:
        it = iter(self._events)
        try:
            selected = next(it)
        except StopIteration:
            # TODO: Change exception type
            raise exceptions.WireException()
        for event in it:
            selected = self._select(selected, event)
        return selected


class Fold(Generic[R, S], Signal[S]):
    _acc: S

    def __init__(self, signal: Signal[R], fold: events.Fold[S, R], initial: S):
        super().__init__()
        self._signal = signal
        self._fold = fold
        self._acc = initial
        self._signal = signal
        signal.subscribe(self._update)

    def _update(self, new: Event[R]):
        self._acc = self._fold(self._acc, new)
        self._notify(project(new, lambda _: self._acc))

    def get(self) -> Optional[S]:
        return self._acc


Number = Union[float, int]


class Sum(Signal[Number]):
    _events: events.Queue[Number]
    _current: Number
    _keep: int

    def __init__(self, signal: Signal[Number], keep: timedelta):
        super().__init__()
        self._events = events.Queue()
        self._keep = int(keep.total_seconds() * 1000)
        self._current = 0
        self._signal = signal
        signal.subscribe(self._update)

    def get(self) -> Optional[Number]:
        return self._current

    def _update(self, new: Event[Number]) -> Number:
        self._current += new.value
        self._events.append(new)
        before = new.occurred_at - self._keep
        dropped = self._events.take(before)
        for event in dropped:
            self._current -= event.value
        self._notify(project(new, lambda _: self._current))
        return self._current
