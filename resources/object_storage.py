import json
import os
import shutil
from datetime import datetime, timedelta

import requests

from utils.constants import Path
from utils.logging_format import LoggingFormat


class ObjectStorage:

    @staticmethod
    def upload():
        message = "Iniciando o envio do arquivo de log para o object storage"
        LoggingFormat.format(message, "Info")

        try:
            # Pegar data atual para acrecentar ao nome do arquivo
            folder_date = datetime.today().strftime("%d-%m-%Y")
            file_name = folder_date + ".log"

            # Informarções sobre o arquivo
            file_stat = os.stat(f"{Path.TMP_DIR + '/log/' + file_name}").st_size
            file_size = file_stat / 1024
            message = f"Dados do arquivo a ser enviado: Nome: {file_name}, Tamanho: {file_size} KiB"
            LoggingFormat.format(message, "Info")

        except Exception as e:
            message = "Erro ao renomear o arquivo. Error: " + str(e)
            LoggingFormat.format(message, "Error")
            return {"message": message}

        try:
            url = "http://object-storage.projetusti.com.br/api/upload"
            payload = {"bucket_name": "logs-files",
                       "app": "infra-clear-dropbox",
                       "container": "infra-clear-dropbox",
                       "folder": f"infra-maintenance/{folder_date}"}
            files = [
                ('file', (file_name, open(Path.TMP_DIR + '/log/' + file_name), 'application/octet-stream'))
            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            if response.status_code == 413:
                message = "Arquivo grande demais."
                LoggingFormat.format(message, "Error")
                return {'message': message, 'status': 413}
            data = json.loads(response.text)
            response = {'message': data['message'], "link_log": data['link_log'], "status": response.status_code}
            return response
        except Exception as e:
            message = "Erro ao enviar o arquivo para o object storage " + str(e)
            LoggingFormat.format(message, "Error")
            return {"message": message, "status": 400}
