"""Arquivo com as variaveis necessárias para o funcionamento do projeto"""
import logging
import os

DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')


class Path:
    TMP_DIR = "/tmp/infra-clear-dropbox"
