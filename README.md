# Blacklist

## Instalação
### Usando pipenv
 - Instale a ferramenta Pipenv, https://pipenv.pypa.io/en/latest/install/#installing-pipenv
 - Instale as dependências do projeto com: ```pipenv install```
### Virtualenv
 - Crie seu virtualenv, ative e instale as dependências: ```pip install -r requirements.txt```

## Configuração
 - Crie um arquivo ```.env```, baseado no exemplo em ```.env.example```
### Banco de dados:
 - O projeto já suporta o banco sqlite, para utilizar outros bancos, instale o conector equivalente e configure a url em ```.env```
 - Exemplos de padrão de url para vários bancos podem ser encontrados em: https://github.com/jacobian/dj-database-url#url-schema

## Rodando
### *Ignore o prefixo "```pipenv run```" se estiver usando diretamente o virtualenv*
### Sincronizando o banco de dados:
```bash
pipenv run python manage.py migrate
```
### Criando um usuário administrador
```bash
pipenv run python manage.py createsuperuser
```
### Importando a lista de deny
```bash
pipenv run python manage.py import_list [ARQUIVO]
```
### Iniciando o servidor
```bash
pipenv run python manage.py collectstatic
pipenv run python manage.py runserver
```
## Testes
```bash
pipenv run python manage.py test
```
## Endpoints
### Autenticação:
```
POST /api/token
```
```json
{
    "username": "nome_de_usuário",
    "password": "senha"
}
```
### Checar CPF
```
GET /cpf/<NÚMERO>
```
### Criar entrada na lista (requer autenticação)
```
POST /cpf/
```
```
HEADERS: Authorization: Bearer <TOKEN RETORNADO NA AUTENTICAÇÃO>
```
### Remover entrada da lista (requer autenticação)
```
DELETE /cpf/
```
```
HEADERS: Authorization: Bearer <TOKEN RETORNADO NA AUTENTICAÇÃO>
```
