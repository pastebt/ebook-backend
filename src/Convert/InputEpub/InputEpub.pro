#-------------------------------------------------
#
# Project created by QtCreator 2012-10-16T15:17:23
#
#-------------------------------------------------

QT       += core

QT       -= gui

TARGET = epub
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app
DESTDIR = $$PWD

SOURCES += main.cpp

win32:CONFIG(release, debug|release): LIBS += -L$$OUT_PWD/../../../3rd-party/quazip/release/ -lquazip1
else:win32:CONFIG(debug, debug|release): LIBS += -L$$OUT_PWD/../../../3rd-party/quazip/debug/ -lquazip1
else:unix:!symbian: LIBS += -L$$OUT_PWD/../../../3rd-party/quazip/ -lquazip

INCLUDEPATH += $$PWD/../../../3rd-party/quazip $$PWD/../../../3rd-party/zlib-1.2.7
DEPENDPATH += $$PWD/../../../3rd-party/quazip
