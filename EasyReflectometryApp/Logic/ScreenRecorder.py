import mss
import cv2
import time
import numpy as np
from threading import Thread
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QApplication


class ScreenRecorder(QObject):

    recordingFinished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.frame_rate = 12
        self.video_codec_name = 'mp4v'
        self.out_file_name = 'tutorial'

        self.device_pixel_ratio = QApplication.primaryScreen().devicePixelRatio()
        self.screen_size = QApplication.primaryScreen().size()
        self.screen_rect = QApplication.primaryScreen().geometry()

        self.mss_frame_rect = self.default_mss_frame_rect()

        self.is_recording_now = False
        self.recording_thread = Thread(target=self.recording)

        self.recordingFinished.connect(self.onRecordingFinished)
        QApplication.instance().aboutToQuit.connect(self.onAboutToQuit)

    # https://gist.github.com/takuma7/44f9ecb028ff00e2132e
    def codec_to_ext(self, codec_name):
        return {
            'mp4v': 'mp4',  # macOS: +, GitHub macOS: +
            'avc1': 'mp4'  # macOS: +, GitHub macOS: -
        }[codec_name]

    def cv2_video_codec(self):
        return cv2.VideoWriter_fourcc(*self.video_codec_name)

    def cv2_frame_size(self):
        return (
            int(self.mss_frame_rect['width'] * self.device_pixel_ratio),
            int(self.mss_frame_rect['height'] * self.device_pixel_ratio)
        )

    def cv2_out_file_name(self):
        return self.out_file_name + '.' + self.codec_to_ext(self.video_codec_name)

    def default_mss_frame_rect(self):
        return {
            'top': self.screen_rect.y(),
            'left': self.screen_rect.x(),
            'width': self.screen_rect.width(),
            'height': self.screen_rect.height()
        }

    def set_mss_frame_rect(self, frame_rect=None, margin_rect=None):
        if frame_rect is None:
            self.mss_frame_rect = self.default_mss_frame_rect()
            return
        self.mss_frame_rect = frame_rect.toVariant()
        self.set_mss_frame_rect_margins(margin_rect)

    def set_mss_frame_rect_margins(self, margin_rect=None):
        if margin_rect is None:
            return
        margin_rect = margin_rect.toVariant()
        self.mss_frame_rect['top'] -= margin_rect['top']
        self.mss_frame_rect['left'] -= margin_rect['left']
        self.mss_frame_rect['width'] += margin_rect['left'] + margin_rect['right']
        self.mss_frame_rect['height'] += margin_rect['top'] + margin_rect['bottom']
        if self.mss_frame_rect['top'] < 0:
            self.mss_frame_rect['top'] = 0
        if self.mss_frame_rect['left'] < 0:
            self.mss_frame_rect['left'] = 0
        if self.mss_frame_rect['left'] + self.mss_frame_rect['width'] > self.screen_rect.width():
            self.mss_frame_rect['width'] = self.screen_rect.width() - self.mss_frame_rect['left']
        if self.mss_frame_rect['top'] + self.mss_frame_rect['height'] > self.screen_rect.height():
            self.mss_frame_rect['height'] = self.screen_rect.height() - self.mss_frame_rect['top']

    def recording(self):
        out = cv2.VideoWriter(
            self.cv2_out_file_name(),
            self.cv2_video_codec(),
            self.frame_rate,
            self.cv2_frame_size()
        )
        with mss.mss() as sct:
            while self.is_recording_now:
                # collect start time
                start_time = time.time()
                # grab and save screenshot
                screenshot = sct.grab(self.mss_frame_rect)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)
                # collect end time
                end_time = time.time()
                # calculate time to wait before next frame
                desired_time = 1 / self.frame_rate
                real_time = end_time - start_time
                delay = desired_time - real_time
                if delay > 0:
                    time.sleep(delay)
        cv2.destroyAllWindows()
        out.release()
        self.recordingFinished.emit()

    @Slot('QVariant', 'QVariant')
    def startRecording(self, frame_rect=None, margin_rect=None):
        self.set_mss_frame_rect(frame_rect, margin_rect)
        if not self.recording_thread.is_alive():
            self.is_recording_now = True
            self.recording_thread.start()

    @Slot()
    def stopRecording(self):
        self.is_recording_now = False

    def onRecordingFinished(self):
        if self.recording_thread.is_alive():
            self.recording_thread.join()

    def onAboutToQuit(self):
        pass
