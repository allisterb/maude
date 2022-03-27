# Based on https://realpython.com/python-timer/
from distutils.log import debug
import time
from logging import info, error

from .runtime import exception_handler

class TimerException(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:
    def __init__(self, elapsed_text="Elapsed time: {:0.2f} seconds"):
        self._start_time = None
        self.elapsed_text = elapsed_text
        self.completed=False
    
    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerException(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerException(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        if self.op == '':
            print(self.text.format(elapsed_time))
        else:
            pass

class Op:
    def __init__(self, op):
        self._start_time = 0.0
        self.op = op
        self.completed_text= op + " completed in {:0.2f} s."
        self.completed = False
        self.abandoned = False
        self.abandoned_text= op + " abadoned after {:0.2f} s."

    def complete(self):
        self.elapsed_time = time.perf_counter() - self._start_time
        self.completed = True
        info(self.completed_text.format(self.elapsed_time))

    def abandon(self):
        if not self.completed:
            self.abandoned = True
            self.elapsed_time = time.perf_counter() - self._start_time
            error(self.abandoned_text.format(self.elapsed_time))
        else:
            raise TimerException(f"Operation {self.op} has already completed.")
    
    def __enter__(self):
        info(self.op + '...')
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, ex_type, ex, tb):
        if not (self.completed or self.abandoned):
            if (ex is not None): 
                debug(f'Exception raised in context: {ex}')
                exception_handler(ex_type, ex, tb)
            self.abandon()
            return ex is None
        
def begin(op): return Op(op)