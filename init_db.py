import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tabela de Usuários (conforme solicitado)
    cursor.execute('DROP TABLE IF EXISTS usuarios')
    cursor.execute('''
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        sobrenome TEXT NOT NULL,
        usuario TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    ''')

    # Tabela de Livros (mantendo a estrutura para a biblioteca)
    cursor.execute('DROP TABLE IF EXISTS livros')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        isbn TEXT,
        categoria TEXT,
        descricao TEXT,
        avaliacao DECIMAL DEFAULT 0.0,
        capa_url TEXT,
        quantidade_total INTEGER DEFAULT 1,
        quantidade_disponivel INTEGER DEFAULT 1
    )
    ''')

    # Dados de exemplo para livros (20 livros)
    livros_exemplo = [
        ('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', '978-8575031377', 'Infantil', 'Uma fábula poética e filosófica sobre um piloto que cai no Saara e encontra um jovem príncipe.', 4.8, 'https://m.media-amazon.com/images/I/81ibfYk4qmL.jpg'),
        ('1984', 'George Orwell', '978-8535914849', 'Ficção Científica', 'Um clássico distópico sobre vigilância governamental extrema e controle do pensamento.', 4.6, 'https://m.media-amazon.com/images/I/71kxa1-0mfL.jpg'),
        ('Dom Quixote', 'Miguel de Cervantes', '978-8582850022', 'Clássico', 'As aventuras de um fidalgo que enlouquece lendo romances de cavalaria e decide se tornar um cavaleiro.', 4.7, 'https://m.media-amazon.com/images/I/91zbi9M+mKL.jpg'),
        ('A Culpa é das Estrelas', 'John Green', '978-8580572261', 'Romance', 'Dois adolescentes com câncer se apaixonam e embarcam em uma jornada transformadora.', 4.9, 'https://m.media-amazon.com/images/I/81iqZ2HHD-L.jpg'),
        ('O Hobbit', 'J.R.R. Tolkien', '978-8595084742', 'Fantasia', 'Bilbo Bolseiro é levado em uma aventura épica para recuperar um tesouro guardado por um dragão.', 4.8, 'https://m.media-amazon.com/images/I/81hCVEC0ExL.jpg'),
        ('Dom Casmurro', 'Machado de Assis', '978-8535922004', 'Clássico', 'Bento Santiago narra sua história e sua obsessão pela dúvida sobre a fidelidade de Capitu.', 4.7, 'https://m.media-amazon.com/images/I/71X8X8xI-oL.jpg'),
        ('Harry Potter e a Pedra Filosofal', 'J.K. Rowling', '978-8532511010', 'Fantasia', 'Um órfão descobre que é um bruxo e começa sua educação na Escola de Magia de Hogwarts.', 4.9, 'https://m.media-amazon.com/images/I/81S6n8h-t7L.jpg'),
        ('O Alquimista', 'Paulo Coelho', '978-8575427583', 'Drama', 'O jovem pastor Santiago viaja em busca de um tesouro e descobre o sentido da vida.', 4.5, 'https://m.media-amazon.com/images/I/8176N+IcnTL.jpg'),
        ('O Senhor dos Anéis', 'J.R.R. Tolkien', '978-8595086357', 'Fantasia', 'A jornada de Frodo para destruir o Um Anel e salvar a Terra-média das trevas.', 4.9, 'https://m.media-amazon.com/images/I/81hCVEC0ExL.jpg'),
        ('Sherlock Holmes', 'Arthur Conan Doyle', '978-8537815236', 'Suspense', 'O brilhante detetive resolve mistérios intrigantes em Londres com seu parceiro Dr. Watson.', 4.8, 'https://m.media-amazon.com/images/I/819NshA-0sL.jpg'),
        ('O Código Da Vinci', 'Dan Brown', '978-8580570182', 'Suspense', 'Um simbologista desvenda segredos escondidos em obras de arte de Leonardo da Vinci.', 4.4, 'https://m.media-amazon.com/images/I/71R0mK9e+ML.jpg'),
        ('A Menina que Roubava Livros', 'Markus Zusak', '978-8580570472', 'Drama', 'A Morte narra a história de uma menina que encontra conforto nos livros na Alemanha nazista.', 4.9, 'https://m.media-amazon.com/images/I/91pXq-Nf6vL.jpg'),
        ('Orgulho e Preconceito', 'Jane Austen', '978-8582850350', 'Romance', 'As complexidades do amor e das classes sociais na Inglaterra do século XIX.', 4.8, 'https://m.media-amazon.com/images/I/712v6364m+L.jpg'),
        ('Fahrenheit 451', 'Ray Bradbury', '978-8525052247', 'Ficção Científica', 'Em uma sociedade onde os livros são proibidos, um bombeiro começa a questionar seu papel.', 4.6, 'https://m.media-amazon.com/images/I/817vXmQf3XL.jpg'),
        ('Admirável Mundo Novo', 'Aldous Huxley', '978-8525056009', 'Ficção Científica', 'Uma visão futurista de uma sociedade controlada por condicionamento e prazer artificial.', 4.5, 'https://m.media-amazon.com/images/I/818H5hC0LdL.jpg'),
        ('Drácula', 'Bram Stoker', '978-8537817117', 'Terror', 'O clássico conto do vampiro mais famoso do mundo e sua viagem da Transilvânia para Londres.', 4.7, 'https://m.media-amazon.com/images/I/8196R6V7fVL.jpg'),
        ('Frankenstein', 'Mary Shelley', '978-8537817094', 'Terror', 'Um cientista cria vida artificial e deve enfrentar as consequências de sua ambição.', 4.6, 'https://m.media-amazon.com/images/I/71Ew1-R9zTL.jpg'),
        ('Moby Dick', 'Herman Melville', '978-8582850497', 'Aventura', 'A obsessão do Capitão Ahab em caçar a baleia branca que o mutilou.', 4.3, 'https://m.media-amazon.com/images/I/91r48A-9l5L.jpg'),
        ('Cem Anos de Solidão', 'Gabriel García Márquez', '978-8501012074', 'Clássico', 'A saga multigeracional da família Buendía na mítica cidade de Macondo.', 4.8, 'https://m.media-amazon.com/images/I/818M9BfS89L.jpg'),
        ('O Retrato de Dorian Gray', 'Oscar Wilde', '978-8537814468', 'Clássico', 'Um jovem permanece belo enquanto seu retrato envelhece e reflete seus pecados.', 4.7, 'https://m.media-amazon.com/images/I/81E6NfT8r2L.jpg')
    ]
    
    cursor.executemany('INSERT INTO livros (titulo, autor, isbn, categoria, descricao, avaliacao, capa_url) VALUES (?, ?, ?, ?, ?, ?, ?)', livros_exemplo)

    # Tabela de Empréstimos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emprestimos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        id_livro INTEGER,
        data_emprestimo DATE,
        data_devolucao_prevista DATE,
        data_devolucao_real DATE,
        multa DECIMAL DEFAULT 0.0,
        status TEXT DEFAULT 'ativo',
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id),
        FOREIGN KEY (id_livro) REFERENCES livros (id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_db()
