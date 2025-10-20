import os
import csv

from app.schemas.livro_schema import LivroSchema, LivroUpdateSchema



class MiniDB:
    
    def __init__(self, base_path: str = 'app/bd', csv_name: str = 'bd.csv', seq_name: str = 'bd.seq'):
        self.path =  base_path
        self.path_csv = os.path.join(self.path, csv_name)
        self.path_seq = os.path.join(self.path, seq_name)
        

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if not os.path.exists(self.path_seq):
            with open(self.path_seq, 'w') as f:
                f.write('0')
        else:
            with open(self.path_seq, 'r') as f:
                content = f.read().strip()
                if not content.isdigit():
                    with open(self.path_seq, 'w') as f:
                        f.write('0')
          


    def _incrementar_id(self) -> int:
        if not os.path.exists(self.path_seq):
            os.makedirs(self.path_seq)
            print(f"Pasta {self.path_seq} criada.")

        with open(self.path_seq, 'r') as f:
            ultimo = f.read().strip()
            if ultimo == "":
                proximo_id = 1
            else:
                proximo_id = int(ultimo) + 1

        with open(self.path_seq, 'w') as f:
            f.write(str(proximo_id))
        return proximo_id
    
    def insert(self, livro: LivroSchema):
        id = self._incrementar_id()
        livro_registro = {
            'id': id,
            'titulo': livro.titulo,
            'autor': livro.autor,
            'genero': livro.genero,
            'quantidade_paginas': livro.quantidade_paginas,
            'editora': livro.editora,
            'deleted': 'False'
        }
        arquivo_existe = os.path.exists(self.path_csv)

        with open(self.path_csv, 'a', newline="", encoding='utf-8') as file:
            header = ['id', 'titulo', 'autor', 'genero', 'quantidade_paginas', 'editora', 'deleted']
            writer = csv.DictWriter(file, fieldnames=header)
            
            if not arquivo_existe:
                writer.writeheader()

            writer.writerow(livro_registro)

    def get_all(self, pagina: int, tamanho_pagina: int):

        inicio = (pagina - 1) * tamanho_pagina
        fim = inicio + tamanho_pagina
        counter = 0
        resultados = []

        if not os.path.exists(self.path_csv):
            print("Arquivo CSV não encontrado.")
            return
        

        with open(self.path_csv, 'r', newline="", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for linha in reader:
                if linha['deleted'] != 'False':
                    continue
                if counter >= inicio and counter < fim:
                    resultados.append(linha)
                counter += 1
                if counter >= fim:
                    break   
        return resultados

    def get_especifico(self, id: int):
        if not os.path.exists(self.path_csv):
            print("Arquivo CSV não encontrado.")
            return None

        with open(self.path_csv, 'r', newline="", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for linha in reader:
                if int(linha['id']) == id and linha['deleted'] == 'False':
                    return linha
        return None

    def update(self, id: int, livro: LivroUpdateSchema):
        if not os.path.exists(self.path_csv):
            print("Arquivo CSV não encontrado.")
            return None
        
        temp_path = os.path.join(self.path, 'bd_temp.csv')
        elemento = self.get_especifico(id)
        for key, value in livro.model_dump(exclude_unset=True).items():
            elemento[key] = value
        
        with open(self.path_csv, 'r', newline="", encoding='utf-8') as file, \
        open(temp_path, 'w', newline="", encoding='utf-8') as temp_file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            writer.writeheader()
            
            for linha in reader:
                if int(linha['id']) == id:
                    writer.writerow(elemento)
                else:
                    writer.writerow(linha)
        os.replace(temp_path, self.path_csv)

    def delete(self, id: int):
        if not os.path.exists(self.path_csv):
            print("Arquivo CSV não encontrado.")
            return None
        
        temp_path = os.path.join(self.path, 'bd_temp.csv')
        
        with open(self.path_csv, 'r', newline="", encoding='utf-8') as file, \
        open(temp_path, 'w', newline="", encoding='utf-8') as temp_file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            writer.writeheader()
            
            for linha in reader:
                if int(linha['id']) == id:
                    linha['deleted'] = 'True'
                    writer.writerow(linha)
                else:
                    writer.writerow(linha)
        os.replace(temp_path, self.path_csv)

    def vacuum(self):
        if not os.path.exists(self.path_csv):
            print("Arquivo CSV não encontrado.")
            return None
        
        temp_path = os.path.join(self.path, 'bd_temp.csv')
        with open(self.path_csv, 'r', newline="", encoding='utf-8') as file, \
        open(temp_path, 'w', newline="", encoding='utf-8') as temp_file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            writer.writeheader()
            
            for linha in reader:
                if linha['deleted'] == 'False':
                    writer.writerow(linha)
            os.replace(temp_path, self.path_csv)

    def count(self):
        if not os.path.exists(self.path_csv):
            print("Arquivo CSV não encontrado.")
            return None

        counter = 0
        with open(self.path_csv, 'r', newline="", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for linha in reader:
                if linha['deleted'] == 'False':
                    counter += 1
        return counter
