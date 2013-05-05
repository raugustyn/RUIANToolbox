﻿# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        RUIAN2DB
# Purpose:
#
# Author:      DiblikT
#
# Created:     05/05/2013
# Copyright:   (c) DiblikT 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PyQt4.QtGui import (QApplication, QWizard, QWizardPage, QPixmap, QLabel,
                         QRadioButton, QVBoxLayout, QLineEdit, QGridLayout,
                         QRegExpValidator, QCheckBox, QPrinter, QPrintDialog,
                         QMessageBox,QTextBrowser,QPushButton, QIcon, QFileDialog)
from PyQt4.QtCore import (pyqtSlot, pyqtSignal, QRegExp, QObject, SIGNAL)
import sys,os

class LicenseWizard(QWizard):
    NUM_PAGES = 6

    (PageIntro, PageImport, PageSetupDB, PageCreateDBStructure, PageImportParameters, PageImportDB) = range(NUM_PAGES)

    def __init__(self, parent=None):
        super(LicenseWizard, self).__init__(parent)

        self.setPage(self.PageIntro, IntroPage(self))
        self.setPage(self.PageImport, ImportPage())
        self.setPage(self.PageSetupDB, SetupDBPage())
        self.setPage(self.PageCreateDBStructure, CreateDBStructurePage())
        self.setPage(self.PageImportParameters, ImportParametersPage())
        self.setPage(self.PageImportDB, ImportDBPage())

        self.setStartId(self.PageIntro)

        self.setWizardStyle(self.ModernStyle)
        self.setWindowTitle(u'EURADIN - Import RÚIAN')
        self.curDir = os.path.dirname(__file__)
        self.pictureName = os.path.join(self.curDir, 'img\\pyProject.png')
        self.setWindowIcon(QIcon(self.pictureName))

        self.setButtonText(self.NextButton, QApplication.translate("LicenseWizard", 'Další >>', None, QApplication.UnicodeUTF8))
        self.setButtonText(self.BackButton, QApplication.translate("LicenseWizard", '<< Zpět', None, QApplication.UnicodeUTF8))
        self.setButtonText(self.CancelButton, QApplication.translate("LicenseWizard", 'Storno', None, QApplication.UnicodeUTF8))
        self.setButtonText(self.FinishButton,QApplication.translate("LicenseWizard", 'Konec', None, QApplication.UnicodeUTF8))

class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle(self.tr(u"Úvod"))
        topLabel = QLabel()
        topLabel.setText(QApplication.translate("IntroPage", 'Tady bude neco napsaného <i>třeba kurzívou</i> nebo na <br> novém řádku a <b style="font-size: large">tučne</b>,<br>protože zde fungují HTML tagy.', None, QApplication.UnicodeUTF8))

        layout = QVBoxLayout()
        layout.addWidget(topLabel)

        self.setLayout(layout)

    def nextId(self):
            return LicenseWizard.PageImport

class ImportPage(QWizardPage):
    def __init__(self, parent=None):
        super(ImportPage, self).__init__(parent)

        self.setTitle(QApplication.translate("ImportPage", 'Vytvoření databázové struktury', None, QApplication.UnicodeUTF8))

        self.serverAddressLabel = QLabel("Adresa serveru: ")
        self.serverAddress = QLineEdit()
        self.serverAddressLabel.setBuddy(self.serverAddress)

        self.SQLPathLabel = QLabel(self.tr("Cesta k SQLPlus:"))
        self.SQLPath = QLineEdit()
        self.SQLPathLabel.setBuddy(self.SQLPath)

        self.userLabel = QLabel(QApplication.translate("ImportPage", 'Uživatel', None, QApplication.UnicodeUTF8))
        self.user = QLineEdit()
        self.userLabel.setBuddy(self.user)

        self.passwordLabel = QLabel(self.tr("Heslo:"))
        self.password = QLineEdit()
        self.passwordLabel.setBuddy(self.password)

        self.openButton = QPushButton()
        self.curDir = os.path.dirname(__file__)
        self.pictureName = os.path.join(self.curDir, 'img\\dir.png')
        self.openButton.setIcon(QIcon(self.pictureName))

        self.registerField("details.serverAddress*", self.serverAddress)
        self.registerField("details.SQLPath*", self.SQLPath)

        grid = QGridLayout()
        grid.addWidget(self.serverAddressLabel, 0, 0)
        grid.addWidget(self.serverAddress, 0, 1)
        grid.addWidget(self.SQLPathLabel, 1, 0)
        grid.addWidget(self.SQLPath, 1, 1)
        grid.addWidget(self.openButton, 1, 2)
        grid.addWidget(self.userLabel, 2, 0)
        grid.addWidget(self.user, 2, 1)
        grid.addWidget(self.passwordLabel, 3, 0)
        grid.addWidget(self.password, 3, 1)
        self.setLayout(grid)

        self.connect(self.openButton, SIGNAL("clicked()"), self.setPath)

    def setPath(self):
        filedialog = QFileDialog.getOpenFileName(self, 'Open file','/home')
        self.SQLPath.setText(filedialog)


    def nextId(self):
        return LicenseWizard.PageSetupDB

class SetupDBPage(QWizardPage):
    def __init__(self, parent=None):
        super(SetupDBPage, self).__init__(parent)

        self.setTitle(QApplication.translate("SetupDBPage", 'Nastavení vytvářené databáze', None, QApplication.UnicodeUTF8))

        keyLabel = QLabel("<b>KEY<\b>")
        valueLable = QLabel("<b>value<\b>")

        tsLabel = QLabel("Table space")
        ts = QLineEdit('EURADIN_RUIAN')
        tsLabel.setBuddy(ts)

        schemaLabel = QLabel(self.tr("Database schema"))
        schema = QLineEdit('dbschema')
        schemaLabel.setBuddy(schema)

        obceLabel = QLabel(self.tr("Obce"))
        obce = QLineEdit('obce')
        obceLabel.setBuddy(obce)

        nazvyObceLabel = QLabel(QApplication.translate("SetupDBPage", 'Části obce', None, QApplication.UnicodeUTF8))
        nazvyObce = QLineEdit('casti_obce')
        nazvyObceLabel.setBuddy(nazvyObce)

        katUzLabel = QLabel(self.tr(u"Katastrální území"))
        katUz = QLineEdit('katastralni_uzemi')
        katUzLabel.setBuddy(katUz)

        uliceLabel = QLabel(self.tr("Ulice"))
        ulice = QLineEdit('ulice')
        uliceLabel.setBuddy(ulice)

        parcelyLabel = QLabel(self.tr("Parcely"))
        parcely = QLineEdit('parcely')
        parcelyLabel.setBuddy(parcely)

        stavObjLabel = QLabel(self.tr(u"Stavební objekty"))
        stavObj = QLineEdit('stavebni_objekty')
        stavObjLabel.setBuddy(stavObj)

        adrMistaLabel = QLabel(self.tr(u"Adresní místa"))
        adrMista = QLineEdit('adresni_mista')
        adrMistaLabel.setBuddy(adrMista)

        grid = QGridLayout()
        grid.addWidget(keyLabel, 0, 0)
        grid.addWidget(valueLable, 0, 1)
        grid.addWidget(tsLabel, 1, 0)
        grid.addWidget(ts, 1, 1)
        grid.addWidget(schemaLabel, 2, 0)
        grid.addWidget(schema, 2, 1)
        grid.addWidget(obceLabel, 3, 0)
        grid.addWidget(obce, 3, 1)
        grid.addWidget(nazvyObceLabel, 4, 0)
        grid.addWidget(nazvyObce, 4, 1)
        grid.addWidget(katUzLabel, 5, 0)
        grid.addWidget(katUz, 5, 1)
        grid.addWidget(uliceLabel, 6, 0)
        grid.addWidget(ulice, 6, 1)
        grid.addWidget(parcelyLabel, 7, 0)
        grid.addWidget(parcely, 7, 1)
        grid.addWidget(stavObjLabel, 8, 0)
        grid.addWidget(stavObj, 8, 1)
        grid.addWidget(adrMistaLabel, 9, 0)
        grid.addWidget(adrMista, 9, 1)
        self.setLayout(grid)

    def nextId(self):
        return LicenseWizard.PageCreateDBStructure


class CreateDBStructurePage(QWizardPage):
    def __init__(self, parent=None):
        super(CreateDBStructurePage, self).__init__(parent)

        self.setTitle(QApplication.translate("CreateDBStructurePage", 'Vytvoření databázové struktury', None, QApplication.UnicodeUTF8))

        self._console = QTextBrowser(self)
        self._button  = QPushButton(self)
        self._button.setText('Test Me')

        def prepareSQL(status):
            if status == '0':
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=red>Připraviji dávku SQL</font>', None, QApplication.UnicodeUTF8))
            else:
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=green>Připraviji dávku SQL</font>', None, QApplication.UnicodeUTF8))

        def runSQL(status):
            if status == '0':
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=red>Spouštím dávku SQL</font>', None, QApplication.UnicodeUTF8))
            else:
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=green>Spouštím dávku SQL</font>', None, QApplication.UnicodeUTF8))

        def done(status):
            if status == '0':
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=red>Hotovo</font>', None, QApplication.UnicodeUTF8))
            else:
                return QLabel(QApplication.translate("CreateDBStructurePage", '<font color=green>Hotovo</font>', None, QApplication.UnicodeUTF8))

        grid = QGridLayout()
        grid.addWidget(prepareSQL('1'), 0, 0)
        grid.addWidget(runSQL('0'), 1, 0)
        grid.addWidget(done('0'), 2, 0)
        grid.addWidget(self._console,3,0)
        grid.addWidget(self._button,6,0)
        self.setLayout(grid)

        # create connections
        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )

        self._button.clicked.connect(self.test)

    def test( self ):
        # print some stuff
        print 'testing'
        print 'testing2'

        # log some stuff
        logger.debug('Testing debug')
        logger.info('Testing info')
        logger.warning('Testing warning')
        logger.error('Testing error')

        # error out something
        print blah


    def nextId(self):
        return LicenseWizard.PageImportParameters
        #return -1

class ImportParametersPage(QWizardPage):
    def __init__(self, parent=None):
        super(ImportParametersPage, self).__init__(parent)

        self.setTitle(self.tr("Parametry importu"))

        self.dirLabel = QLabel(QApplication.translate("ImportParametersPage", 'Adresář s daty RÚIAN', None, QApplication.UnicodeUTF8))
        self.setDir = QLineEdit()
        self.dirLabel.setBuddy(self.setDir)

        self.suffixLabel = QLabel(QApplication.translate("CreateDBStructurePage", 'Přípona souboru', None, QApplication.UnicodeUTF8))
        self.suffix = QLineEdit('.xml')
        self.suffixLabel.setBuddy(self.suffix)

        self.openButton1 = QPushButton()
        self.curDir = os.path.dirname(__file__)
        self.pictureName = os.path.join(self.curDir, 'img\\dir.png')
        self.openButton1.setIcon(QIcon(self.pictureName))

        self.bottomLabel = QLabel()
        self.bottomLabel.setWordWrap(True)

        self.walkDir = QCheckBox(QApplication.translate("ImportParametersPage", 'Včetně podadresářů', None, QApplication.UnicodeUTF8))

        grid = QGridLayout()
        grid.addWidget(self.dirLabel, 0, 0)
        grid.addWidget(self.setDir, 0, 1)
        grid.addWidget(self.openButton1, 0, 2)
        grid.addWidget(self.suffixLabel, 1, 0)
        grid.addWidget(self.suffix, 1, 1)
        grid.addWidget(self.bottomLabel, 2, 0)
        grid.addWidget(self.walkDir, 2, 1)

        self.setLayout(grid)
        self.connect(self.openButton1, SIGNAL("clicked()"), self.setPath1)

    def setPath1(self):
        dirDialog = QFileDialog.getExistingDirectory(self, QApplication.translate("CreateDBStructurePage", 'Výběr adrešáře', None, QApplication.UnicodeUTF8))
        if not dirDialog.isNull():
            self.setDir.setText(dirDialog)

    def nextId(self):
        return LicenseWizard.PageImportDB

class ImportDBPage(QWizardPage):
    def __init__(self, parent=None):
        super(ImportDBPage, self).__init__(parent)

        self.setTitle(self.tr(u"Importování dat"))

        self._console = QTextBrowser(self)
        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )

        grid = QGridLayout()
        grid.addWidget(self._console,0,0)
        self.setLayout(grid)

    def nextId(self):
        return -1

class XStream(QObject):
    _stdout = None
    _stderr = None

    messageWritten = pyqtSignal(str)

    def flush( self ):
        pass

    def fileno( self ):
        return -1

    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(unicode(msg))

    @staticmethod
    def stdout():
        if ( not XStream._stdout ):
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if ( not XStream._stderr ):
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr


# main ========================================================================
def main():

    app = QApplication(sys.argv)
    wiz = LicenseWizard()
    wiz.show()

    print 'Console..'

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()