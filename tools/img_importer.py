#!/usr/bin/python3
import os

install_path = "../static_imgs"
_img = "self_help_table.tar"

def unpackTheImg(filesToExtract):
    if not os.path.exists(install_path):
        os.makedirs(install_path)
    if img_format == 'zip':
        from zipfile import ZipFile
        print("Opening the zip file")
        with ZipFile(_img, 'r') as zipObj:
            for elem in filesToExtract:
                elem = elem.replace("\\", "/") #Windows path fix :(
                #print(elem)
                zipObj.extract(elem, install_path)
    elif img_format == 'tar':
        import tarfile
        print("Opening the tar file")
        with tarfile.open(_img, "r") as tf:
            for elem in filesToExtract:
                #print(elem.name)
                elem = elem.replace("\\", "/") #Windows path fix :(
                tf.extract(elem, install_path)
    else:
        print("Format not supported!")
        exit()
    print("Done with upgrading files.")

install_path = os.path.abspath(install_path)

unpackTheImg(_img)
print("Done.")
