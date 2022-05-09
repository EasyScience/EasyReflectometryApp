# CHANGELOG

### Changes 0.0.5

- Fix the reset state button []()

### Changes 0.0.4

- Add min and max columns to the Analysis tab [da47432](https://github.com/easyScience/EasyReflectometryApp/commit/da47432db1bec0e16e587328a24c23bdd174c099)
- Improvement to Analysis tab to ensure parameters are only listed once [f67eb02](https://github.com/easyScience/EasyReflectometryApp/commit/f67eb023aa18ebed41d5b19c719da5d6896d14b3)
- Introduction of the 'Surfactant Layer' item type [91ef5f1](https://github.com/easyScience/EasyReflectometryApp/commit/91ef5f152af6160a48dc39e3cfaf99447bf06aea) and [dcc9297](https://github.com/easyScience/EasyReflectometryApp/commit/dcc9297946253f74d2101dcc741ad452b850b237)
- Improvements to the efficiency of the Sample tab by divorcing the Materials/Items/Layers where possible [e57e5c3](https://github.com/easyScience/EasyReflectometryApp/commit/e57e5c367da783020a67b2335c32f01317429ae9)
- Refactor of the internal logic proxy object `PyQmlProxy.py` into a variety of `Proxies` [3abdb40](https://github.com/easyScience/EasyReflectometryApp/commit/3abdb40f7b9e5b35754061395c939d61dfc4d9d4)
- Removal of more old EasyDiffraction GUI code [9a41c0f](https://github.com/easyScience/EasyReflectometryApp/commit/9a41c0fbd446344b468c78ec220f02c20f56abc9)
- Solve problem when number of iterations was changed in a RepeatingMultiLayer [9542d4d](https://github.com/easyScience/EasyReflectometryApp/commit/9542d4db07d210d178c61503c66f42a666907a61)
- Enable the data plotted in the Sample tab to be pure reflectometry (i.e. scaling of one, no background or resolution) and deactivation of 'qtcharts' plotting [52accc9](https://github.com/easyScience/EasyReflectometryApp/commit/52accc9a062ad2533679cacf778877c05cebf47e)
- Move to BSD license [413bd9b](https://github.com/easyScience/EasyReflectometryApp/commit/413bd9b93cba04b962386ddcd0b697cc9921345c)

### Changes 0.0.3

- Change name from 'easyReflectometry' to 'EasyReflectometry'

### Changes 0.0.2

- A bug fix to enable multithreaded fitting to work on Windows and Linux
