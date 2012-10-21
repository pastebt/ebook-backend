#include <QCoreApplication>
#include <QtCore>
#include <QFileInfo>
#include <QFile>
#include <QDir>
#include <iostream>
#include <quazip.h>
#include <quazipfile.h>
#include <quazipfileinfo.h>

using namespace std;

void print_usage()
{
    cout << "Copyright (C) 2012 Fan Yang <missdeer@gmail.com>\n"
         << "epub filename.epub [-d destine_directory]"
            << endl;
}

bool convert(const QString& epub, const QString destineDir)
{
    qDebug() << "Start extracting file " << epub << " to " << destineDir;
    QuaZip zip(epub);
    if (!zip.open(QuaZip::mdUnzip)) {
        cerr << "Opening " << epub.toStdString() << " as a zipped archive failed!" << endl;
        return false;
    }

    // and now we are going to access files inside it
    QuaZipFile file(&zip);
    for(bool more=zip.goToFirstFile(); more; more=zip.goToNextFile()) {
        if (file.open(QIODevice::ReadOnly)) {
            qDebug() << "Extracting " << file.getActualFileName();
            QString destineFile(destineDir + QDir::separator() + file.getActualFileName());
            QFileInfo destineFileInfo(destineFile);
            QDir destinePath(destineFileInfo.absoluteDir());
            if (!destinePath.exists())
                destinePath.mkpath(destineFileInfo.absolutePath());

            QFile unzipFile(destineFile);
            if (unzipFile.open(QFile::WriteOnly)) {
                qDebug() << "Saving to " << unzipFile.fileName();
                unzipFile.write(file.readAll());
                unzipFile.close();
            }
            file.close(); // do not forget to close!
        }
    }
    if(zip.getZipError()==UNZ_OK) {
      // ok, there was no error
    }

    zip.close();
    return true;
}

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    if (argc != 2 && argc != 4)
    {
        print_usage();
        return -1;
    }

    QString ePubFilePath(QString::fromLocal8Bit(argv[1]));
    QString destineDir;
    if (argc == 4) {
        destineDir = argv[3];
    } else {
        QFileInfo fi(ePubFilePath);
        if (!QFile::exists(ePubFilePath)) {
            qDebug() << ePubFilePath << " does not exist.";
            cerr << argv[1] << " does not exist.";
            return -2;
        }

        destineDir = fi.absoluteFilePath();
        int index = destineDir.lastIndexOf(".");
        destineDir.remove(index, destineDir.length() - index);
        if (!QDir(destineDir).exists()) {
            QDir(destineDir).mkpath(destineDir);
        }
    }

    return (convert(ePubFilePath, destineDir) ? 0 : 1);
}
