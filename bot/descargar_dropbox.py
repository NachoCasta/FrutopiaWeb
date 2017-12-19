import os
import base64

import dropbox


def descargar_excels(download_path):
    token = base64.b64decode(b'WFlYYTUtTnhQY1FBQUFBQUFBQU5JVmtCNlBFZm5IQzVnaVBMS2pCa256Vmg5cXFqMlhRSXNWZUxicGhGaUZSTg==').decode("utf-8")
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

def descargar_jefes(download_path):
    token = base64.b64decode(b'WFlYYTUtTnhQY1FBQUFBQUFBQU5JVmtCNlBFZm5IQzVnaVBMS2pCa256Vmg5cXFqMlhRSXNWZUxicGhGaUZSTg==').decode("utf-8")
    dbx = dropbox.Dropbox(token)
    download_path = download_path.strip("/") + "/"
    path = "/Frutillas"
    file = "Jefes 2017-2.xlsx"
    dbx.files_download_to_file(download_path+file, path + "/" + file)

def actualizar_archivo(file_path, upload_path):
    token = base64.b64decode(b'WFlYYTUtTnhQY1FBQUFBQUFBQU5JVmtCNlBFZm5IQzVnaVBMS2pCa256Vmg5cXFqMlhRSXNWZUxicGhGaUZSTg==').decode("utf-8")
    dbx = dropbox.Dropbox(token)
    with open(file_path, "rb") as file:
        data = file.read()
    nombre = file_path.split("/")[-1]
    dbx.files_upload(data, upload_path+"/"+nombre,
                     mode=dropbox.files.WriteMode.overwrite)
    


if __name__ == "__main__":
    descargar_excels("datos")
