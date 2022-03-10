import sys

from PySide2.QtCore import Signal, QThread, QObject, Property, Slot

from easyCore import borg
from easyCore.Fitting.Fitting import Fitter as easyFitter

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


class FitterProxy(QObject):

    fitFinished = Signal()
    fitFinishedNotify = Signal()
    fitResultsChanged = Signal()

    stopFit = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._fit_finished = True
        self._fit_results = self._defaultFitResults()
        self._fitter_thread = None
        self.eFitter = easyFitter(self.parent._model_proxy._model, self.parent._interface.fit_func)

        self.fitFinished.connect(self._onFitFinished)
        self.stopFit.connect(self.onStopFit)

    # # #
    # Defaults
    # # # 

    def _defaultFitResults(self):
        return {
            "success": None,
            "nvarys":  None,
            "GOF":     None,
            "redchi2": None
        }

    # # #
    # Setters and getters
    # # #

    @Property(bool, notify=fitFinishedNotify)
    def isFitFinished(self):
        return self._fit_finished

    @isFitFinished.setter
    def isFitFinished(self, fit_finished: bool):
        if self._fit_finished == fit_finished:
            return
        self._fit_finished = fit_finished
        self.fitFinishedNotify.emit()

    @Property('QVariant', notify=fitResultsChanged)
    def fitResults(self):
        return self._fit_results

    def _setFitResults(self, res):
        self._fit_results = {
            "success": res.success,
            "nvarys":  res.n_pars,
            "GOF":     float(res.goodness_of_fit),
            "redchi2": float(res.reduced_chi)
        }
        self.fitResultsChanged.emit()
        self.isFitFinished = True
        self.fitFinished.emit()

    def _setFitResultsFailed(self, res):
        self.isFitFinished = True

    # # # 
    # Actions
    # # # 

    def _onFitFinished(self):
        self.parent.parametersChanged.emit()

    # # #
    # Slots
    # # #

    @Slot()
    def fit(self):
        # if running, stop the thread
        if not self.isFitFinished:
            self.onStopFit()
            borg.stack.endMacro()  # need this to close the undo stack properly
            return
        # macos is possibly problematic with MT, skip on this platform
        if 'darwin' in sys.platform:
            self.nonthreaded_fit()
        else:
            self.threaded_fit()

    # # # 
    # Methods
    # # #

    def nonthreaded_fit(self):
        self.isFitFinished = False
        exp_data = self.parent._data_proxy._data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.ye
        method = self.parent._current_minimizer_method_name

        res = self.eFitter.fit(x, y, weights=weights, method=method)
        self._setFitResults(res)

    def threaded_fit(self):
        self.isFitFinished = False
        exp_data = self.parent._data_proxy._data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.ye
        method = self._current_minimizer_method_name

        args = (x, y)
        kwargs = {"weights": weights, "method": method}
        self._fitter_thread = Fitter(self, self.eFitter, 'fit', *args, **kwargs)
        self._fitter_thread.setTerminationEnabled(True)
        self._fitter_thread.finished.connect(self._setFitResults)
        self._fitter_thread.failed.connect(self._setFitResultsFailed)
        self._fitter_thread.start()

    def onStopFit(self):
        """
        Slot for thread cancelling and reloading parameters
        """
        self.stop_fit()
        self._fitter_thread = None

        self._fit_results['success'] = 'cancelled'
        self._fit_results['nvarys'] = None
        self._fit_results['GOF'] = None
        self._fit_results['redchi2'] = None
        self._setFitResultsFailed("Fitting stopped")

    def stop_fit(self):
        self._fitter_thread.stop()