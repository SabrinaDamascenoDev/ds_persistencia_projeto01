from fastapi import APIRouter, status
from app.bd.minidb import MiniDB
from app.schemas.livro_schema import LivroSchema, LivroUpdateSchema

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





