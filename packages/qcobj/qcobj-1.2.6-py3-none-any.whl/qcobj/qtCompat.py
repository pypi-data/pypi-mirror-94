""" The main initialization of our PySide6/PySide2/PyQt5 Package.

    Warning:
        This module tries to import PySide2 if available, else tries
        to load PySide6 or PyQt5.

    Note:
        Define environment variable **QT_PREFERRED_LIB** to change
        this behaviour.

        - **QT_PREFERRED_LIB=PyQt5** for PyQt5
        - **QT_PREFERRED_LIB=PySide2** for PySide2

    Author:
        - 2009-2020 Roberto Vidmar

    Copyright:
        2011-2020 Roberto Vidmar <rvidmar@inogs.it>

    License:
        MIT/X11 License (see :download:`license.txt <../../license.txt>`)
"""
import os
import sys
from pkgutil import iter_modules

QT_PREFERRED_LIB = os.environ.get('QT_PREFERRED_LIB', '')
if QT_PREFERRED_LIB:
    QT_LIB = QT_PREFERRED_LIB
else:
    # Search among available
    available = [p.name for p in iter_modules() if p.ispkg]
    if "PySide2" in available:
        QT_LIB = "PySide2"
    elif "PySide6" in available:
        QT_LIB = "PySide6"
    elif "PyQt5" in available:
        QT_LIB = "PyQt5"
    else:
        QT_LIB = None

if QT_LIB is None:
    raise SystemExit("\n%s: ERROR! PyQt5/PySide2/PySide6 not installed.\n"
                % __name__)
elif QT_LIB == "PyQt5":
    try:
        import PyQt5.QtCore as _QtCore
        import PyQt5.QtGui as _QtGui
        import PyQt5.QtWidgets as _QtWidgets
        import PyQt5.QtOpenGL as _QtOpenGL
    except ImportError:
        LIB = None
    else:
        LIB = "PyQt5"
elif QT_LIB == "PySide2":
    try:
        import PySide2.QtCore as _QtCore
        import PySide2.QtGui as _QtGui
        import PySide2.QtWidgets as _QtWidgets
        import PySide2.QtOpenGL as _QtOpenGL
    except ImportError:
        LIB = None
    else:
        LIB = "PySide2"
elif QT_LIB == "PySide6":
    try:
        import PySide6.QtCore as _QtCore
        import PySide6.QtGui as _QtGui
        import PySide6.QtWidgets as _QtWidgets
        import PySide6.QtOpenGL as _QtOpenGL
    except ImportError:
        LIB = None
    else:
        LIB = "PySide6"
else:
    raise SystemExit("\n%s: ERROR! QT_PREFERRED_LIB=%s not supported.\n"
                % (__name__, QT_PREFERRED_LIB))

if LIB is None:
    raise SystemExit("\n%s: ERROR! Library %s could not be imported!\n"
                % (__name__, QT_LIB))

QtWidgets = _QtWidgets
QtCore = _QtCore
QtGui = _QtGui
QtOpenGL = _QtOpenGL

if LIB in "PySide2 PySide6".split():
    Signal = QtCore.Signal
    Slot = QtCore.Slot
    Property = QtCore.Property

    def getOpenFileName(*args, **kargs):
        """ Wrap to PySide QtWidgets.QFileDialog.getOpenFileName
        """
        pn, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(*args,
                **kargs)
        return pn

    def getOpenFileNames(*args, **kargs):
        """ Wrap to PySide QtWidgets.QFileDialog.getOpenFileNames
        """
        pn, selectedFilter = QtWidgets.QFileDialog.getOpenFileNames(*args,
                **kargs)
        return pn

    def getSaveFileName(*args, **kargs):
        """ Wrap to PySide QtWidgets.QFileDialog.getSaveFileName
        """
        pn, selectedFilter = QtWidgets.QFileDialog.getSaveFileName(*args,
                **kargs)
        return pn
else:
    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
    Property = QtCore.pyqtProperty

    def getOpenFileName(*args, **kargs):
        """ Wrap to PyQt4 QtWidgets.QFileDialog.getOpenFileName
        """
        return QtWidgets.QFileDialog.getOpenFileName(*args, **kargs)

    def getOpenFileNames(*args, **kargs):
        """ Wrap to PyQt4 QtWidgets.QFileDialog.getOpenFileNames
        """
        return QtWidgets.QFileDialog.getOpenFileNames(*args, **kargs)

    def getSaveFileName(*args, **kargs):
        """ Wrap to PyQt4 QtWidgets.QFileDialog.getSaveFileName
        """
        return QtWidgets.QFileDialog.getSaveFileName(*args, **kargs)

    QtCore.pyqtRemoveInputHook()

if LIB == "PySide6":
    from PySide6.QtOpenGLWidgets import QOpenGLWidget
    from PySide6.QtGui import QSurfaceFormat as QGLFormat
    QAction = QtGui.QAction
else:
    QOpenGLWidget = QtWidgets.QOpenGLWidget
    QGLFormat = QtOpenGL.QGLFormat
    QAction = QtWidgets.QAction

Qt = QtCore.Qt
