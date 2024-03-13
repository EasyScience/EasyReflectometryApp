# CHANGELOG

### Changes 0.0.9

- Changes to make the MacOS version runable

### Changes 0.0.8

- Just a retry of the release protocol

### Changes 0.0.7

- No end-user related changes  

### Changes 0.0.6

- Enable plotting of reflectometry data with a logarithmic q-axes [6c26411](https://github.com/easyScience/EasyReflectometryApp/commit/6c26411c5a4d4f412ce475b16d64e0c46a040e55)
- Automatic transition to Sample tab after "Continue without project [31dfe4d](https://github.com/easyScience/EasyReflectometryApp/commit/31dfe4d6e3b2823bcc5420d26573a6cf5e20bad7)
- Remove private repo access set from CI [f706d2a](https://github.com/easyScience/EasyReflectometryApp/pull/98/commits/f706d2af0aec333a9653616a1b88a7a51831d12c)
- Modified the data loader to handle tab and comma separated datasets, as well as raising a type error if unable to load [20ca60b](https://github.com/easyScience/EasyReflectometryApp/pull/97/commits/20ca60b1fe65af0489fb68f835cf46da93f662fd)
- Fixed bug in loading/saving of project [7b49266](https://github.com/easyScience/EasyReflectometryApp/pull/104/commits/7b49266782ab056a763bd0929d022d16f6c2ff22)
- Add scale and background lines to Experiment and Analysis plots [c646de8](https://github.com/easyScience/EasyReflectometryApp/commit/c646de81fffb309531b540cc6a972cb3fc2d02ea)
- Update to use EasyCore-0.3.0 [751dd43](https://github.com/easyScience/EasyReflectometryApp/commit/751dd43b6cd9b1c9ad1b1cb0c2a6adb14703f20c)
- Fix bug in saving project caused by stale proxy locations [4468e5c](https://github.com/easyScience/EasyReflectometryApp/commit/4468e5cb1b35d35676fa65c3f022f51e7e193407)
- New continuous integration methodology [faa857d](https://github.com/easyScience/EasyReflectometryApp/commit/faa857df7e59bbe16388921ca720882cafdf1a2e)
- Building of snapcast images [9e970d4](https://github.com/easyScience/EasyReflectometryApp/commit/9e970d4062b2efc07267e7202ea4db28cb836b44)


### Changes 0.0.5

- Addition of multiple contrast support [091abe1](https://github.com/easyScience/EasyReflectometryApp/pull/79/commits/091abe1b727c7b9e1f1b60ed1327d79ef318dd8e)
- Saving and loading fixed [598e7f3](https://github.com/easyScience/EasyReflectometryApp/pull/79/commits/598e7f36ef5feb6263ed015e13002528c15b03b9)
- Enabling parameter-parameter constraints to be defined [82e3821](https://github.com/easyScience/EasyReflectometryApp/pull/79/commits/82e382141e8e5b469e89fe42ca397c21bd194fcc)
- Clean up of the sample interface [3907bde](https://github.com/easyScience/EasyReflectometryApp/pull/79/commits/3907bde69d608be6b82051c60bb7a304f04f0002)
- Enabling the docs and bug reporting buttons [7d29276](https://github.com/easyScience/EasyReflectometryApp/pull/79/commits/7d292761e96860b5b8ce74365174e38f79bbaf80)
- Fix the reset state button [a1db4ac](https://github.com/easyScience/EasyReflectometryApp/pull/79/commits/a1db4ac10bbd5f90c764f28336cbfecb26671a03)
- Parameter quick filters [27a64b6](https://github.com/easyScience/EasyReflectometryApp/pull/79/commits/27a64b615d016713478817119e45133b4af50695)
- Start using easyApp [5e38ef8](https://github.com/easyScience/EasyReflectometryApp/commit/5e38ef8bd6fa542edd89e3c687d3a84dcc803800)
- Add plotting in R(q)q^4 [5e38ef8](https://github.com/easyScience/EasyReflectometryApp/commit/5e38ef8bd6fa542edd89e3c687d3a84dcc803800)
- Make the plots colourful to match the model colours [225ac06](https://github.com/easyScience/EasyReflectometryApp/pull/81/commits/225ac06cd7a72ba91a71e1c339c774fa351f1802)
- Disable the fitting button if no parameters are `fixed == False` [45be44c](https://github.com/easyScience/EasyReflectometryApp/pull/90/commits/45be44c35cdfefa6e311929cdf2ab4a0512b88f6)
- Saving plots to a single pdf [da7eba6](https://github.com/easyScience/EasyReflectometryApp/pull/89/commits/da7eba6c2acc23dd9b04d2fc5b51e3421e913820)
- Remove the colour from the materials as it isn't used [7a40613](https://github.com/easyScience/EasyReflectometryApp/pull/88/commits/7a40613d07a021f0440a46105843f9fabe945430)

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
