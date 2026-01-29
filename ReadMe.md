## Projeto - API REST SOA

[![Active Development](https://img.shields.io/badge/Maintenance%20Level-Actively%20Developed-brightgreen.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)
![status](https://img.shields.io/badge/status-stable-green.svg) ![pyversions](https://img.shields.io/badge/python-3.14.0-blue)

[![Python Badge](https://img.shields.io/badge/-Python-22272e?style=for-the-badge&logo=python&logoColor=3776AB)](https://www.python.org/)
[![FastAPI Badge](https://img.shields.io/badge/-FastAPI-22272e?style=for-the-badge&logo=fastapi&logoColor=009688)](https://fastapi.tiangolo.com/)
[![SQLite Badge](https://img.shields.io/badge/-SQLite-22272e?style=for-the-badge&logo=sqlite&logoColor=003B57)](https://www.sqlite.org/)
[![Docker Badge](https://img.shields.io/badge/-Docker-22272e?style=for-the-badge&logo=docker&logoColor=2496ED)](https://www.docker.com/)
[![Linux Badge](https://img.shields.io/badge/-Linux-22272e?style=for-the-badge&logo=linux&logoColor=FCC624)](https://www.kernel.org/doc/html/latest/)


## Sumário
- [Introdução](#introdução)
- [Como rodar](#como-rodar)

## Introdução
Esse repositório aloca uma api rest com o principío de estruturação SOA(Service-Oriented Architecture).
A Arquitetura Orientada a Serviços (SOA) é um modelo arquitetural no qual o sistema é dividido em serviços independentes, cada um responsável por uma função de negócio bem definida, que se comunicam entre si por meio de interfaces padronizadas.

Esses serviços não dependem da implementação interna uns dos outros, apenas do contrato de comunicação.


## Como rodar
A maneira indicada de se executar esse projeto é instanciando o respectivo container da aplicação. Após clonar o repo do projeto, no diretório raiz execute o comando abaixo.
Com os arquivos baixados configurados, basta subir o container usando o docker:

```bash
docker compose up -d --build
```

Após o container orquestrara a inicialização.
