from pathlib import Path

from easyreflectometry import Project as ProjectLib
from easyreflectometry.summary import Summary as SummaryLib


class Summary:
    def __init__(self, project_lib: ProjectLib):
        self._created = True

        self._project_lib = project_lib
        self._summary = SummaryLib(project_lib)
        self._file_name = 'summary'

    @property
    def created(self) -> bool:
        return self._created

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, value: str) -> None:
        self._file_name = value

    @property
    def file_path(self) -> Path:
        return self._project_lib.path / self._file_name

    @property
    def as_html(self) -> str:
        return self._summary.compile_html_summary()

    def save_as_html(self) -> None:
        if not self._project_lib.path.exists():
            self._project_lib.path.mkdir(parents=True, exist_ok=True)
        self._summary.save_html_summary(self.file_path.with_suffix('.html'))

    def save_as_pdf(self) -> None:
        if not self._project_lib.path.exists():
            self._project_lib.path.mkdir(parents=True, exist_ok=True)
        self._summary.save_pdf_summary(self.file_path.with_suffix('.pdf'))
