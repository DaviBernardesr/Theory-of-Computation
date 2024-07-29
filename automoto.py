# Classe para representar um AFD (Autômato Finito Determinístico)
class AutomatoFinitoDeterministico:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados  # Conjunto de estados do AFD
        self.alfabeto = alfabeto  # Conjunto de símbolos do alfabeto
        self.transicoes = transicoes  # Mapeamento de transições (estado, símbolo) -> estado de destino
        self.estado_inicial = estado_inicial  # Estado inicial do AFD
        self.estados_finais = estados_finais  # Conjunto de estados finais do AFD

# Classe para representar um AFN (Autômato Finito Não Determinístico)
class AutomatoFinitoNaoDeterministico:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados  # Conjunto de estados do AFN
        self.alfabeto = alfabeto  # Conjunto de símbolos do alfabeto
        self.transicoes = transicoes  # Mapeamento de transições (estado, símbolo) -> conjunto de estados de destino
        self.estado_inicial = estado_inicial  # Estado inicial do AFN
        self.estados_finais = estados_finais  # Conjunto de estados finais do AFN

# Função para criar um AFD a partir das entradas do usuário
def criar_afd():
    # Solicita os estados, alfabeto e transições do usuário
    estados = set(input("Digite os estados separados por espaço: ").split())
    alfabeto = set(input("Digite o alfabeto separado por espaço: ").split())
    transicoes = {}

    # Inicializa o dicionário de transições
    for estado in estados:
        transicoes[estado] = {}

    # Define as transições para cada estado e símbolo
    for estado in estados:
        print(f"Definindo transições para o estado {estado}:")
        for simbolo in alfabeto:
            destino = input(f"  Destino para a transição {estado} --{simbolo}--> (deixe em branco para nenhum): ")
            if destino:
                transicoes[estado][simbolo] = destino

    # Solicita o estado inicial e os estados finais
    estado_inicial = input("Digite o estado inicial: ")
    estados_finais = set(input("Digite os estados finais separados por espaço: ").split())

    return AutomatoFinitoDeterministico(
        estados=estados,
        alfabeto=alfabeto,
        transicoes=transicoes,
        estado_inicial=estado_inicial,
        estados_finais=estados_finais
    )

# Função para imprimir a representação de um AFD
def imprimir_afd(afd):
    print("AFD:")
    print("Estados:", [list(s) for s in afd.estados])  # Exibe os estados
    print("Alfabeto:", afd.alfabeto)  # Exibe o alfabeto
    print("Transições:")
    # Exibe as transições
    for estado in afd.transicoes:
        for simbolo in afd.transicoes[estado]:
            print(f"  {list(estado)} --{simbolo}--> {list(afd.transicoes[estado][simbolo])}")
    print("Estado Inicial:", list(afd.estado_inicial))  # Exibe o estado inicial
    print("Estados Finais:", [list(s) for s in afd.estados_finais])  # Exibe os estados finais
    print()

# Função para criar um AFN a partir das entradas do usuário
def criar_afn():
    # Solicita os estados, alfabeto e transições do usuário
    estados = set(input("Digite os estados separados por espaço: ").split())
    alfabeto = set(input("Digite o alfabeto separado por espaço: ").split())
    transicoes = {}

    # Inicializa o dicionário de transições
    for estado in estados:
        transicoes[estado] = {}

    # Define as transições para cada estado e símbolo
    for estado in estados:
        print(f"Definindo transições para o estado {estado}:")
        for simbolo in alfabeto:
            destinos = set(input(f"  Destinos para a transição {estado} --{simbolo}--> (separe por espaço, deixe em branco para nenhum): ").split())
            if destinos:
                transicoes[estado][simbolo] = destinos

    # Solicita o estado inicial e os estados finais
    estado_inicial = input("Digite o estado inicial: ")
    estados_finais = set(input("Digite os estados finais separados por espaço: ").split())

    return AutomatoFinitoNaoDeterministico(
        estados=estados,
        alfabeto=alfabeto,
        transicoes=transicoes,
        estado_inicial=estado_inicial,
        estados_finais=estados_finais
    )

# Função para imprimir a representação de um AFN
def imprimir_afn(afn):
    print("AFN:")
    print("Estados:", afn.estados)  # Exibe os estados
    print("Alfabeto:", afn.alfabeto)  # Exibe o alfabeto
    print("Transições:")
    # Exibe as transições
    for estado, transicoes in afn.transicoes.items():
        for simbolo, destinos in transicoes.items():
            print(f"  {estado} --{simbolo}--> {destinos}")
    print("Estado Inicial:", afn.estado_inicial)  # Exibe o estado inicial
    print("Estados Finais:", afn.estados_finais)  # Exibe os estados finais
    print()

# Função para converter um AFN em um AFD
def converter_afn_para_afd(afn):
    novos_estados = []  # Lista para armazenar novos estados do AFD
    novas_transicoes = {}  # Dicionário para armazenar transições do AFD
    estado_inicial = frozenset([afn.estado_inicial])  # Estado inicial do AFD como um conjunto imutável
    novos_estados.append(estado_inicial)
    novas_transicoes[estado_inicial] = {}

    processar_estados = [estado_inicial]  # Lista para processar estados
    estados_finais = set()  # Conjunto de estados finais do AFD

    while processar_estados:
        estado_atual = processar_estados.pop()
        novas_transicoes[estado_atual] = {}

        for simbolo in afn.alfabeto:
            novos_estados_atuais = set()

            # Coleta os estados de destino para o símbolo atual
            for subestado in estado_atual:
                if subestado in afn.transicoes and simbolo in afn.transicoes[subestado]:
                    novos_estados_atuais.update(afn.transicoes[subestado][simbolo])

            novos_estados_atuais = frozenset(novos_estados_atuais)  # Converte os estados de destino para um conjunto imutável

            if novos_estados_atuais:
                novas_transicoes[estado_atual][simbolo] = novos_estados_atuais

                if novos_estados_atuais not in novos_estados:
                    novos_estados.append(novos_estados_atuais)
                    processar_estados.append(novos_estados_atuais)

                if novos_estados_atuais & set(afn.estados_finais):
                    estados_finais.add(novos_estados_atuais)

    return AutomatoFinitoDeterministico(
        estados=novos_estados,
        alfabeto=afn.alfabeto,
        transicoes=novas_transicoes,
        estado_inicial=estado_inicial,
        estados_finais=estados_finais
    )

# Função para simular a aceitação de uma palavra por um AFN
def simular_afn(afn, palavra):
    estados_atuais = {afn.estado_inicial}  # Começa com o estado inicial
    for simbolo in palavra:
        novos_estados = set()
        for estado in estados_atuais:
            if estado in afn.transicoes and simbolo in afn.transicoes[estado]:
                novos_estados.update(afn.transicoes[estado][simbolo])
        estados_atuais = novos_estados
    return bool(estados_atuais & afn.estados_finais)  # Retorna True se algum estado atual é final

# Função para simular a aceitação de uma palavra por um AFD
def simular_afd(afd, palavra):
    estado_atual = afd.estado_inicial  # Começa com o estado inicial
    for simbolo in palavra:
        if estado_atual in afd.transicoes and simbolo in afd.transicoes[estado_atual]:
            estado_atual = afd.transicoes[estado_atual][simbolo]
        else:
            return False
    return estado_atual in afd.estados_finais  # Retorna True se o estado final é um estado final

# Função para demonstrar a equivalência entre um AFN e um AFD para uma lista de palavras
def demonstrar_equivalencia(afn, afd, palavras):
    resultado = ""
    for palavra in palavras:
        aceito_afn = simular_afn(afn, palavra)
        aceito_afd = simular_afd(afd, palavra)
        resultado += f"Palavra: {palavra}\n"
        resultado += f"  Aceito pelo AFN: {aceito_afn}\n"
        resultado += f"  Aceito pelo AFD: {aceito_afd}\n"
        resultado += f"  Equivalente: {aceito_afn == aceito_afd}\n\n"
    return resultado

# Função para minimizar um AFD
def minimizar_afd(afd):
    # Particiona os estados em dois grupos: finais e não finais
    P = [afd.estados_finais, set(afd.estados) - set(afd.estados_finais)]
    W = [afd.estados_finais]  # Conjunto de estados a serem processados

    while W:
        A = W.pop()
        for simbolo in afd.alfabeto:
            X = set()
            # Encontra os estados que têm transição para um estado em A com o símbolo atual
            for estado in afd.estados:
                if simbolo in afd.transicoes.get(estado, {}) and afd.transicoes[estado][simbolo] in A:
                    X.add(estado)
            # Refina a partição com base em X
            for Y in P[:]:
                interseccao = X & Y
                diferenca = Y - X
                if interseccao and diferenca:
                    P.remove(Y)
                    P.append(interseccao)
                    P.append(diferenca)
                    if Y in W:
                        W.remove(Y)
                        W.append(interseccao)
                        W.append(diferenca)
                    else:
                        if len(interseccao) <= len(diferenca):
                            W.append(interseccao)
                        else:
                            W.append(diferenca)

    # Cria novos estados para a partição final
    novos_estados = {frozenset(particao) for particao in P}
    novo_estado_inicial = next(particao for particao in novos_estados if afd.estado_inicial in particao)
    novos_estados_finais = {particao for particao in novos_estados if particao & afd.estados_finais}

    novas_transicoes = {}
    for particao in novos_estados:
        estado_representante = next(iter(particao))
        novas_transicoes[particao] = {}
        for simbolo in afd.alfabeto:
            if simbolo in afd.transicoes[estado_representante]:
                estado_destino = afd.transicoes[estado_representante][simbolo]
                for destino in novos_estados:
                    if estado_destino in destino:
                        novas_transicoes[particao][simbolo] = destino
                        break

    return AutomatoFinitoDeterministico(
        estados=novos_estados,
        alfabeto=afd.alfabeto,
        transicoes=novas_transicoes,
        estado_inicial=novo_estado_inicial,
        estados_finais=novos_estados_finais
    )