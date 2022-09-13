import sys
import time

from dropbox import Dropbox

from utils import constants
from utils.logging_format import LoggingFormat


class DeleteFiles:

    @staticmethod
    def delete(cliente, date):
        """A ideia é fazer é varrer a pasta do cliente enviado e fazer um for de exclusão,
        com a condição que se não for igual a data enviada exclui, se for não excluí"""

        # Validando variavel
        if not constants.DROPBOX_TOKEN:
            message = "Token não informado!"
            LoggingFormat.format(message, "Error")
            sys.exit(1)

        # Conectar Dropbox com o token
        try:
            dropbox = Dropbox(constants.DROPBOX_TOKEN)
        except Exception as e:
            message = f"Erro ao tentar conectar com no DropBox com o Token informado " + str(e)
            LoggingFormat.format(message, "Error")
            message = 'Tentando novamente daqui a 1 minuto!'
            LoggingFormat.format(message, "Info")
            time.sleep(60)
            message = 'Efetuando nova tentativa!'
            LoggingFormat.format(message, "Info")
            DeleteFiles.delete(cliente, date)

        file_objs = dropbox.files_list_folder(f"/{cliente}", recursive=True)

        message = f'Efetuando a deleção dos arquivos antigos do cliente: {cliente}'
        LoggingFormat.format(message, "Alert")

        # Validando paginação
        while file_objs.has_more:
            # Varrer objetos dentro da pasta do cliente informdo.

            for i in file_objs.entries:
                # Vericar se existe os atributos do objeto para coletar informações.
                if hasattr(i, 'client_modified'):
                    # Validar se o arquivo atual é o mesmo que é pra ser preservado, se não for, chama a deleção
                    if i.client_modified != date:
                        if i.name != 'calima-backup.zip':
                            # Chamar a deleção
                            dropbox.files_delete_v2(path=f"/{cliente}/{i.name}")
                            message = f"Deletando o arquivo {i.name} com data de alteração em: {i.client_modified}"
                            LoggingFormat.format(message, "Info")
                    else:
                        message = f"Arquivo: {i.name} com data: {date}, vai ser preservado! "
                        LoggingFormat.format(message, "Alert")

            # Pula o cursor para ver se tem paginação.
            file_objs = dropbox.files_list_folder_continue(file_objs.cursor)

        # Varrer a ultima pagina para pegar todoso os arquivo e chama a deleção.
        for i in file_objs.entries:
            # Vericar se existe os atributos do objeto para coletar informações.
            if hasattr(i, 'client_modified'):
                if i.client_modified != date:
                    # Vou chamar a deleção
                    dropbox.files_delete_v2(path=f"/{cliente}/{i.name}")
                    message = f"Deletando o arquivo {i.name} com data de alteração em: {i.client_modified}"
                    LoggingFormat.format(message, "Info")
                else:
                    message = f"Arquivo: {i.name} vai ser preservado"
                    LoggingFormat.format(message, "Alert")
