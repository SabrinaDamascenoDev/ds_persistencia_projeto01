import os
import csv
import pandas as pd
from app.bd.minidb import MiniDB
from app.schemas.livro_schema import LivroSchema, LivroUpdateSchema

db = MiniDB()

def main():
    livro1 = LivroSchema(
        titulo="O Senhor dos Anéis",
        autor="J.R.R. Tolkien",
        quantidade_paginas=1216,
        editora="HarperCollins",
        genero="Fantasia"
    )
    db.insert(livro1)

    
    total_livros =  db.count()
    print(f"Total de livros: {total_livros}")

    livros_pagina_1 =  db.get_all(pagina=1, tamanho_pagina=2)
    
    print("Livros na página 1:")
    for livro in livros_pagina_1:
        print(livro)
        livro_atualizado = LivroUpdateSchema(
            quantidade_paginas=1300
        )
        db.update(int(livro['id']), livro_atualizado)
    livro_especifico =  db.get_especifico(1)
    print("Livro específico (ID 1):", livro_especifico)

if __name__ == "__main__":
    main()
