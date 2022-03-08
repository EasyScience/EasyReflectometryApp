from PySide2.QtCore import Signal, QThread


class Fitter(QThread):
    """
    Simple wrapper for calling a function in separate thread
    """
    failed = Signal(str)
    finished = Signal(dict)

    def __init__(self, parent, obj, method_name, *args, **kwargs):
        QThread.__init__(self, parent)
        self._obj = obj
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs

    def run(self):
        res = {}
        if hasattr(self._obj, self.method_name):
            func = getattr(self._obj, self.method_name)
            try:
                res = func(*self.args, **self.kwargs)
            except Exception as ex:
                self.failed.emit(str(ex))
                return str(ex)
            self.finished.emit(res)
        return res

    def stop(self):
        self.terminate()
        self.wait()  # to assure proper termination
