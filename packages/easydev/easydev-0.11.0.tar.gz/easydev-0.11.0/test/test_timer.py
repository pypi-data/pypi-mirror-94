from easydev.timer import Timer
import time


def test_timer():

    times = []
    with Timer(times):
        time.sleep(.1)
    assert len(times) == 1
    assert sum(times) <1

    tt = Timer(times)
