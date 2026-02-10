# Importa a biblioteca JSON, utilizada geralmente para salvar dados em um arquivo (serializar) e carregar dados de um arquivo (desserializar). 
import json
# Importa a biblioteca OS, que é utilizada para interagir com o sistema operacional. Nesse caso, ela é exclusivamente utilizada para verificar se um arquivo existe no sistema operacional.
import os

# Atribui-se o nome do arquivo onde serão armazenados os clientes a uma variável constante.
NOME_ARQUIVO_CLIENTES = "clientes_point.json"
# Atribui-se um dicionário com as bases e seus respectivos preços a uma variável constante.
PRECOS_BASE = {"Leite": 4.35, "Maracujá": 4.60, "Rosa": 5.85, "Manga": 5.47}
# Atribui-se um dicionário com os complementos e seus respectivos preços a uma variável constante.
PRECOS_COMPLEMENTO = {"Boba": 0.50, "Lichia": 0.75, "Geleia": 0.65, "Taro": 1.00, "Chia": 0.35}

# A classe "Cliente" é criada. 
class Cliente:
    # Função que constroí a classe e serve para inicializar um objeto, tendo parâmetros generalizados caso o cliente não tenha especificidades.
    def __init__(self, nome, tipo = "comunidade", saldo_cashback = 0.0):
        # É criada uma variável de instância nome, que guarda o valor do parâmetro nome nela.
        self.nome = nome
        # É criada uma variável de instância tipo, que guarda o valor do parâmetro tipo nela.
        self.tipo = tipo
        # É criada uma variável de instância saldo_cashback, que guarda o valor do parâmetro saldo_cashback nela com verificação de tipo (float).
        self.saldo_cashback = float(saldo_cashback)

    # Função para controlar e obter descontos de acordo com o tipo do cliente.
    def obter_desconto(self):
        # Estrutura condicional onde se a variável de instância tipo for um estudante ou um professor/funcionário da UEFS, um desconto é obtido e vai ser futuramente calculado. Caso não, nenhum desconto é obtido.
        if self.tipo == "estudante":
            return 0.25 
        elif self.tipo == "professor_funcionario":
            return 1.00
        else:
            return 0.0

    # Função que é utilizada para organizar os dados em um dicionário. O nome não pertence a esse dicionário porque no arquivo JSON o nome já vai ser a chave.
    def criar_dicionario(self):
        return {"tipo": self.tipo, "saldo_cashback": self.saldo_cashback}

# A classe "Pedido" é criada. 
class Pedido:

    # Função que constroí a classe e serve para inicializar um objeto.
    def __init__(self, cliente, base, complementos):
        # É criada uma variável de instância cliente, que guarda o valor do parâmetro cliente nela.
        self.cliente = cliente
        # É criada uma variável de instância base, que guarda o valor do parâmetro base nela.
        self.base = base
        # É criada uma variável de instância complementos, que guarda o valor do parâmetro complementos nela.
        self.complementos = complementos

    # Função que calcula o valor bruto do pedido, ou seja, sem descontos ou cashback.
    def calcular_valor_bruto(self):
        # Atribui-se o preço da base (sistema chave-valor) a variável valor.
        valor = PRECOS_BASE[self.base]
        # Percorre todos os complementos escolhidos e atribui a variável valor um contador, para acumular o preço dos complementos.
        for complemento in self.complementos:
            valor += PRECOS_COMPLEMENTO[complemento]
        # Retorna a variável valor.
        return valor

    # Função que exibe um resumo do pedido. 
    def exibir_resumo_pedido(self, valor_final, cashback_usado):
        # Imprime os dados do pedido.
        print("\nRESUMO DO PEDIDO:")
        print(f"Cliente: {self.cliente.nome}")
        print(f"Base: {self.base}")
        # Estrutura condicional que verifica se foram escolhidos complementos ou não.
        if self.complementos:
            print(f"Adicionais: {', '.join(self.complementos)}")
        else:
            print("Adicionais: Nenhum")
        
        # Estrutura condicional que verifica se o cliente tem desconto especial e qual o seu tipo.
        if self.cliente.tipo == "estudante":
            print("Cliente com desconto especial de estudante")
        elif self.cliente.tipo == "professor_funcionario":
            print("Cliente com desconto especial de professor ou funcionário")

        # Imprime os dados do pedido.
        print(f"Valor Total: R$ {valor_final:.2f}")

        # Estrutura condicional que verifica o cashback usado e o saldo do mesmo.
        if cashback_usado > 0:
            print(f"Cashback utilizado: R$ {cashback_usado:.2f}")
        else:
            print("Cashback não utilizado.")

        # Imprime o saldo de cashback atualizado.
        print(f"Saldo de cashback atual: R$ {self.cliente.saldo_cashback:.2f}\n")

# A classe "GerenciadorClientes" é criada.
class GerenciadorClientes:

    # Função que constroí a classe.
    def __init__(self, arquivo):
        # É criada uma variável de instância arquivo, que guarda o valor do parâmetro arquivo nela.
        self.arquivo = arquivo
        # Nesse caso, o metódo _carregar() é chamado, que lê o arquivo e preenche uma estrutura de dados futura (self.clientes) com os clientes que já existem.
        self.clientes = self._carregar()

    # Função que define um metódo interno. 
    def _carregar(self):
        # Estrutura condicional que verifica se o arquivo de salvamento já existe.
        if not os.path.exists(self.arquivo):
            # Se o arquivo não existe um dicionário vazio é retornado.
            return {}

        # Tratamento de erros com try-except na tentativa de leitura do arquivo.
        try:
            # Funcionalidade que abre o arquivo no modo de leitura.
            with open(self.arquivo, 'r', encoding='utf-8') as arquivo_clientes:
                # Carrega o conteúdo do arquivo JSON e o converte para um dicionário Python.
                dados_carregados = json.load(arquivo_clientes)
                # Cria um dicionário vazio para armazenar os objetos (Cliente).
                objetos_cliente = {}
                # Estrutura de repetção que percorre o dicionário, obtendo o nome e os dados de cada cliente.
                for nome, dados in dados_carregados.items():
                    # Estrutura que constroí o perfil do cliente usando as informações lidas do arquivo.
                    objetos_cliente[nome] = Cliente(nome, dados['tipo'], dados['saldo_cashback'])
                # Retorna o dicionário preenchido com objetos (Cliente).
                return objetos_cliente
            
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def salvar(self):
        # Atribui-se um dicionário vazio a variável para armazenar os dados.
        dados_para_salvar = {}
        # Estrutura de repetição que percore o dicionário de clientes.
        for nome, objetos_cliente in self.clientes.items():
            # Estrutura onde cada objeto (Cliente_ chama o método que o converte para um dicionário.
            dados_para_salvar[nome] = objetos_cliente.criar_dicionario() 
        
        # Abre o arquivo no modo de escrita.
        with open(self.arquivo, 'w', encoding='utf-8') as arquivo_clientes:
            # Salva o dicionário de clientes no arquivo JSON, formatando-o para ser legível.
            json.dump(dados_para_salvar, arquivo_clientes, indent=4, ensure_ascii=False)

    def obter_cliente(self, nome):
        # Retorna o valor se a chave 'nome' existir.
        return self.clientes.get(nome)

    def registrar_cliente(self, cliente):
        # Funcionalidade para adicionar um novo objeto cliente ao dicionário.
        self.clientes[cliente.nome] = cliente

# A classe "SistemaBubbleTea" é criada.
class SistemaBubbleTea:

    # Função que constroí a classe.
    def __init__(self):
        # Quando o sistema iniciar, é criada uma instância do GerenciadorClientes.
        self.gerenciador_clientes = GerenciadorClientes(NOME_ARQUIVO_CLIENTES)

    # Função que obtém o menu de opções para o usuário.
    def _obter_escolha_menu(self, titulo, opcoes):
        # Imprime o título do menu.
        print(f"\n{titulo}")
        # Converte as chaves do dicionário de opções para uma lista.
        opcoes_lista = list(opcoes.keys())
        # Estrutura de repetição que enumera a lista de opções e exibe cada uma com seu preço.
        for i, opcao in enumerate(opcoes_lista, 1):
            print(f"{i}. {opcao} - R$ {opcoes[opcao]:.2f}")

        # Variável de controle do loop.
        entrada_valida = False
        # Loop que continua enquanto a entrada não for válida.
        while not entrada_valida:
            # Tratamento de erros.
            try:
                # Entrada de dados.
                escolha = int(input("Escolha uma opção: "))
                # Estrutura condicional que verifica se o número escolhido é válido.
                if 1 <= escolha <= len(opcoes_lista):
                    # Se for válido, a variável de controle se torna True.
                    entrada_valida = True
                    return opcoes_lista[escolha - 1]
                # Imprime um aviso.
                print("Opção inválida. Tente novamente.")
            except ValueError:
                # Se a entrada não puder ser convertida para um número, exibe uma mensagem de erro.
                print("Entrada inválida. Por favor, digite um número.")

    # Função que coleta as informações do pedido.
    def _coletar_informacoes_pedido(self):
        # Entrada de dados.
        nome_cliente = input("Digite o nome do cliente: ").strip().title()
        # Usa a funcionalidade do gerenciador para verificar se o cliente existe.
        cliente = self.gerenciador_clientes.obter_cliente(nome_cliente)

        # Estrutura condicional onde se o cliente não for encontrado, ele é um cliente novo.
        if not cliente:
            # Imprime uma frase.
            print("Cliente novo! Vamos fazer um rápido cadastro.")
            # Variável de controle para o loop.
            tipo_definido = False
            # Estrutura de repetição para garantir que um tipo de cliente válido seja escolhido.
            while not tipo_definido:
                # Entrada de dados.
                tipo_input = input("O cliente é (1) Estudante UEFS, (2) Professor/Funcionário UEFS ou (3) Comunidade? ")
                # Estrutura condicional que verifica o tipo de cliente.
                if tipo_input == '1':
                    tipo = "estudante"
                    tipo_definido = True
                elif tipo_input == '2':
                    tipo = "professor_funcionario"
                    tipo_definido = True
                elif tipo_input == '3':
                    tipo = "comunidade"
                    tipo_definido = True
                else:
                    print("Opção inválida.")
            # Cria um novo objeto Cliente com as informações coletadas.
            cliente = Cliente(nome_cliente, tipo)
            # Registra o novo cliente no gerenciador de clientes.
            self.gerenciador_clientes.registrar_cliente(cliente)

        # Usa um dos métodos para obter a escolha da base do chá.
        base_escolhida = self._obter_escolha_menu("BASES", PRECOS_BASE)

        # Atribui-se a uma variável uma lista vazia.
        complementos_escolhidos = []
        # Variável de controle para o loop.
        adicionando_complementos = True
        # Estrutura de repetição que permite que o cliente adicione vários complementos.
        while adicionando_complementos:
            # Imprime uma pergunta.
            print("\nAdicionar um complemento?")
            # Usa um dos métodos para obter a escolha do complemento.
            complemento = self._obter_escolha_menu("COMPLEMENTOS", PRECOS_COMPLEMENTO)
            # Adiciona o complemento escolhido à lista.
            complementos_escolhidos.append(complemento)
            
            # Variável de controle para o loop.
            continuar = True

            # Estrutura de repetição para continuar enquanto complementos ainda sejam adicionados.
            while continuar:
                # Entrada de dados
                resposta_continuar = input("Deseja adicionar outro complemento? (s/n): ").lower()
                if resposta_continuar in ("s", "n"):
                    # Interrupção de loop.
                    continuar = False 

                print("Opção inválida. Por favor, digite 's' ou 'n'.")
            
            # Estrutura condicional onde se o processo não continua, o loop é interrompido.
            if resposta_continuar == "n":
                adicionando_complementos = False

        # Retorna o objeto cliente e as escolhas de produtos.
        return cliente, base_escolhida, complementos_escolhidos

    # Função para o processamento do pedido.
    def processar_pedido(self):
        # Obtém todas as informações do pedido.
        cliente, base, complementos = self._coletar_informacoes_pedido()
        # Cria um objeto Pedido com as informações.
        pedido = Pedido(cliente, base, complementos)

        # Realização dos cálculos de preço e desconto.
        valor_bruto = pedido.calcular_valor_bruto()
        desconto = cliente.obter_desconto()

        # Aplica o desconto de acordo com o tipo de cliente.
        valor_com_desconto = valor_bruto
        # Estrutura condicional.
        if cliente.tipo == "estudante":
            valor_com_desconto -= valor_bruto * desconto
        elif cliente.tipo == "professor_funcionario":
            valor_com_desconto -= desconto

        # Cálculos do novo cashback do cliente.
        novo_cashback = valor_com_desconto * 0.10
        cashback_usado = 0.0

        # Estrutura condicional que verifica se o cliente tem saldo de cashback.
        if cliente.saldo_cashback > 0:
            # Imprime algumas informações do pedido.
            print(f"\nValor do pedido: R$ {valor_com_desconto:.2f}")
            print(f"Você possui R$ {cliente.saldo_cashback:.2f} de cashback.")
            usar = input("Deseja usar seu cashback? (s/n): ").lower()
            if usar == 's':
                # Usa o menor valor entre o saldo de cashback e o valor do pedido.
                cashback_usado = min(cliente.saldo_cashback, valor_com_desconto)
                # Variável contadora que subtrai o cashback usado do saldo do cliente.
                cliente.saldo_cashback -= cashback_usado

        # Calcula o valor final.
        valor_final = valor_com_desconto - cashback_usado
        # Adiciona o novo cashback ganho ao saldo do cliente.
        cliente.saldo_cashback += novo_cashback

        # Exibe o resumo do pedido.
        pedido.exibir_resumo_pedido(valor_final, cashback_usado)
        # Salva o estado atual de todos os clientes no arquivo JSON.
        self.gerenciador_clientes.salvar()

    # Função que inicia o programa principal.
    def iniciar(self):
        # Imprime uma frase de boas-vindas.
        print("Bem-vindo ao Ponto de Bubble Tea da UEFS!")
        # Variável de controle para do loop.
        processando_pedidos = True
        # Estrutura de repetição para o processamento de pedidos.
        while processando_pedidos:
            self.processar_pedido()
            # Entrada de dados.
            resposta_continuar = input("Deseja processar um novo pedido? (s/n): ").lower()
            # Estrutura condicional onde se o processo não continua, o loop é interrompido.
            if resposta_continuar != 's':
                processando_pedidos = False
        # Imprime uma frase.
        print("Obrigado e volte sempre!")

# Este bloco garante que o arquivo Python seja rodado diretamente.
if __name__ == "__main__":
    # Cria uma instância da classe principal do sistema.
    sistema = SistemaBubbleTea()
    # Chama o método iniciar() para começar o loop.
    sistema.iniciar()