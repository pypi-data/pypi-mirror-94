from highwire.events import Event


def ema(factor: float):
    def fn(acc: float, event: Event[float]):
        return acc * factor + event.value

    return fn
