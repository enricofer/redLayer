# -*- coding: utf-8 -*-
"""
/***************************************************************************
 idtVen - class idtVen_albero
                                 A QGIS plugin
 compilazione assistita metadati regione veneto
                              -------------------
        begin                : 2014-12-04
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Enrico Ferreguti
        email                : enricofer@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

#from PyQt4 import QtCore, QtGui
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from qgis.core import *
from qgis.utils import *
from qgis.gui import *
# create the dialog for zoom to point

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_note_dialog.ui'))

class sketchNoteDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        super(sketchNoteDialog, self).__init__(parent)
        self.setupUi(self)
        self.hide()
        self.buttonBox.accepted.connect(self.mkNote)
        self.buttonBox.rejected.connect(self.cancel)
        self.note = None
        self.iface = iface

    def setPoint(self,segment):
        self.point = self.midPoint(segment)

    def getNote(self):
        return self.note

    def getAnnotation(self):
        try:
            return self.textItem
        except:
            return None

    def cancel(self):
        self.note = ""
        #self.hide()
        pass

    def mkNote(self):
        self.textItem = self.mkAnnotation(self.noteText.toPlainText())
        self.note = self.noteText.toPlainText()
        self.noteText.clear()

    def mkAnnotation(self,doc):
        if self.point:
            TD =QTextDocument(doc)
            item = QgsTextAnnotation()
            item.setMapPosition(self.point)
            item.setFrameSize(TD.size())
            item.setDocument(TD)
            i = QgsMapCanvasAnnotationItem(item, self.iface.mapCanvas())
            return i
        else:
            return

    def midPoint(self,s):
       x = (s.vertexAt(0).x() + s.vertexAt(1).x())/2
       y = (s.vertexAt(0).y() + s.vertexAt(1).y())/2
       return QgsPointXY(x,y)

    @staticmethod
    def newPoint(iface,segment,txt = None):
        dialog = sketchNoteDialog(iface)

        dialog.setPoint(segment)
        if not txt:
            result = dialog.exec_()
            dialog.show()
            if QDialog.Accepted:
                return dialog.getAnnotation()
            else:
                return None
        else:
            return dialog.mkAnnotation(txt)
            