from langchain.tools import tool
import PyPDF2
import shutil
import os
from langgraph.prebuilt import ToolNode
from src.agent.agents import llm_groq
from src.ui.console_ui import ConsoleUI

ui = ConsoleUI()

class Tools:
    @tool(description="""
        Lista conteúdo de diretórios.

        ESTRATÉGIA DE NAVEGAÇÃO:
        - Explore INCREMENTALMENTE: /home → /home/username → /home/username/Documents
        - NUNCA assuma caminhos completos de uma vez
        - Use resultados anteriores para informar próximo passo

        FLUXO:
        1. Comece do diretório mais genérico conhecido
        2. Analise o resultado
        3. Navegue um nível mais profundo
        4. Repita até encontrar o alvo

        EXEMPLO:
        User: "vá na pasta de downloads"
        Passo 1: list_dir("/home") → vê ['user_example']
        Passo 2: list_dir("/home/user123") → vê ['Downloads', 'Documents']
        Passo 3: list_dir("/home/user123/Downloads") → objetivo alcançado

        EVITE:
        ❌ list_dir("/home/user/Downloads") sem confirmar 'user' existe
        ✅ list_dir("/home") → confirmar → list_dir("/home/user_real")
        """)
    def list_directory(path: str) -> str:
        ui.show_tool_action('list_directory', path)
        try:
            items = os.listdir(path)
            return "\n".join(items)
        except Exception as e:
            return f"Erro: {str(e)}"

    @tool(description="""
        Verifica a existência de arquivo ou diretório.
        
        Args:
            path: Caminho a ser verificado
            
        Returns:
            Mensagem informando se existe ou não
        """)
    def verify_if_exists(path: str) -> str:
        ui.show_tool_action('verify_if_exists', path)
        try:
            if os.path.exists(path):
                tipo = "diretório" if os.path.isdir(path) else "arquivo"
                return f"✓ '{path}' existe e é um {tipo}"
            else:
                return f"✗ '{path}' não existe"
        except Exception as e:
            return f"❌ Erro ao verificar: {str(e)}"
        
    @tool(description="""
        Cria um arquivo com conteúdo.
        
        Args:
            file_path: Caminho completo do arquivo a ser criado
            content: Conteúdo a ser escrito no arquivo (opcional)
            
        Returns:
            Mensagem de sucesso ou erro
        """)
    def create_file(file_path: str, content: str = "") -> str:
        ui.show_tool_action('create_file', file_path)
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return f"✓ Arquivo '{file_path}' criado com sucesso"
        except PermissionError:
            return f"❌ Erro: Sem permissão para criar '{file_path}'"
        except Exception as e:
            return f"❌ Erro ao criar arquivo: {str(e)}"
    
    @tool(description="""
        Cria um diretório.
        
        Args:
            dir_path: Caminho completo do diretório a ser criado
          
        Returns:
            Mensagem de sucesso ou erro
        """)
    def create_directory(dir_path: str) -> str:
        ui.show_tool_action('create_directory', dir_path)
        try:
            os.makedirs(dir_path, exist_ok=True)
            return f"✓ Diretório '{dir_path}' criado com sucesso"
        except PermissionError:
            return f"❌ Erro: Sem permissão para criar '{dir_path}'"
        except Exception as e:
            return f"❌ Erro ao criar diretório: {str(e)}"
    
    @tool(description="""
        Lê e retorna o conteúdo de um arquivo.
        
        Args:
            file_path: Caminho completo do arquivo a ser lido
            
        Returns:
            Conteúdo do arquivo ou mensagem de erro
        """)
    def read_file(file_path: str) -> str:
        ui.show_tool_action('read_file', file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return f"Conteúdo do arquivo '{file_path}':\n\n{content}"
        except FileNotFoundError:
            return f"❌ Erro: Arquivo '{file_path}' não encontrado"
        except PermissionError:
            return f"❌ Erro: Sem permissão para ler '{file_path}'"
        except Exception as e:
            return f"❌ Erro ao ler arquivo: {str(e)}"
            
    @tool(description="""
        Lê e retorna o conteúdo de um PDF.
        
        Args:
            file_path: Caminho completo do PDF a ser lido
            
        Returns:
            Conteúdo do arquivo ou mensagem de erro
        """)
    def read_pdf(file_path: str) -> str:
        ui.show_tool_action('read_pdf', file_path)
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return f"Conteúdo do PDF:\n\n{text}"
        except Exception as e:
            return f"❌ Erro ao ler PDF: {str(e)}"
        
    @tool(description="""
        Retorna informações de um arquivo.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Informações do arquivo (tamanho, datas, permissões)
        """)
    def get_file_info(file_path: str) -> str:
        ui.show_tool_action('get_file_info', file_path)
        try:
            stats = os.stat(file_path)
            from datetime import datetime
            
            tamanho = stats.st_size
            criado = datetime.fromtimestamp(stats.st_ctime).strftime('%d/%m/%Y %H:%M:%S')
            modificado = datetime.fromtimestamp(stats.st_mtime).strftime('%d/%m/%Y %H:%M:%S')
            
            info = f"""
    Informações de '{file_path}':
    - Tamanho: {tamanho} bytes ({tamanho / 1024:.2f} KB)
    - Criado em: {criado}
    - Modificado em: {modificado}
    - Tipo: {'Diretório' if os.path.isdir(file_path) else 'Arquivo'}
    """
            return info
        except FileNotFoundError:
            return f"❌ Erro: '{file_path}' não encontrado"
        except Exception as e:
            return f"❌ Erro ao obter informações: {str(e)}"
    
    @tool(description="""
        Edita/sobrescreve o conteúdo de um arquivo.
        
        Args:
            file_path: Caminho do arquivo a ser editado
            new_content: Novo conteúdo do arquivo
            
        Returns:
            Mensagem de sucesso ou erro
        """)
    def edit_file(file_path: str, new_content: str) -> str:
        ui.show_tool_action('edit_file', file_path)
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            return f"✓ Arquivo '{file_path}' editado com sucesso"
        except FileNotFoundError:
            return f"❌ Erro: Arquivo '{file_path}' não encontrado"
        except PermissionError:
            return f"❌ Erro: Sem permissão para editar '{file_path}'"
        except Exception as e:
            return f"❌ Erro ao editar arquivo: {str(e)}"
    
    @tool(description="""
        Renomeia arquivo ou diretório.
        
        Args:
            old_path: Caminho atual do arquivo/diretório
            new_path: Novo caminho/nome
            
        Returns:
            Mensagem de sucesso ou erro
        """)
    def rename(old_path: str, new_path: str) -> str:
        ui.show_tool_action('rename', old_path, new_path)
        try:
            os.rename(old_path, new_path)
            return f"✓ '{old_path}' renomeado para '{new_path}'"
        except FileNotFoundError:
            return f"❌ Erro: '{old_path}' não encontrado"
        except FileExistsError:
            return f"❌ Erro: '{new_path}' já existe"
        except PermissionError:
            return f"❌ Erro: Sem permissão para renomear"
        except Exception as e:
            return f"❌ Erro ao renomear: {str(e)}"
    
    @tool(description="""
        Move arquivo ou diretório.
        
        Args:
            source_path: Caminho do arquivo/diretório de origem
            destination_path: Caminho de destino
            
        Returns:
            Mensagem de sucesso ou erro
        """)
    def move(source_path: str, destination_path: str) -> str:
        ui.show_tool_action('move', source_path, destination_path)
        try:
            shutil.move(source_path, destination_path)
            return f"✓ '{source_path}' movido para '{destination_path}'"
        except FileNotFoundError:
            return f"❌ Erro: '{source_path}' não encontrado"
        except PermissionError:
            return f"❌ Erro: Sem permissão para mover"
        except Exception as e:
            return f"❌ Erro ao mover: {str(e)}"
    
    @tool(description="""
        Copia arquivo ou diretório.
        
        Args:
            source_path: Caminho do arquivo/diretório de origem
            destination_path: Caminho de destino
            
        Returns:
            Mensagem de sucesso ou erro
        """)
    def copy(source_path: str, destination_path: str) -> str:
        ui.show_tool_action('copy', source_path, destination_path)
        try:
            if os.path.isfile(source_path):
                shutil.copy2(source_path, destination_path)
                return f"✓ Arquivo copiado de '{source_path}' para '{destination_path}'"
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                return f"✓ Diretório copiado de '{source_path}' para '{destination_path}'"
            else:
                return f"❌ Erro: '{source_path}' não encontrado"
        except FileExistsError:
            return f"❌ Erro: '{destination_path}' já existe"
        except PermissionError:
            return f"❌ Erro: Sem permissão para copiar"
        except Exception as e:
            return f"❌ Erro ao copiar: {str(e)}"
    
    @tool(description="""
        Deleta um arquivo.
        
        Args:
            file_path: Caminho completo do arquivo a ser deletado
            
        Returns:
            Mensagem de sucesso ou erro
        """)
    def delete_file(file_path: str) -> str:
        ui.show_tool_action('delete_file', file_path)
        try:
            os.remove(file_path)
            return f"✓ Arquivo '{file_path}' deletado com sucesso"
        except FileNotFoundError:
            return f"❌ Erro: Arquivo '{file_path}' não encontrado"
        except IsADirectoryError:
            return f"❌ Erro: '{file_path}' é um diretório, não um arquivo"
        except PermissionError:
            return f"❌ Erro: Sem permissão para deletar '{file_path}'"
        except Exception as e:
            return f"❌ Erro ao deletar arquivo: {str(e)}"
    
    @tool(description="""
        Deleta um diretório completo.
        
        Args:
            dir_path: Caminho completo do diretório a ser deletado
            
        Returns:
            Mensagem de sucesso ou erro
        """)
    def delete_directory(dir_path: str) -> str:
        ui.show_tool_action('delete_directory', dir_path)
        try:
            shutil.rmtree(dir_path)
            return f"✓ Diretório '{dir_path}' deletado com sucesso"
        except FileNotFoundError:
            return f"❌ Erro: Diretório '{dir_path}' não encontrado"
        except PermissionError:
            return f"❌ Erro: Sem permissão para deletar '{dir_path}'"
        except Exception as e:
            return f"❌ Erro ao deletar diretório: {str(e)}"
    
    @tool(description="""
        Busca arquivos por nome.
        
        Args:
            directory: Diretório onde buscar
            filename: Nome do arquivo (pode ser parcial)
            
        Returns:
            Lista de arquivos encontrados
        """)
    def search_file(directory: str, filename: str) -> str:
        ui.show_tool_action('search_file', directory, filename)
        try:
            found = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if filename.lower() in file.lower():
                        found.append(os.path.join(root, file))
            
            if found:
                result = f"✓ Encontrados {len(found)} arquivo(s):\n"
                result += "\n".join(f"- {f}" for f in found)
                return result
            else:
                return f"✗ Nenhum arquivo com '{filename}' encontrado em '{directory}'"
        except PermissionError:
            return f"❌ Erro: Sem permissão para acessar '{directory}'"
        except Exception as e:
            return f"❌ Erro na busca: {str(e)}"

    tools_main = [
        list_directory,
        verify_if_exists,
        create_file,
        create_directory,
        read_file,
        read_pdf,
        get_file_info,
        rename,
        move,
        copy,
        delete_file,
        delete_directory,
        search_file,
    ]

    tool_node = ToolNode(tools_main)
    llm_with_tools = llm_groq.bind_tools(tools_main)