#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import (QLayout, QSizePolicy)


class PFlowLayout(QLayout):

    def __init__(self, orientation=Qt.Horizontal, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.orientation = orientation

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList = []
        self.configData = {}
        self.realHeight = 0

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def clear(self):
        self.__del__()

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return self.orientation == Qt.Horizontal

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def hasWidthForHeight(self):
        return self.orientation == Qt.Vertical

    def widthForHeight(self, height):
        return self.doLayout(QRect(0, 0, 0, height), True)

    def setGeometry(self, rect: QRect):
        self.update()
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def getLineSize(self, parentRect: QRect):
        total = 1 if len(self.itemList) > 0 else 0
        last = 0
        size = {}
        for item in self.itemList:
            last += item.sizeHint().width()
            if last >= parentRect.width():
                total += 1
                last = 0
            if str(total) not in size:
                size[str(total)] = item.sizeHint().height()
            else:
                size[str(total)] = max(size[str(total)], item.sizeHint().height())

        return total, size

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.sizeHint())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)

        layoutSize = self.contentsRect()
        if self.hasHeightForWidth():
            size.setHeight(self.heightForWidth(layoutSize.width()))
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = columnWidth = heightForWidth = 0
        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton,
                                                                Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton,
                                                                Qt.Vertical)
            if self.orientation == Qt.Horizontal:
                nextX = x + item.sizeHint().width() + spaceX
                if nextX - spaceX > rect.right() and lineHeight > 0:
                    x = rect.x()
                    y = y + lineHeight + spaceY
                    nextX = x + item.sizeHint().width() + spaceX
                    lineHeight = 0

                if not testOnly:
                    item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

                x = nextX
                lineHeight = max(lineHeight, item.sizeHint().height())
            else:
                nextY = y + item.sizeHint().height() + spaceY
                if nextY - spaceY > rect.bottom() and columnWidth > 0:
                    x = x + columnWidth + spaceX
                    y = rect.y()
                    nextY = y + item.sizeHint().height() + spaceY
                    columnWidth = 0

                heightForWidth += item.sizeHint().height() + spaceY
                if not testOnly:
                    item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

                y = nextY
                columnWidth = max(columnWidth, item.sizeHint().width())

        if self.orientation == Qt.Horizontal:
            return y + lineHeight - rect.y()
        else:
            return heightForWidth - rect.y()
