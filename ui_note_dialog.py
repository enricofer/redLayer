# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\documenti\dev\redLayer\ui_note_dialog.ui'
#
# Created: Thu Mar 12 10:35:39 2015
#      by: PyQt4 UI code generator 4.11.3
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
        noteDialog.resize(180, 131)
        self.horizontalLayout = QtGui.QHBoxLayout(noteDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(noteDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.noteText = QtGui.QTextEdit(noteDialog)
        self.noteText.setObjectName(_fromUtf8("noteText"))
        self.verticalLayout.addWidget(self.noteText)
        self.buttonBox = QtGui.QDialogButtonBox(noteDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(noteDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), noteDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), noteDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(noteDialog)

    def retranslateUi(self, noteDialog):
        noteDialog.setWindowTitle(_translate("noteDialog", "Sketch Note", None))
        self.label.setText(_translate("noteDialog", "Note", None))

