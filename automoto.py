class AFD:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

class AFN:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

def criar_afd():
    estados = set(input("Digite os estados separados por espaco: ").split())
    alfabeto = set(input("Digite o alfabeto separado por espaco: ").split())
    transicoes = {estado: {} for estado in estados}

    for estado in estados:
        print(f"Definindo transicoes para o estado {estado}:")
        for simbolo in alfabeto:
            destino = input(f"  Destino para a transicao {estado} --{simbolo}--> (deixe em branco para nenhum): ")
            if destino:
                transicoes[estado][simbolo] = destino

    estado_inicial = input("Digite o estado inicial: ")
    estados_finais = set(input("Digite os estados finais separados por espaco: ").split())

    return AFD(estados, alfabeto, transicoes, estado_inicial, estados_finais)

def imprimir_afd(afd):
    print("AFD:")
    print("Estados:", afd.estados)
    print("Alfabeto:", afd.alfabeto)
    print("Transicoes:")
    for estado in afd.transicoes:
        for simbolo in afd.transicoes[estado]:
            print(f"  {estado} --{simbolo}--> {afd.transicoes[estado][simbolo]}")
    print("Estado Inicial:", afd.estado_inicial)
    print("Estados Finais:", afd.estados_finais)
    print()

def criar_afn():
    estados = set(input("Digite os estados separados por espaco: ").split())
    alfabeto = set(input("Digite o alfabeto separado por espaco: ").split())
    transicoes = {estado: {} for estado in estados}

    for estado in estados:
        print(f"Definindo transicoes para o estado {estado}:")
        for simbolo in alfabeto:
            destinos = set(input(f"  Destinos para a transicao {estado} --{simbolo}--> (separe por espaco, deixe em branco para nenhum): ").split())
            if destinos:
                transicoes[estado][simbolo] = destinos

    estado_inicial = input("Digite o estado inicial: ")
    estados_finais = set(input("Digite os estados finais separados por espaco: ").split())

    return AFN(estados, alfabeto, transicoes, estado_inicial, estados_finais)

def imprimir_afn(afn):
    print("AFN:")
    print("Estados:", afn.estados)
    print("Alfabeto:", afn.alfabeto)
    print("Transicoes:")
    for estado, transicoes in afn.transicoes.items():
        for simbolo, destinos in transicoes.items():
            print(f"  {estado} --{simbolo}--> {destinos}")
    print("Estado Inicial:", afn.estado_inicial)
    print("Estados Finais:", afn.estados_finais)
    print()

def converter_afn_para_afd(afn):
    novos_estados = set()
    novas_transicoes = {}
    estado_inicial = frozenset([afn.estado_inicial])
    novos_estados.add(estado_inicial)
    novas_transicoes[estado_inicial] = {}

    processar_estados = [estado_inicial]
    estados_finais = set()

    while processar_estados:
        estado_atual = processar_estados.pop()
        novas_transicoes[estado_atual] = {}

        for simbolo in afn.alfabeto:
            novos_estados_atuais = set()
            for subestado in estado_atual:
                if subestado in afn.transicoes and simbolo in afn.transicoes[subestado]:
                    novos_estados_atuais.update(afn.transicoes[subestado][simbolo])
            novos_estados_atuais = frozenset(novos_estados_atuais)

            if novos_estados_atuais:
                novas_transicoes[estado_atual][simbolo] = novos_estados_atuais

                if novos_estados_atuais not in novos_estados:
                    novos_estados.add(novos_estados_atuais)
                    processar_estados.append(novos_estados_atuais)

                if novos_estados_atuais & set(afn.estados_finais):
                    estados_finais.add(novos_estados_atuais)

    return AFD(
        estados=novos_estados,
        alfabeto=afn.alfabeto,
        transicoes=novas_transicoes,
        estado_inicial=estado_inicial,
        estados_finais=estados_finais
    )

def simular_afn(afn, palavra):
    estados_atuais = {afn.estado_inicial}
    for simbolo in palavra:
        novos_estados = set()
        for estado in estados_atuais:
            if estado in afn.transicoes and simbolo in afn.transicoes[estado]:
                novos_estados.update(afn.transicoes[estado][simbolo])
        estados_atuais = novos_estados
    return bool(estados_atuais & afn.estados_finais)

def simular_afd(afd, palavra):
    estado_atual = afd.estado_inicial
    for simbolo in palavra:
        if estado_atual in afd.transicoes and simbolo in afd.transicoes[estado_atual]:
            estado_atual = afd.transicoes[estado_atual][simbolo]
        else:
            return False
    return estado_atual in afd.estados_finais

def verificar_equivalencia(afn, afd):
    afd = minimizar_afd(afd)

    def executa_afd(estado_inicial, transicoes, palavra):
        estado_atual = estado_inicial
        for simbolo in palavra:
            if simbolo in transicoes.get(estado_atual, {}):
                estado_atual = transicoes[estado_atual][simbolo]
            else:
                return False
        return estado_atual in afd.estados_finais

    def gera_palavras(alfabeto):
        from itertools import product
        for i in range(1, 10):  # Limite do comprimento das palavras
            for palavra in product(alfabeto, repeat=i):
                yield ''.join(palavra)

    for palavra in gera_palavras(afd.alfabeto):
        if executa_afd(afd.estado_inicial, afd.transicoes, palavra) != \
           simular_afn(afn, palavra):
            return False
    return True

def minimizar_afd(afd):
    P = [afd.estados_finais, set(afd.estados) - set(afd.estados_finais)]
    W = [afd.estados_finais]

    while W:
        A = W.pop()
        for simbolo in afd.alfabeto:
            X = set()
            for estado in afd.estados:
                if simbolo in afd.transicoes.get(estado, {}) and afd.transicoes[estado][simbolo] in A:
                    X.add(estado)
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

    novos_estados = {frozenset(particao) for particao in P}
    novo_estado_inicial = next(particao for particao in novos_estados if afd.estado_inicial in particao)
    novos_estados_finais = {particao for particao in novos_estados if particao & afd.estados_finais}

    novas_transicoes = {}
    for particao in novos_estados:
        estado_representante = next(iter(particao))
        novas_transicoes[particao] = {}
        for simbolo in afd.alfabeto:
            if simbolo in afd.transicoes.get(estado_representante, {}):
                estado_destino = afd.transicoes[estado_representante][simbolo]
                for destino in novos_estados:
                    if estado_destino in destino:
                        novas_transicoes[particao][simbolo] = destino
                        break

    return AFD(
        estados=novos_estados,
        alfabeto=afd.alfabeto,
        transicoes=novas_transicoes,
        estado_inicial=novo_estado_inicial,
        estados_finais=novos_estados_finais
    )
