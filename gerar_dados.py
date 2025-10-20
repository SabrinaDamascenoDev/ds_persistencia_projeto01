import random
from faker import Faker
from app.schemas.livro_schema import LivroSchema
from app.bd.minidb import MiniDB  # ajuste o caminho se necessário

fake = Faker('pt_BR')

GENEROS_POPULARES = [
    "Ficção Científica", "Fantasia", "Romance", "Suspense",
    "Mistério", "Thriller", "Drama", "Comédia",
    "Aventura", "História", "Biografia", "Poesia",
    "Autoajuda", "Tecnologia", "Infantil", "Horror",
    "Filosofia", "Política", "Negócios", "Culinária"
]

NUM_REGISTROS = 1000


def gerar_livro_fake() -> LivroSchema:
    """Gera um livro fictício."""
    titulo = fake.sentence(nb_words=random.randint(3, 8)).replace('.', '')
    autor = fake.name()
    quantidade_paginas = random.randint(50, 1500)
    editora = fake.company()
    deleted = False  # Ao criar, todos começam como não deletados
    genero = random.choice(GENEROS_POPULARES)

    return LivroSchema(
        titulo=titulo,
        autor=autor,
        quantidade_paginas=quantidade_paginas,
        editora=editora,
        deleted=deleted,
        genero=genero
    )


def povoar_bd(numero_registros: int = NUM_REGISTROS):
    """Povoa o MiniDB com livros fictícios."""
    db = MiniDB()  # usa a pasta app/bd por padrão
    print(f"🔄 Gerando {numero_registros} livros fictícios e salvando em '{db.path_csv}'...")

    for _ in range(numero_registros):
        livro = gerar_livro_fake()
        db.insert(livro)

    print(f"✅ {numero_registros} livros gerados e salvos com sucesso!")


if __name__ == "__main__":
    povoar_bd()
