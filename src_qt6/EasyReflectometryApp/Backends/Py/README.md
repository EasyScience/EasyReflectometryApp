The code in this folder is a backend implemented in Python that serves a GUI implemented in QML. 
The backend utilizes the EasyReflectometryLib.

# Folder root
The modules in the root folder define the API of the backend.  
The API is used in the GUI through the QML wrapper defined in Gui.Globals.Backend.qml
Pyside is used to handle the integration between the Python backend and the QML GUI.

The entrypoint is the class:
- Backend

This Backend class is a collections of other classes, which each are dedicated to specific pages in the GUI.  
Furthermore the Backend class is responsible for doing the required connections between page specific classes to enable information to be passed between these.

The structure of the folder is to have a module with a class for each of the pages in the GUI.  One can think of each of the classes as the API for the corresponding page in the GUI:
- Home
- Project
- Experiment
- ...

There should NOT be any logic in the modules in the root folder.  Rather the methods should make calls to the modules in the logic folder to provide the functionality of a given API entrypoint.

The syntax of the code in the root folder is a mixture of QML and Python.  

# Logic folder
The modules in the logic folder is to provide the functionality that is needed for the backend to work but which is not generic enough to be in EasyReflectometryLib.

There will often be a match between the logic module and the API module for a page.

There should NOT be any traces of Pyside in the logic folder.

The syntax of the code in the logic folder is Python.
 