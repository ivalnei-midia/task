# TaskFlow - Gerenciador de Tarefas

Um aplicativo moderno e eficiente para gerenciamento de tarefas criado com Streamlit.

## Funcionalidades

- Adicionar tarefas com diferentes níveis de prioridade
- Marcar tarefas como concluídas
- Filtrar tarefas por status (todas, pendentes, concluídas)
- Filtrar tarefas por nível de prioridade
- Visualizar estatísticas de progresso
- Interface responsiva e amigável

## Requisitos

- Python 3.8+
- Streamlit
- PostgreSQL (ou outro banco de dados compatível)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/taskflow.git
cd taskflow
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure a conexão com o banco de dados no arquivo `database.py`.

4. Execute o aplicativo:
```bash
streamlit run app.py
```

## Estrutura do Projeto

- `app.py`: Código principal da aplicação
- `database.py`: Configuração e conexão com o banco de dados
- `static/`: Arquivos estáticos (CSS, imagens)
  - `style.css`: Estilos da aplicação
  - `img/`: Pasta de imagens

## Screenshots

(Adicione screenshots da aplicação aqui)

## Desenvolvido por

Este projeto foi desenvolvido para a EBSERH. 