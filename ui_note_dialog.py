# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/enrico/Documenti/plugins/redLayer/ui_note_dialog.ui'
#
# Created: Thu Mar 12 01:02:15 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_noteDialog(object):
    def setupUi(self, noteDialog):
        noteDialog.setObjectName(_fromUtf8("noteDialog"))
        noteDialog.resize(323, 105)
        self.horizontalLayout = QtGui.QHBoxLayout(noteDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(noteDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.sourceString = QtGui.QLineEdit(noteDialog)
        self.sourceString.setReadOnly(False)
        self.sourceString.setObjectName(_fromUtf8("sourceString"))
        self.verticalLayout.addWidget(self.sourceString)
        self.buttonBox = QtGui.QDialogButtonBox(noteDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(noteDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), noteDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), noteDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(noteDialog)

    def retranslateUi(self, noteDialog):
        noteDialog.setWindowTitle(_translate("noteDialog", "Dialog", None))
        self.label.setText(_translate("noteDialog", "Note", None))

