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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_note_dialog import Ui_noteDialog

from qgis.core import *
from qgis.utils import *
from qgis.gui import *
# create the dialog for zoom to point



class sketchNoteDialog(QDialog, Ui_noteDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.hide()
        self.buttonBox.accepted.connect(self.mkNote)
        self.buttonBox.rejected.connect(self.cancel)
        self.note = None
        self.iface = iface

    def setPoint(self,p):
        self.point = p

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
        self.textItem = self.mkAnnotation(self.noteText.toPlainText(),self.point)
        self.note = self.noteText.toPlainText()
        self.noteText.clear()

    def mkAnnotation(self,doc,p):
        TD =QTextDocument(doc)
        item = QgsTextAnnotationItem( self.iface.mapCanvas() )
        item.setMapPosition(p)
        item.setFrameSize(TD.size())
        item.setDocument(TD)
        item.update()
        return item
        

    @staticmethod
    def newPoint(iface,p,txt = None):
        dialog = sketchNoteDialog(iface)
        dialog.setPoint(p)
        if not txt:
            print "interactive"
            result = dialog.exec_()
            dialog.show()
            if QDialog.Accepted:
                return dialog.getAnnotation()
            else:
                return None
        else:
            print "non interactive"
            return dialog.mkAnnotation(txt,p)
            