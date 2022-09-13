# Infra-clear-dropbox
Aplicação para a limpeza de arquivos antigos dos usuários do dropbox.

# Objetivo
O objetivo dessa aplicação é ser chamada ou executada num cron ou de forma automatizada usando o JobLaucher para que possa manter apenas os últimos arquivo de backup dos clientes no dropbox. Assim, a empresa não paga muito com armazenamento, mantendo arquivos que não são mais necessários.

# Uso
Python 
- python3 main.py

Cron
- 0 5 * * 1 python3 main.py
