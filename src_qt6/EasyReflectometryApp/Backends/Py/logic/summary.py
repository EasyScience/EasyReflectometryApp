from easyreflectometry import Project as ProjectLib
from pathlib import Path

class Summary:
    def __init__(self, project_lib: ProjectLib):
        self._project_lib = project_lib
        self._created = True
        self._file_name = "summary"

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
        return _PY_HTML

    def save_as_html(self) -> None:
        print("Saving as HTML")

    def save_as_pdf(self) -> None:
        print("Saving as PDF")


_PY_HTML = """<!DOCTYPE html>
<html>
<style>
th, td { padding-right: 18px; }
    th { text-align: left; }
</style>
<body>
    <table>
    <tr></tr>
    <tr>
        <td><h1>Py Summary</h1></td>
    </tr>
    <tr></tr>
    <tr>
        <td><h3>Project information</h3></td>
    </tr>
    <tr></tr>
    <tr>
        <th>Title</th>
        <th>La0.5Ba0.5CoO3</th>
    </tr>
    <tr>
        <td>Description</td>
        <td>neutrons, powder, constant wavelength</td>
    </tr>
    <tr>
        <td>No. of phases</td>
        <td>1</td>
    </tr>
    <tr>
        <td>No. of experiments</td>
        <td>1</td>
    </tr>
    <tr></tr>
        <tr>
            <td><h3>Crystal data</h3></td>
        </tr>
        <tr></tr>
    <tr>
        <th>Phase datablock</th>
        <th>lbco</th>
    </tr>
    <tr>
        <td>Crystal system, space group</td>
        <td>cubic,&nbsp;&nbsp;<i>P m -3 m</i></td>
    </tr>
    <tr></tr>
        <tr>
            <td><h3>Data collection</h3></td>
        </tr>
        <tr></tr>
    <tr>
        <th>Experiment datablock</th>
        <th>hrpt</th>
    </tr>
    <tr>
        <td>Radiation probe</td>
        <td>neutron</td>
    </tr>
    <tr>
        <td>Measured range: min, max, inc (&deg;)</td>
        <td>10.0,&nbsp;&nbsp;164.85,&nbsp;&nbsp;0.05</td>
    </tr>
    <tr></tr>
    </table>
</body>
</html>
"""