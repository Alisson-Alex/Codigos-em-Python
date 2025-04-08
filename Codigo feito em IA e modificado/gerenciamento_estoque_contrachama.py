import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass
import os

class CategoriaEnum(Enum):
    PLACAS = "Placas"
    ACOGALVANIZADO = "Aço galvanizado"
    ACOBRONZE = "Aço bronze"
    PVC = "PVC"
    OUTROS = "Outros"

@dataclass
class Localizacao:
    corredor: str
    prateleira: str
    posicao: str

    def __str__(self) -> str:
        return f"Corredor {self.corredor}, Prateleira {self.prateleira}, Posição {self.posicao}"

class BancoDeDados:
    def __init__(self, nome_banco: str = "estoque.db"):
        self.nome_banco = nome_banco
        self.criar_tabelas()

    def obter_conexao(self):
        return sqlite3.connect(self.nome_banco)

    def criar_tabelas(self):
        with self.obter_conexao() as conn:
            cursor = conn.cursor()
            
            # Tabela de Produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    codigo TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    preco REAL NOT NULL,
                    quantidade INTEGER DEFAULT 0,
                    quantidade_minima INTEGER DEFAULT 10,
                    quantidade_maxima INTEGER DEFAULT 100,
                    corredor TEXT,
                    prateleira TEXT,
                    posicao TEXT
                )
            ''')
            
            # Tabela de Movimentações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movimentacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_codigo TEXT,
                    data TIMESTAMP NOT NULL,
                    quantidade INTEGER NOT NULL,
                    tipo TEXT NOT NULL,
                    saldo INTEGER NOT NULL,
                    FOREIGN KEY (produto_codigo) REFERENCES produtos (codigo)
                )
            ''')
            
            conn.commit()

class SistemaEstoque:
    def __init__(self):
        self.db = BancoDeDados()

    def cadastrar_produto(self, 
                         codigo: str, 
                         nome: str, 
                         categoria: CategoriaEnum, 
                         preco: float,
                         quantidade_minima: int = 10,
                         quantidade_maxima: int = 100) -> None:
        with self.db.obter_conexao() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO produtos (codigo, nome, categoria, preco, 
                                        quantidade_minima, quantidade_maxima)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (codigo, nome, categoria.value, preco, quantidade_minima, quantidade_maxima))
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError(f"Produto com código {codigo} já existe")

    def atualizar_produto(self, 
                         codigo: str, 
                         nome: str = None, 
                         categoria: CategoriaEnum = None, 
                         preco: float = None,
                         quantidade_minima: int = None,
                         quantidade_maxima: int = None) -> None:
        with self.db.obter_conexao() as conn:
            cursor = conn.cursor()
            
            # Busca dados atuais do produto
            cursor.execute('SELECT * FROM produtos WHERE codigo = ?', (codigo,))
            produto = cursor.fetchone()
            if not produto:
                raise ValueError(f"Produto com código {codigo} não encontrado")
            
            # Atualiza apenas os campos fornecidos
            atualizacoes = {}
            if nome is not None:
                atualizacoes['nome'] = nome
            if categoria is not None:
                atualizacoes['categoria'] = categoria.value
            if preco is not None:
                atualizacoes['preco'] = preco
            if quantidade_minima is not None:
                atualizacoes['quantidade_minima'] = quantidade_minima
            if quantidade_maxima is not None:
                atualizacoes['quantidade_maxima'] = quantidade_maxima
            
            if atualizacoes:
                query = 'UPDATE produtos SET ' + ', '.join(f'{k} = ?' for k in atualizacoes.keys())
                query += ' WHERE codigo = ?'
                cursor.execute(query, (*atualizacoes.values(), codigo))
                conn.commit()

    def excluir_produto(self, codigo: str) -> None:
        with self.db.obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM produtos WHERE codigo = ?', (codigo,))
            if cursor.rowcount == 0:
                raise ValueError(f"Produto com código {codigo} não encontrado")
            conn.commit()

    def buscar_produto(self, codigo: str) -> Optional[Dict]:
        with self.db.obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT codigo, nome, categoria, preco, quantidade, 
                       quantidade_minima, quantidade_maxima,
                       corredor, prateleira, posicao
                FROM produtos 
                WHERE codigo = ?
            ''', (codigo,))
            produto = cursor.fetchone()
            
            if produto:
                return {
                    'codigo': produto[0],
                    'nome': produto[1],
                    'categoria': produto[2],
                    'preco': produto[3],
                    'quantidade': produto[4],
                    'quantidade_minima': produto[5],
                    'quantidade_maxima': produto[6],
                    'localizacao': Localizacao(produto[7], produto[8], produto[9]) if produto[7] else None
                }
            return None

    def listar_produtos(self) -> List[Dict]:
        with self.db.obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT codigo, nome, categoria, preco, quantidade, 
                       quantidade_minima, quantidade_maxima,
                       corredor, prateleira, posicao
                FROM produtos
            ''')
            produtos = cursor.fetchall()
            
            return [{
                'codigo': p[0],
                'nome': p[1],
                'categoria': p[2],
                'preco': p[3],
                'quantidade': p[4],
                'quantidade_minima': p[5],
                'quantidade_maxima': p[6],
                'localizacao': Localizacao(p[7], p[8], p[9]) if p[7] else None
            } for p in produtos]

    def atualizar_quantidade(self, codigo: str, quantidade: int, tipo_movimento: str) -> None:
        with self.db.obter_conexao() as conn:
            cursor = conn.cursor()
            
            # Verifica se o produto existe e obtém quantidade atual
            cursor.execute('SELECT quantidade FROM produtos WHERE codigo = ?', (codigo,))
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError(f"Produto com código {codigo} não encontrado")
            
            quantidade_atual = resultado[0]
            nova_quantidade = quantidade_atual + quantidade
            
            # Verifica se há quantidade suficiente para saída
            if tipo_movimento == "SAÍDA" and nova_quantidade < 0:
                raise ValueError(f"Quantidade insuficiente em estoque. Disponível: {quantidade_atual}")
            
            # Atualiza a quantidade do produto
            cursor.execute('''
                UPDATE produtos 
                SET quantidade = ?
                WHERE codigo = ?
            ''', (nova_quantidade, codigo))
            
            # Registra a movimentação
            cursor.execute('''
                INSERT INTO movimentacoes (produto_codigo, data, quantidade, tipo, saldo)
                VALUES (?, ?, ?, ?, ?)
            ''', (codigo, datetime.now(), quantidade, tipo_movimento, nova_quantidade))
            
            conn.commit()

    def entrada_estoque(self, codigo: str, quantidade: int) -> None:
        self.atualizar_quantidade(codigo, quantidade, "ENTRADA")

    def saida_estoque(self, codigo: str, quantidade: int) -> None:
        self.atualizar_quantidade(codigo, -quantidade, "SAÍDA")

    def atualizar_localizacao(self, codigo: str, localizacao: Localizacao) -> None:
        with self.db.obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE produtos
                SET corredor = ?, prateleira = ?, posicao = ?
                WHERE codigo = ?
            ''', (localizacao.corredor, localizacao.prateleira, localizacao.posicao, codigo))
            if cursor.rowcount == 0:
                raise ValueError(f"Produto com código {codigo} não encontrado")
            conn.commit()

    def gerar_relatorio_estoque_baixo(self) -> List[Dict]:
        with self.db.obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT codigo, nome, quantidade, quantidade_minima
                FROM produtos
                WHERE quantidade < quantidade_minima
            ''')
            return [{'codigo': r[0], 'nome': r[1], 'quantidade': r[2], 'minimo': r[3]} 
                   for r in cursor.fetchall()]

    def gerar_relatorio_estoque_excedente(self) -> List[Dict]:
        with self.db.obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT codigo, nome, quantidade, quantidade_maxima
                FROM produtos
                WHERE quantidade > quantidade_maxima
            ''')
            return [{'codigo': r[0], 'nome': r[1], 'quantidade': r[2], 'maximo': r[3]} 
                   for r in cursor.fetchall()]

    def gerar_relatorio_movimentacao(self, codigo: str, 
                                   data_inicio: datetime = None, 
                                   data_fim: datetime = None) -> List[Dict]:
        with self.db.obter_conexao() as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT data, quantidade, tipo, saldo
                FROM movimentacoes
                WHERE produto_codigo = ?
            '''
            params = [codigo]
            
            if data_inicio:
                query += ' AND data >= ?'
                params.append(data_inicio)
            if data_fim:
                query += ' AND data <= ?'
                params.append(data_fim)
            
            query += ' ORDER BY data DESC'
            
            cursor.execute(query, params)
            return [{
                'data': datetime.fromisoformat(str(r[0])),
                'quantidade': r[1],
                'tipo': r[2],
                'saldo': r[3]
            } for r in cursor.fetchall()]

class InterfaceEstoque:
    def __init__(self):
        self.sistema = SistemaEstoque()

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pausar(self):
        input("\nPressione ENTER para continuar...")

    def exibir_menu(self):
        while True:
            self.limpar_tela()
            print("=" * 40)
            print("SISTEMA DE GERENCIAMENTO DE ESTOQUE")
            print("=" * 40)
            print("\n1. Cadastrar novo produto")
            print("2. Atualizar produto")
            print("3. Excluir produto")
            print("4. Consultar produto")
            print("5. Listar todos os produtos")
            print("6. Registrar entrada de estoque")
            print("7. Registrar saída de estoque")
            print("8. Atualizar localização")
            print("9. Relatório de estoque baixo")
            print("10. Relatório de estoque excedente")
            print("11. Histórico de movimentação")
            print("12. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            try:
                if opcao == "1":
                    self.cadastrar_produto()
                elif opcao == "2":
                    self.atualizar_produto()
                elif opcao == "3":
                    self.excluir_produto()
                elif opcao == "4":
                    self.consultar_produto()
                elif opcao == "5":
                    self.listar_produtos()
                elif opcao == "6":
                    self.registrar_entrada()
                elif opcao == "7":
                    self.registrar_saida()
                elif opcao == "8":
                    self.atualizar_localizacao()
                elif opcao == "9":
                    self.relatorio_estoque_baixo()
                elif opcao == "10":
                    self.relatorio_estoque_excedente()
                elif opcao == "11":
                    self.historico_movimentacao()
                elif opcao == "12":
                    print("\nEncerrando o sistema...")
                    break
                else:
                    print("\nOpção inválida!")
                    self.pausar()
            except Exception as e:
                print(f"\nErro: {str(e)}")
                self.pausar()

    def cadastrar_produto(self):
        self.limpar_tela()
        print("=== Cadastro de Produto ===\n")
        
        codigo = input("Código do produto: ")
        nome = input("Nome do produto: ")
        
        print("\nCategorias disponíveis:")
        for i, categoria in enumerate(CategoriaEnum, 1):
            print(f"{i}. {categoria.value}")
        
        cat_index = int(input("\nEscolha a categoria (número): ")) - 1
        categoria = list(CategoriaEnum)[cat_index]
        
        preco = float(input("Preço do produto: "))
        qtd_min = int(input("Quantidade mínima: "))
        qtd_max = int(input("Quantidade máxima: "))

        self.sistema.cadastrar_produto(codigo, nome, categoria, preco, qtd_min, qtd_max)
        print("\nProduto cadastrado com sucesso!")
        self.pausar()

    def atualizar_produto(self):
        self.limpar_tela()
        print("=== Atualização de Produto ===\n")
        
        codigo = input("Código do produto: ")
        print("\nDeixe em branco os campos que não deseja atualizar")
        
        nome = input("Novo nome (ou Enter para manter): ")
        nome = nome if nome.strip() else None
        
        categoria = None
        cat_input = input("Nova categoria (número ou Enter para manter): ")
        if cat_input.strip():
            cat_index = int(cat_input) - 1
            categoria = list(CategoriaEnum)[cat_index]
        
        preco = None
        preco_input = input("Novo preço (ou Enter para manter): ")
        if preco_input.strip():
            preco = float(preco_input)
        
        qtd_min = None
        qtd_min_input = input("Nova quantidade mínima (ou Enter para manter): ")
        if qtd_min_input.strip():
            qtd_min = int(qtd_min_input)
        
        qtd_max = None
        qtd_max_input = input("Nova quantidade máxima (ou Enter para manter): ")
        if qtd_max_input.strip():
            qtd_max = int(qtd_max_input)

        self.sistema.atualizar_produto(codigo, nome, categoria, preco, qtd_min, qtd_max)
        print("\nProduto atualizado com sucesso!")
        self.pausar()

    def excluir_produto(self):
        self.limpar_tela()
        print("=== Exclusão de Produto ===\n")
        
        codigo = input("Código do produto: ")
        confirmacao = input(f"\nConfirma a exclusão do produto {codigo}? (S/N): ")
        
        if confirmacao.upper() == 'S':
            self.sistema.excluir_produto(codigo)
            print("\nProduto excluído com sucesso!")
        else:
            print("\nOperação cancelada!")
        self.pausar()

    def consultar_produto(self):
        self.limpar_tela()
        print("=== Consulta de Produto ===\n")
        
        codigo = input("Código do produto: ")
        produto = self.sistema.buscar_produto(codigo)
        
        if produto:
            print("\nInformações do Produto:")
            print(f"Código: {produto['codigo']}")
            print(f"Nome: {produto['nome']}")
            print(f"Categoria: {produto['categoria']}")
            print(f"Preço: R$ {produto['preco']:.2f}")
            print(f"Quantidade em estoque: {produto['quantidade']}")
            print(f"Quantidade mínima: {produto['quantidade_minima']}")
            print(f"Quantidade máxima: {produto['quantidade_maxima']}")
            if produto['localizacao']:
                print(f"Localização: {produto['localizacao']}")
            else:
                print("Localização: Não definida")
        else:
            print("\nProduto não encontrado!")
        
        self.pausar()

    def listar_produtos(self):
        self.limpar_tela()
        print("=== Lista de Produtos ===\n")
        
        produtos = self.sistema.listar_produtos()
        if produtos:
            for produto in produtos:
                print(f"Código: {produto['codigo']}")
                print(f"Nome: {produto['nome']}")
                print(f"Categoria: {produto['categoria']}")
                print(f"Quantidade: {produto['quantidade']}")
                print("-" * 30)
        else:
            print("Nenhum produto cadastrado.")
        
        self.pausar()

    def registrar_entrada(self):
        self.limpar_tela()
        print("=== Entrada de Estoque ===\n")
        
        codigo = input("Código do produto: ")
        quantidade = int(input("Quantidade a entrar: "))
        
        self.sistema.entrada_estoque(codigo, quantidade)
        print("\nEntrada registrada com sucesso!")
        self.pausar()

    def registrar_saida(self):
        self.limpar_tela()
        print("=== Saída de Estoque ===\n")
        
        codigo = input("Código do produto: ")
        quantidade = int(input("Quantidade a sair: "))
        
        self.sistema.saida_estoque(codigo, quantidade)
        print("\nSaída registrada com sucesso!")
        self.pausar()

    def atualizar_localizacao(self):
        self.limpar_tela()
        print("=== Atualização de Localização ===\n")
        
        codigo = input("Código do produto: ")
        corredor = input("Corredor: ")
        prateleira = input("Prateleira: ")
        posicao = input("Posição: ")
        
        localizacao = Localizacao(corredor, prateleira, posicao)
        self.sistema.atualizar_localizacao(codigo, localizacao)
        
        print("\nLocalização atualizada com sucesso!")
        self.pausar()

    def relatorio_estoque_baixo(self):
        self.limpar_tela()
        print("=== Relatório de Estoque Baixo ===\n")
        
        produtos = self.sistema.gerar_relatorio_estoque_baixo()
        if produtos:
            for produto in produtos:
                print(f"Código: {produto['codigo']}")
                print(f"Nome: {produto['nome']}")
                print(f"Quantidade atual: {produto['quantidade']}")
                print(f"Quantidade mínima: {produto['minimo']}")
                print("-" * 30)
        else:
            print("Nenhum produto com estoque baixo.")
        
        self.pausar()

    def relatorio_estoque_excedente(self):
        self.limpar_tela()
        print("=== Relatório de Estoque Excedente ===\n")
        
        produtos = self.sistema.gerar_relatorio_estoque_excedente()
        if produtos:
            for produto in produtos:
                print(f"Código: {produto['codigo']}")
                print(f"Nome: {produto['nome']}")
                print(f"Quantidade atual: {produto['quantidade']}")
                print(f"Quantidade máxima: {produto['maximo']}")
                print("-" * 30)
        else:
            print("Nenhum produto com estoque excedente.")
        
        self.pausar()

    def historico_movimentacao(self):
        self.limpar_tela()
        print("=== Histórico de Movimentação ===\n")
        
        codigo = input("Código do produto: ")
        data_inicio_str = input("Data início (dd/mm/aaaa) ou Enter para ignorar: ")
        data_fim_str = input("Data fim (dd/mm/aaaa) ou Enter para ignorar: ")
        
        data_inicio = None
        data_fim = None
        
        if data_inicio_str:
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
        if data_fim_str:
            data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
        
        movimentacoes = self.sistema.gerar_relatorio_movimentacao(codigo, data_inicio, data_fim)
        
        if movimentacoes:
            for mov in movimentacoes:
                print(f"Data: {mov['data'].strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"Tipo: {mov['tipo']}")
                print(f"Quantidade: {mov['quantidade']}")
                print(f"Saldo: {mov['saldo']}")
                print("-" * 30)
        else:
            print("Nenhuma movimentação registrada.")
        
        self.pausar()

if __name__ == "__main__":
    interface = InterfaceEstoque()
    interface.exibir_menu()
