__author__ = 'github.com/arm61'

from PySide2.QtCore import Signal
from PySide2.QtCore import QThread
from PySide2.QtCore import QObject
from PySide2.QtCore import Property
from PySide2.QtCore import Slot

from easyscience import global_object

from easyreflectometry.fitting import MultiFitter as easyFitter


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
    sampleChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self._fit_finished = True
        self._fit_results = self._defaultFitResults()
        self._fitter_thread = None

        self.eFitter = easyFitter(*[i for i in self.parent._model_proxy._model])

        self.fitFinished.connect(self._onFitFinished)
        self.stopFit.connect(self.onStopFit)

    # # #
    # Defaults
    # # #

    def _defaultFitResults(self):
        return {"success": None, "nvarys": None, "chi2": None}

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
        success = []
        n_pars = []
        chi2 = []
        for r in res:
            success.append(r.success)
            n_pars.append(r.n_pars)
            chi2.append(r.chi2)
        self._fit_results = {
            "success": all(success),
            "nvarys": sum(n_pars),
            "chi2": float(sum(chi2))
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
        self.parent.sampleChanged.emit()

    # # #
    # Slots
    # # #

    @Slot()
    def fit(self):
        # if running, stop the thread
        if not self.isFitFinished:
            self.onStopFit()
            global_object.stack.endMacro()  # need this to close the undo stack properly
            return
        # macos is possibly problematic with MT, skip on this platform
        # if 'darwin' in sys.platform:
        self.nonthreaded_fit()
        # else:
        #     self.threaded_fit()

    # # #
    # Methods
    # # #

    def nonthreaded_fit(self):
        self.eFitter = easyFitter(*[i.model for i in self.parent._data_proxy._data])
        self.isFitFinished = False
        exp_data = self.parent._data_proxy._data.experiments

        x = [i.x for i in exp_data]
        y = [i.y for i in exp_data]
        weights = [1 / i.ye for i in exp_data]
        method = self.parent.minimizer._current_minimizer.method

        res = self.eFitter.easy_science_multi_fitter.fit(x, y, weights=weights, method=method)
        self._setFitResults(res)

    # def threaded_fit(self):
    #     self.isFitFinished = False
    #     exp_data = self.parent._data_proxy._data.experiments[0]

    #     x = exp_data.x
    #     y = exp_data.y
    #     weights = 1 / exp_data.ye
    #     method = self.parent.minimizer._current_minimizer_method_name

    #     args = (x, y)
    #     kwargs = {"weights": weights, "method": method}
    #     self._fitter_thread = Fitter(self, self.eFitter, 'fit', *args, **kwargs)
    #     self._fitter_thread.setTerminationEnabled(True)
    #     self._fitter_thread.finished.connect(self._setFitResults)
    #     self._fitter_thread.failed.connect(self._setFitResultsFailed)
    #     self._fitter_thread.start()

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

    def _onSampleChanged(self):
        print(">>> Sample changed")
        self.sampleChanged.emit()  # this signal has no slots!

    