from . import timework as tw

import time


def test_no_split():
    """
    output example:
      [TIMEWORK] Start:  Mon Feb  8 04:11:38 2021
      [TIMEWORK] Stop:   00:00:01.438
      [TIMEWORK] Finish: Mon Feb  8 04:11:41 2021
    """
    for _ in range(3):
        with tw.Stopwatch() as s:
            assert -.1 < s._initial - time.time() < .1
            time.sleep(.3)
            assert s._running is True
            s.pause()
            assert s._running is False
            time.sleep(.4)
            assert s._running is False
            s.resume()
            assert s._running is True
            time.sleep(.5)
            split, total = s.get_hms()
            assert split == total
            assert split == tw.sec_to_hms(tw.hms_to_sec(total))
            time.sleep(.6)
            assert s._running is True
            s.stop()
            assert s._running is False
            time.sleep(.7)


def test_split():
    """
    output example:
      [TIMEWORK] Start:  Mon Feb  8 04:03:13 2021
      [TIMEWORK] Split:  00:00:00.804 | 00:00:00.804
      [TIMEWORK] Split:  00:00:01.411 | 00:00:00.606
      [TIMEWORK] Stop:   00:00:02.114 | 00:00:00.703
      [TIMEWORK] Finish: Mon Feb  8 04:03:16 2021
    """
    for _ in range(3):
        with tw.Stopwatch() as s:
            assert s._running is True
            time.sleep(.3)
            s.pause()
            assert s._running is False
            time.sleep(.4)
            s.resume()
            assert s._running is True
            time.sleep(.5)
            s.split()
            assert s._start_at != s._initial
            time.sleep(.6)
            s.split()
            assert s._start_at - s._initial > .6
            time.sleep(.7)
            assert s._running is True


def test_restart():
    """
    output example:
      [TIMEWORK] Start:  Mon Feb  8 17:14:57 2021
      [TIMEWORK] Split:  00:00:00.312 | 00:00:00.312
      [TIMEWORK] Stop:   00:00:01.119
      [TIMEWORK] Stop:   00:00:00.709
      [TIMEWORK] Finish: Mon Feb  8 17:15:00 2021
    """
    for _ in range(3):
        with tw.Stopwatch() as s:
            assert s._running is True
            time.sleep(.3)
            s.split()
            time.sleep(.4)
            s.restart()
            assert s._running is True
            time.sleep(.5)
            split, total = s.get_sec()
            assert total < .6
            time.sleep(.6)
            s.stop()
            assert s._running is False
            s.restart()
            time.sleep(.7)
            assert s._running is True
