from fastapi import APIRouter, HTTPException, status
from app.bd.minidb import MiniDB
from app.schemas.livro_schema import LivroSchema, LivroUpdateSchema
import hashlib
from pydantic import BaseModel
import zipfile, io, csv
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/api/Livros", 
    tags=["Livros"]
)

db = MiniDB()


#inserir livro

@router.post(
    path="/insert",
    response_model=list[LivroSchema],
    status_code=status.HTTP_201_CREATED
)
def create_livros(livros: list[LivroSchema]):
    livros_inseridos = []

    for livro in livros:
        db.insert(livro)
        livros_inseridos.append(livro)

    return livros_inseridos

        

#retornar os livros
@router.get(
    path="/get",
    status_code=status.HTTP_200_OK
)
def get_livros(pag: int=1, tam: int=10):
    registros=db.get_all(pag, tam)
    
    return registros

#atualizar livro

@router.put(
    path="/uptade",
    status_code=status.HTTP_201_CREATED
)
def uptade_livros(id: int, livro_up: LivroUpdateSchema):
    db.update(id, livro_up)

#delete livro

@router.delete(
    path="/delete",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_livros(id: int):
    db.delete(id)



#retornar a quantidade de livros
@router.get(
    path="/count",
    status_code=status.HTTP_200_OK
)
def get_count():
    quant=db.count()
    
    return quant


@router.post(
    path="/vacuum",
    status_code=status.HTTP_200_OK
)
def vacuum():
    db.vacuum()

class HashRequest(BaseModel):
    dado: str
    hash_type: str  # "MD5", "SHA1" ou "SHA256"


class HashResponse(BaseModel):
    hash: str

@router.post(
    path="/hash",
    response_model=HashResponse,
    status_code=status.HTTP_200_OK
)
def gerar_hash(req: HashRequest):
    """
    Recebe um dado e o tipo de hash (MD5, SHA1 ou SHA256)
    e retorna o hash correspondente.
    """
    hash_type = req.hash_type.upper()
    dado_bytes = req.dado.encode('utf-8')

    if hash_type == "MD5":
        h = hashlib.md5(dado_bytes).hexdigest()
    elif hash_type == "SHA1":
        h = hashlib.sha1(dado_bytes).hexdigest()
    elif hash_type == "SHA256":
        h = hashlib.sha256(dado_bytes).hexdigest()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="hash_type inválido. Use MD5, SHA1 ou SHA256."
        )

    return {"hash": h}

@router.get("/export_zip")
def exportar_bd_zip():
    # Pega todos os registros
    total = db.count() or 1_000_000_000
    registros = db.get_all(pagina=1, tamanho_pagina=total) or []

    # Cria CSV em memória
    csv_buffer = io.StringIO()
    if registros:
        writer = csv.DictWriter(csv_buffer, fieldnames=registros[0].keys())
        writer.writeheader()
        for linha in registros:
            writer.writerow(linha)

    csv_buffer.seek(0)

    # Cria ZIP em memória
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("bd.csv", csv_buffer.getvalue())

    zip_buffer.seek(0)

    # Retorna streaming do ZIP
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": 'attachment; filename="bd.zip"'}
    )