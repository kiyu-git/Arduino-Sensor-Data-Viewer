# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analysis_simple.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from pyqtgraph import GraphicsLayoutWidget
from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateTimeEdit,
    QDoubleSpinBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class Ui_Analyzer(object):
    def setupUi(self, Analyzer):
        if not Analyzer.objectName():
            Analyzer.setObjectName("Analyzer")
        Analyzer.resize(1512, 916)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Analyzer.sizePolicy().hasHeightForWidth())
        Analyzer.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Analyzer)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setLabelAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )
        self.formLayout.setFormAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.formLayout.setHorizontalSpacing(-1)
        self.formLayout.setVerticalSpacing(4)
        self.formLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_13 = QLabel(Analyzer)
        self.label_13.setObjectName("label_13")

        self.horizontalLayout.addWidget(self.label_13)

        self.horizontalSpacer = QSpacerItem(
            20, 20, QSizePolicy.Preferred, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.InputFiles = QComboBox(Analyzer)
        self.InputFiles.setObjectName("InputFiles")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.InputFiles.sizePolicy().hasHeightForWidth())
        self.InputFiles.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.InputFiles)

        self.formLayout.setLayout(2, QFormLayout.SpanningRole, self.horizontalLayout)

        self.label = QLabel(Analyzer)
        self.label.setObjectName("label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label)

        self.InputProgram = QLabel(Analyzer)
        self.InputProgram.setObjectName("InputProgram")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.InputProgram)

        self.label_2 = QLabel(Analyzer)
        self.label_2.setObjectName("label_2")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_2)

        self.InputChannel = QSpinBox(Analyzer)
        self.InputChannel.setObjectName("InputChannel")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.InputChannel)

        self.label_3 = QLabel(Analyzer)
        self.label_3.setObjectName("label_3")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_3)

        self.InputStartDate = QDateTimeEdit(Analyzer)
        self.InputStartDate.setObjectName("InputStartDate")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.InputStartDate)

        self.label_4 = QLabel(Analyzer)
        self.label_4.setObjectName("label_4")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_4)

        self.InputInvertFlg = QCheckBox(Analyzer)
        self.InputInvertFlg.setObjectName("InputInvertFlg")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.InputInvertFlg)

        self.label_5 = QLabel(Analyzer)
        self.label_5.setObjectName("label_5")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_5)

        self.InputLoadLimit = QSpinBox(Analyzer)
        self.InputLoadLimit.setObjectName("InputLoadLimit")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.InputLoadLimit)

        self.label_6 = QLabel(Analyzer)
        self.label_6.setObjectName("label_6")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_6)

        self.InputLPFStrength = QDoubleSpinBox(Analyzer)
        self.InputLPFStrength.setObjectName("InputLPFStrength")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.InputLPFStrength)

        self.label_9 = QLabel(Analyzer)
        self.label_9.setObjectName("label_9")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.label_9)

        self.InputUpdateFlg = QCheckBox(Analyzer)
        self.InputUpdateFlg.setObjectName("InputUpdateFlg")

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.InputUpdateFlg)

        self.label_10 = QLabel(Analyzer)
        self.label_10.setObjectName("label_10")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.label_10)

        self.InputUpdateInterval = QSpinBox(Analyzer)
        self.InputUpdateInterval.setObjectName("InputUpdateInterval")

        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.InputUpdateInterval)

        self.verticalLayout_2.addLayout(self.formLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_11 = QLabel(Analyzer)
        self.label_11.setObjectName("label_11")

        self.horizontalLayout_2.addWidget(self.label_11)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.InputConsoleClear = QPushButton(Analyzer)
        self.InputConsoleClear.setObjectName("InputConsoleClear")

        self.horizontalLayout_2.addWidget(self.InputConsoleClear)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.InputConsole = QTextBrowser(Analyzer)
        self.InputConsole.setObjectName("InputConsole")
        sizePolicy.setHeightForWidth(self.InputConsole.sizePolicy().hasHeightForWidth())
        self.InputConsole.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.InputConsole)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.GraphicsLayoutWidget = GraphicsLayoutWidget(Analyzer)
        self.GraphicsLayoutWidget.setObjectName("GraphicsLayoutWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(10)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.GraphicsLayoutWidget.sizePolicy().hasHeightForWidth()
        )
        self.GraphicsLayoutWidget.setSizePolicy(sizePolicy2)
        self.GraphicsLayoutWidget.setInteractive(True)
        self.GraphicsLayoutWidget.setRenderHints(QPainter.TextAntialiasing)

        self.gridLayout.addWidget(self.GraphicsLayoutWidget, 0, 1, 1, 1)

        self.retranslateUi(Analyzer)
        self.InputConsoleClear.clicked.connect(self.InputConsole.clear)

        QMetaObject.connectSlotsByName(Analyzer)

    # setupUi

    def retranslateUi(self, Analyzer):
        Analyzer.setWindowTitle(QCoreApplication.translate("Analyzer", "Form", None))
        self.label_13.setText(QCoreApplication.translate("Analyzer", "file", None))
        self.label.setText(QCoreApplication.translate("Analyzer", "program", None))
        self.InputProgram.setText(
            QCoreApplication.translate("Analyzer", "TextLabel", None)
        )
        self.label_2.setText(QCoreApplication.translate("Analyzer", "channel", None))
        self.label_3.setText(QCoreApplication.translate("Analyzer", "start", None))
        self.label_4.setText(QCoreApplication.translate("Analyzer", "invert", None))
        self.InputInvertFlg.setText("")
        self.label_5.setText(
            QCoreApplication.translate("Analyzer", "load limit [H]", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("Analyzer", "LPF strength", None)
        )
        self.label_9.setText(QCoreApplication.translate("Analyzer", "update", None))
        self.InputUpdateFlg.setText("")
        self.label_10.setText(
            QCoreApplication.translate("Analyzer", "update interval [s]", None)
        )
        self.label_11.setText(QCoreApplication.translate("Analyzer", "Log", None))
        self.InputConsoleClear.setText(
            QCoreApplication.translate("Analyzer", "clear", None)
        )

    # retranslateUi
