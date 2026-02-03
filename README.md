# 🤖 Termius - Agente de Terminal Inteligente

> Gerenciador de arquivos e diretórios via IA no terminal Linux

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)](https://langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange.svg)](https://groq.com/)

## 📋 Sobre

**Termius** é um agente de IA que opera via terminal, permitindo gerenciar arquivos e diretórios através de comandos em linguagem natural. Construído com LangChain, LangGraph e Groq LLM, oferece uma interface conversacional para operações do sistema de arquivos.

### ✨ Funcionalidades

- 📂 **Navegação de diretórios** - Liste e explore pastas
- 📄 **Criação de arquivos** - Crie arquivos com conteúdo
- 📁 **Gerenciamento de pastas** - Crie, mova, renomeie diretórios
- 📖 **Leitura de arquivos** - Leia textos e PDFs
- ✏️ **Edição de arquivos** - Modifique conteúdo
- 🔍 **Busca de arquivos** - Encontre arquivos por nome
- 🗑️ **Deleção segura** - Remove arquivos com confirmação
- 💾 **Histórico persistente** - Mantém contexto entre sessões

## 🚀 Instalação

### Pré-requisitos

- Python 3.10+
- Ubuntu/Linux
- Conta Groq (API Key gratuita)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/Gab-Angel/AI_terminal.git
cd termius
```

2. **Crie o ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
nano .env
```

Adicione sua chave da Groq:
```env
GROQ_API_KEY=sua_chave_aqui
PROMPT_MAIN=prompt_ai
```

5. **Torne o comando global** (opcional)
```bash
chmod +x termius
sudo cp termius /usr/local/bin/
```

## 🎯 Uso

### Modo Local
```bash
python main.py
```

### Modo Global (após instalação)
```bash
termius
```

### Exemplos de Comandos

```bash
# Navegação
▸ liste os arquivos aqui
▸ vá para a pasta Downloads
▸ mostre o que tem em /home/user/documentos

# Criação
▸ crie um arquivo teste.txt com o conteúdo "Hello World"
▸ crie uma pasta chamada projetos

# Leitura
▸ leia o arquivo config.json
▸ mostre o conteúdo do PDF relatorio.pdf

# Edição
▸ edite o arquivo notas.txt e adicione "Tarefa concluída"

# Busca
▸ procure arquivos com nome "projeto" na pasta atual

# Deleção
▸ delete o arquivo antigo.log
▸ remova a pasta temp
```

### Comandos Especiais

- `exit` - Sair do programa
- `0` - Limpar histórico de conversas

## 🏗️ Arquitetura

```
termius/
├── main.py                 # Entry point
├── termius                 # Script executável
├── src/
│   ├── agent/
│   │   └── agents.py       # Configuração LLM
│   ├── graph/
│   │   ├── state.py        # State do agente
│   │   ├── nodes.py        # Nós do grafo
│   │   ├── tools.py        # Ferramentas disponíveis
│   │   └── workflow.py     # Orquestração LangGraph
│   ├── db/
│   │   └── db_sqlite.py    # Persistência SQLite
│   ├── prompts/
│   │   ├── prompt_ai.j2    # Template do sistema
│   │   ├── rules.json      # Regras de negócio
│   │   └── get_prompt.py   # Carregador de prompts
│   └── ui/
│       ├── console_ui.py   # Interface Rich
│       └── animations.py   # Spinners e efeitos
└── checkpoints.db          # Histórico de conversas
```

## 🛠️ Tecnologias

- **[LangChain](https://langchain.com/)** - Framework para aplicações LLM
- **[LangGraph](https://langchain-ai.github.io/langgraph/)** - Orquestração de agentes
- **[Groq](https://groq.com/)** - Inference rápida de LLMs
- **[Rich](https://rich.readthedocs.io/)** - Interface de terminal estilizada
- **[SQLite](https://www.sqlite.org/)** - Persistência local
- **[Jinja2](https://jinja.palletsprojects.com/)** - Templates de prompts

## ⚙️ Configuração Avançada

### Modelos Disponíveis

Edite `src/agent/agents.py` para trocar o modelo:

```python
llm_groq = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model_name='llama-3.3-70b-versatile',  # Padrão recomendado
    # model_name='mixtral-8x7b-32768',     # Alternativa
    temperature=0,
)
```

### Customizar Prompts

Edite os arquivos em `src/prompts/`:
- `prompt_ai.j2` - Instruções do sistema
- `rules.json` - Variáveis do template

### Adicionar Novas Ferramentas

1. Crie a tool em `src/graph/tools.py`:
```python
@tool(description='Descrição da ferramenta')
def minha_tool(param: str) -> str:
    # Implementação
    return "resultado"
```

2. Adicione à lista `tools_main`

3. Atualize `rules.json` com o nome da tool

## 🔒 Segurança

- ⚠️ **Confirmação obrigatória** para deleções
- 🚫 **Validação de caminhos** para evitar operações perigosas
- 🔐 **API Key** nunca commitada (use .env)

## 🐛 Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'main'`
- Certifique-se que o caminho do projeto está correto em `termius`
- Verifique se executou `chmod +x termius`

### Erro: `groq.BadRequestError: Failed to parse tool call`
- Troque o modelo para `llama-3.3-70b-versatile`
- Verifique se a API key está válida

### Interface não aparece formatada
- Instale: `pip install rich`
- Verifique se o terminal suporta cores (True Color)

## 📝 Roadmap

- [ ] Suporte a múltiplos idiomas
- [ ] Integração com Git
- [ ] Análise de código
- [ ] Compressão de arquivos (zip/tar)
- [ ] Sincronização com cloud storage
- [ ] Web interface

## 🤝 Contribuindo

Contribuições são bem-vindas! 

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**Gabriel Angel**

- GitHub: [@Gab-Angel](https://github.com/Gab-Angel)

## 🙏 Agradecimentos

- Groq pela API de inference rápida
- LangChain pela framework robusta
- Comunidade open source

---

⭐ Se este projeto foi útil, considere dar uma estrela!