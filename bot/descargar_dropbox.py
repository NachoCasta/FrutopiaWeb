import os

import dropbox


def descargar_excels(download_path):
    token = "XYXa5-NxPcQAAAAAAAANIVkB6PEfnHC5giPLKjBknzVh9qqj2XQIsVeLbphFiFRN"
    dbx = dropbox.Dropbox(token)
    path = "/Frutillas/Contabilidad/2017 - 2"
    download_path = download_path.strip("/") + "/"
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    for entry in dbx.files_list_folder(path).entries:
        file = entry.name
        dbx.files_download_to_file(download_path+file, path + "/" + file)
    path = "/Frutillas"
    file = "Jefes 2017-2.xlsx"
    dbx.files_download_to_file(download_path+file, path + "/" + file)


if __name__ == "__main__":
    descargar_excels("test")
