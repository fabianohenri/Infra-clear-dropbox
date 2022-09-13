"""A ideia é fazer a execução via cron e ele ir chamando a exclusão de todos os arquivos de todos os clientes
    no dropbox da projetus.
    Tratar a parte não ir somando um numero ao folder mas sim epgar de fato o valor do folder"""
import logging

from dropbox import Dropbox

from controller.delete_files import DeleteFiles
from utils import constants
from utils.logging_format import LoggingFormat


class DrobpoxController:

    @staticmethod
    def clear():
        message = "Chamada para efetuar a exclusão dos arquivos antigos do DropBox"
        # logging.warning(message)
        LoggingFormat.format(message, "Info")

        # Validando variavel
        if not constants.DROPBOX_TOKEN:
            message = "Token não informado!"
            LoggingFormat.format(message, "Error")
            raise SystemExit

        # Conectar Dropbox com o token
        try:
            dropbox = Dropbox(constants.DROPBOX_TOKEN, max_retries_on_error=5)
            all_objects = dropbox.files_list_folder('')
        except Exception as e:
            message = f"Erro ao tentar conectar com no DropBox com o Token informado " + str(e)
            # logging.warning(message)
            LoggingFormat.format(message, "Error")
            return

        directories = []
        # Varrer os diretorios da raiz, adicionando somente diretorios validos a uma nova lista
        message = f"Criando lista de diretórios a serem verificados."
        # logging.info(message)
        LoggingFormat.format(message, "Info")

        while all_objects.has_more:
            for client in all_objects.entries:
                # Validar se o nome da pasta é númerico pra não pegar outras pastas.
                if client.name.isnumeric():
                    directories.append(int(client.name))

            all_objects = dropbox.files_list_folder_continue(all_objects.cursor)

        # Varrer registros restantes
        for client in all_objects.entries:
            if client.name.isnumeric():
                directories.append(int(client.name))

        directories_order = sorted(directories)
        # TODO Passar essa parte de coletar o ultimo arquivo para uma classe separada.
        # Varrer diretorio do cliente para verificar data dos arquivos
        for current_directories in directories_order:
            file_objs = dropbox.files_list_folder(f"/{str(current_directories)}", recursive=True)
            date_current, name_current = None, None
            message = f'Verificando backups do cliente: {str(current_directories)}'
            LoggingFormat.format(message, "Info")

            current = False
            count_files = 0
            while file_objs.has_more:
                # Validar se tem mais de um arquivo na pasta para agilizar o procecsso.
                if len(file_objs.entries) < 3:
                    for file in file_objs.entries:
                        if hasattr(file, 'client_modified'):
                            count_files += 1
                            if date_current is None:
                                date_current = file.client_modified
                                name_current = file.name
                            elif file.client_modified > date_current:
                                date_current = file.client_modified
                                name_current = file.name
                    if not current:
                        current = True
                else:
                    for file in file_objs.entries:
                        # Vericar se existe os atributos do objeto para coletar informações.
                        if hasattr(file, 'client_modified'):
                            # Existindo os atributos começo a alimentar as variaveis
                            count_files += 1
                            message = f'Nome: {file.name}, Data: {file.client_modified}'
                            LoggingFormat.format(message, "Info")
                            if date_current is None:
                                date_current = file.client_modified
                                name_current = file.name
                            elif file.client_modified > date_current:
                                date_current = file.client_modified
                                name_current = file.name

                # Adianto o cursor para que se a tiver paginação na quantidade de arquivos dentro da pasta
                file_objs = dropbox.files_list_folder_continue(file_objs.cursor)

            # Validar se tem mais de um arquivo na pasta para agilizar o procecsso.
            if len(file_objs.entries) <= 2:
                if not current:
                    for file in file_objs.entries:
                        # Vericar se existe os atributos do objeto para coletar informações.
                        if hasattr(file, 'client_modified'):
                            count_files += 1
                            if date_current is None:
                                date_current = file.client_modified
                                name_current = file.name
                            elif file.client_modified > date_current:
                                date_current = file.client_modified
                                name_current = file.name
                    current = True
            else:
                # Varrer pela ultima vez a ultima listagem
                for file in file_objs.entries:
                    if hasattr(file, 'client_modified'):
                        count_files += 1
                        message = f'Nome: {file.name}, Data: {file.client_modified}'
                        LoggingFormat.format(message, "Info")
                        if date_current is None:
                            date_current = file.client_modified
                            name_current = file.name
                        elif file.client_modified > date_current:
                            date_current = file.client_modified
                            name_current = file.name

            if count_files >= 2:
                # Valido se existe um arquivo atual. Se tiver, chama a deleção.
                if date_current is not None:
                    "Chamando a deleção passando o nome, data do arquivo que NÂO vai ser deletado, e passando o nome " \
                        "da pasta para que sejá deletado da pasta correta."

                    message = f'Arquivo do Cliente: {current_directories} a ser preservado, vai ser o de nome: '\
                              f'{name_current}, data: {date_current}'
                    LoggingFormat.format(message, "Info")
                    DeleteFiles.delete(str(current_directories), date_current)
            else:
                if current:
                    message = f'Arquivo do Cliente: {current_directories} com de nome: ' \
                              f'{name_current}, data: {date_current}, já é o mais atual!'
                    LoggingFormat.format(message, "Info")
        return "Verificação Terminanda"

    @staticmethod
    def list_files_dropbox(customer_code):
        try:
            dropbox = Dropbox(constants.DROPBOX_TOKEN, max_retries_on_error=5)
            list_files = dropbox.files_list_folder(f"/{customer_code}", recursive=True)
        except Exception as e:
            message = f"Erro ao tentar conectar com no DropBox com o Token informado " + str(e)
            LoggingFormat.format(message, "Error")
            return

        date_current, name_current = None, None
        count_files = 0
        while list_files.has_more:
            # Validar se tem mais de um arquivo na pasta para agilizar o procecsso.
            if len(list_files.entries) < 3:
                for file in list_files.entries:
                    if hasattr(file, 'client_modified'):
                        count_files += 1
                        if date_current is None:
                            date_current = file.client_modified
                            name_current = file.name
                        elif file.client_modified > date_current:
                            date_current = file.client_modified
                            name_current = file.name
            else:
                for file in list_files.entries:
                    if hasattr(file, 'client_modified'):
                        count_files += 1
                        if date_current is None:
                            date_current = file.client_modified
                            name_current = file.name
                        elif file.client_modified > date_current:
                            date_current = file.client_modified
                            name_current = file.name

            list_files = dropbox.files_list_folder_continue(list_files.cursor)

        for file in list_files.entries:
            if hasattr(file, 'client_modified'):
                count_files += 1
                if date_current is None:
                    date_current = file.client_modified
                    name_current = file.name
                elif file.client_modified > date_current:
                    date_current = file.client_modified
                    name_current = file.name

        return date_current
