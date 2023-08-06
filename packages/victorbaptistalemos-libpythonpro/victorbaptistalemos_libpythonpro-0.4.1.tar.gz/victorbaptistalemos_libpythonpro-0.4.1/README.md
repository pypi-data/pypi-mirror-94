# victorbaptistalemos_libpythonpro

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Módulo para exemplificar construção de projetos Python no curso PyTools.

Nesse curso é ensinado como contribuir para projetos de código aberto.

Link para o curso [Python Pro](https://www.python.pro.br).

Este projeto tem como base o repositório [pythonprobr/libpythonpro](https://www.github.com/pythonprobr/libpythonpro).

Suportada a versão 3 do Python.

Tópicos a serem abordados:

1. Git
   1. Clone
      ```
      Copia um repositório através do link HTTPS ou SSH.
      ```
   2. Fork
      ```
      Cria uma cópia a partir de outro repositório.
      Utilizado para fazer melhorias em projetos de
      código aberto que você não tenha permissão
      para modificar. 
      ```
   3. Branch
      ```
      Utilizada para fazer alterações independentes no código.
      Caso a modificação na branch criada dê algum priblema,
      esta pode ser excluída sem alterar o código principal.
      ```
   4. Pull request
      ```
      Utilizada para solicitar a inclusão de uma alteração
      código na branch principal.
      ```
   5. Issues
      ```
      Utilizada para solicitar melhorias no código.
      ```
   6. Feature branch
      ```
      Utilizada por outro contribuidor para fazer melhorias em seu código.
      ```
   7. Tag
      ```
      Marca a distribuição de uma release.
      ```

   
2. Virtualenv
   1. Criar
      ```console
      python3 -m venv .venv
      ```
   2. Ativar
      ```console
      source .venv/bin/activate
      ```
   3. Desativar
      ```console
      deactivate
      ```


3. Pip
   1. Instalar
      ```console
      pip install -r requirements.txt
      ```
   2. Atualizar
      ```console
      pip install --upgrade requests
      ```
   3. Desinstalar
      ```console
      pip uninstall -r requirements.txt -y
      ```
   4. Requirements
      ```console
      pip freeze > requirements.txt
      ```
   5. Flake8
      1. Instalar
         ```console
         pip install flake8
         ```
      2. Configurar 
         ```console
         # Crie um arquivo .flake8
         # Insira no arquivo .flake8 as configurações abaixo (sem o #)
         # [flake8]
         # max-line-length = 120
         # exclude = .venv
         ```
      3. Conferir qualidade do código
         ```console
         flake8
         ```
4. Travis CI
   [![Build Status](https://www.travis-ci.com/victorbaptistalemos/libpythonpro.svg?branch=main)](https://www.travis-ci.com/victorbaptistalemos/libpythonpro)
   

5. PyUp 
   [![Updates](https://pyup.io/repos/github/victorbaptistalemos/libpythonpro/shield.svg)](https://pyup.io/repos/github/victorbaptistalemos/libpythonpro/)
   [![Python 3](https://pyup.io/repos/github/victorbaptistalemos/libpythonpro/python-3-shield.svg)](https://pyup.io/repos/github/victorbaptistalemos/libpythonpro/)


6. PyPI
   1. Instalação do twine
      ```console
      pip install twine
      ```
   2. Criação de distribuição
      ```console
      python setup.py sdist
      ```
   3. Envio da distribuição ao PyPI
      ```console
      twine upload dist/*
      ```


7. PyTest
   1. Instalaçáo
      ```console
      pip install pytest
      ```
   2. Criando testes e a utilização da palavra reservada `assert`
   3. Cobertura de testes: [![codecov](https://codecov.io/gh/victorbaptistalemos/libpythonpro/branch/main/graph/badge.svg?token=5YMELE1KML)](https://codecov.io/gh/victorbaptistalemos/libpythonpro)
   4. Desenvolvimento Orientado a Testes (TDD).
   5. Parametrização de testes com o decorator `@pytest.mark.parametrize`
   6. Técnica do baby steps (desenvolvimento passo a passo).
   7. Testes de Exceções.
   8. PyTest Fixtures
   9. Utilização da palavra reservada `yield`
