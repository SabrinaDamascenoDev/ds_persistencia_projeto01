# ds-persistencia-t1

Pequeno projeto de persistência em CSV para livros — API REST construída com FastAPI e persistência simples em CSV.

## Requisitos
- Python 3.12 (ver [`.python-version`](.python-version))
- pip

## Instalação (local)
Recomenda-se criar um ambiente virtual:

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```


## Executando

1. Executar como exemplo (script demonstrativo):

```bash
python main.py
```

2. Executar como servidor HTTP (FastAPI + Uvicorn — recomendado para API):

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Observação: o comando acima pressupõe que o arquivo `main.py` exporta a instância FastAPI com o nome `app`. Se o nome for diferente, ajuste `main:app` para `<module>:<app_name>`.

Depois de subir o servidor, a documentação interativa estará disponível em:
- Swagger: http://127.0.0.1:8000/docs
- ReDoc:  http://127.0.0.1:8000/redoc

## Estrutura e arquivos principais
- main.py — ponto de entrada / cria a app FastAPI e demonstra uso
- app/bd/bd.csv — arquivo CSV que armazena os registros
- app/bd/bd.seq — arquivo com o último ID usado
- app/bd/minidb.py — implementação MiniDB (insert, get_all, get_especifico, update, delete, vacuum, count)
- app/schemas/livro_schema.py — schemas: LivroSchema e LivroUpdateSchema
- pyproject.toml — configurações do projeto (dependências listadas)

## Operações importantes
- Reiniciar IDs: editar `app/bd/bd.seq` com o número desejado (inteiro).
- Limpar registros marcados como deleted: chame `vacuum()` em `MiniDB`.
- Logs/depuração: use `--reload` durante desenvolvimento ou remova em produção.


## Referências rápidas
- Endpoints: veja `main.py` (rotas expostas pela FastAPI)
- Implementação DB: `app/bd/minidb.py`
- Schemas: `app/schemas/livro_schema.py`
- Dados: `app/bd/bd.csv`,