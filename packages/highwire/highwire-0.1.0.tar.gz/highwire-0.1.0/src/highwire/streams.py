from typing import Any, AsyncIterator, Callable, Iterator, Mapping, Optional, Tuple, TypeVar

from highwire.events import Event

S = TypeVar("S")

AsyncStream = AsyncIterator[Event[S]]
Stream = Iterator[Event[S]]


def tick(start: int, delay: int, it: Optional[Iterator[S]] = None) -> Stream[S]:
    return arrivals(start, lambda: delay, it)


def arrivals(
    start: int, delay: Callable[[], int], it: Optional[Iterator[S]] = None
) -> Stream[S]:
    def nats():
        i = 0
        while True:
            yield i
            i += 1

    it = it or nats()
    current = start
    for i in it:
        yield Event(value=i, occurred_at=current, received_at=current)
        current += delay()


def merge(*streams: Stream[Any]) -> Stream[Any]:
    def head(stream):
        try:
            return next(stream)
        except StopIteration:
            return None

    def first_by_index(events):
        i_ = None
        for (i, event) in enumerate(events):
            if event is not None:
                if i_ is None:
                    i_ = i
                else:
                    if pending[i_].occurred_at > pending[i].occurred_at:
                        i_ = i
        return i_

    pending = [head(s) for s in streams]
    while True:
        i = first_by_index(pending)
        if i is None:
            break
        yield pending[i]
        pending[i] = head(streams[i])


K = TypeVar("K")


def keyed_merge(
    streams: Mapping[K, Stream[Any]], ticks: Tuple[K, Optional[int]] = None
) -> Iterator[Tuple[K, Event[Any]]]:
    def head(stream):
        try:
            return next(stream)
        except StopIteration:
            return None

    def first_by_index(events):
        k_ = None
        has_event = False
        for (k, event) in events.items():
            if event is not None:
                if k != ticks[0]:
                    has_event = True
                if k_ is None:
                    k_ = k
                else:
                    if pending[k_].occurred_at > pending[k].occurred_at:
                        k_ = k
        if has_event:
            return k_
        return None

    pending = {k: head(s) for (k, s) in streams.items()}
    k = first_by_index(pending)
    if k is None:
        return
    yield (k, pending[k])
    current_tick = pending[k].occurred_at
    pending[k] = head(streams[k])
    if ticks:
        occurred_at = current_tick + ticks[1]
        pending[ticks[0]] = Event(value=None, received_at=occurred_at, occurred_at=occurred_at)
    while True:
        k = first_by_index(pending)
        if k is None:
            break
        yield (k, pending[k])
        if ticks and k == ticks[0]:
            occurred_at = pending[k].occurred_at + ticks[1]
            pending[k] = Event(value=None, received_at=occurred_at, occurred_at=occurred_at)
        else:
            pending[k] = head(streams[k])
