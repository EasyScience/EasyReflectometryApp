# CHANGELOG

### Changes 0.0.4

- Add min and max columns to the Analysis tab [da47432](https://github.com/easyScience/EasyReflectometryApp/commit/da47432db1bec0e16e587328a24c23bdd174c099)
- Improvement to Analysis tab to ensure parameters are only listed once [f67eb02](https://github.com/easyScience/EasyReflectometryApp/commit/f67eb023aa18ebed41d5b19c719da5d6896d14b3)
- Introduction of the 'Surfactant Layer' item type [91ef5f1](https://github.com/easyScience/EasyReflectometryApp/commit/91ef5f152af6160a48dc39e3cfaf99447bf06aea) and [dcc9297](https://github.com/easyScience/EasyReflectometryApp/commit/dcc9297946253f74d2101dcc741ad452b850b237)
- Improvements to the efficiency of the Sample tab by divorcing the Materials/Items/Layers where possible [e57e5c3](https://github.com/easyScience/EasyReflectometryApp/commit/e57e5c367da783020a67b2335c32f01317429ae9)
- Refactor of the internal logic proxy object `PyQmlProxy.py` into a variety of `Proxies` [3abdb40](https://github.com/easyScience/EasyReflectometryApp/commit/3abdb40f7b9e5b35754061395c939d61dfc4d9d4)
- Deactivation of 'qtcharts' plotting
- Removal of more old EasyDiffraction GUI code
- Solve problem when number of iterations was changed in a RepeatingMultiLayer ([issue #18](https://github.com/easyScience/EasyReflectometryApp/issues/18)))
- Enable the data plotted in the Sample tab to be pure reflectometry (i.e. scaling of one, no background or resolution) ([issue #66](https://github.com/easyScience/EasyReflectometryApp/issues/66))
- Move to BSD license

### Changes 0.0.3

- Change name from 'easyReflectometry' to 'EasyReflectometry'

### Changes 0.0.2

- A bug fix to enable multithreaded fitting to work on Windows and Linux
