import threading


class CallBackThread(threading.Thread):
    """A thread that contains a callback when the thread has finished running"""

    def __init__(self, target, callback=None, exception_callback=None, *args, **kwargs):
        if not callable(target):
            raise TypeError('expected callable function, not {0}'.format(type(target)))

        if callback is not None and not callable(callback):
            raise TypeError('expected callable function, not {0}'.format(type(callback)))

        if exception_callback is not None and not callable(exception_callback):
            raise TypeError('expected callable function, not {0}'.format(type(exception_callback)))

        super(CallBackThread, self).__init__(target=self.__callback_target, *args, **kwargs)
        self.callback = callback
        self.exception_callback = exception_callback
        self.method = target

    def __callback_target(self):
        try:
            self.method()
            if self.callback is not None:
                self.callback()
        except Exception as e:
            if self.exception_callback is not None:
                self.exception_callback(e)
