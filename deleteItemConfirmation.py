from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DeleteConfirmation(object):
    def setupUi(self, DeleteConfirmation):
        DeleteConfirmation.setObjectName("DeleteConfirmation")
        DeleteConfirmation.resize(387, 178)
        DeleteConfirmation.setMinimumSize(QtCore.QSize(387, 178))
        DeleteConfirmation.setMaximumSize(QtCore.QSize(387, 178))
        self.Text = QtWidgets.QLabel(parent=DeleteConfirmation)
        self.Text.setGeometry(QtCore.QRect(10, 40, 362, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Text.setFont(font)
        self.Text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Text.setObjectName("Text")
        self.widget = QtWidgets.QWidget(parent=DeleteConfirmation)
        self.widget.setGeometry(QtCore.QRect(11, 120, 361, 35))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Cancel = QtWidgets.QPushButton(parent=self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Cancel.setFont(font)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout.addWidget(self.Cancel)
        self.Confirm = QtWidgets.QPushButton(parent=self.widget)
        self.Confirm.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Confirm.setFont(font)
        self.Confirm.setObjectName("Confirm")
        self.Confirm.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                padding: 6px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)
        self.horizontalLayout.addWidget(self.Confirm)

        self.retranslateUi(DeleteConfirmation)
        QtCore.QMetaObject.connectSlotsByName(DeleteConfirmation)

    def retranslateUi(self, DeleteConfirmation):
        _translate = QtCore.QCoreApplication.translate
        DeleteConfirmation.setWindowTitle(_translate("DeleteConfirmation", "Dialog"))
        self.Text.setText(_translate("DeleteConfirmation", "Are you sure you want to delete this item?"))
        self.Cancel.setText(_translate("DeleteConfirmation", "Cancel"))
        self.Confirm.setText(_translate("DeleteConfirmation", "Confirm"))
