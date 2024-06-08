from .base import *

from . import (
    events,
    pgapi
)


TIMEOUTS: list[Timeout] = []


@events.update
def update() -> None:
    for to in structured_clone(TIMEOUTS):
        if to.interval + to.start_time < pgapi.TIME.current:
            to.fn(*to.args)
            TIMEOUTS.remove(to)


def new(interval: Number, fn: Callable[..., None], args: Tuple) -> None:
    TIMEOUTS.append(
        Timeout(interval=interval, fn=fn, args=args, start_time=pgapi.TIME.current)
    )
