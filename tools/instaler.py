#!/usr/bin/python3
import tarfile
import os
import shutil

install_path = "./self_help"
tar_img = "self_help_table.tar"
try:
    shutil.rmtree(install_path)
except FileNotFoundError:
    pass
os.mkdir(install_path)
with tarfile.open(tar_img, "r") as tf:
    print("Opened tarfile")
    tf.extractall(path=install_path)

print("Done.")
