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
    print("Estados:", [list(s) for s in afd.estados])
    print("Alfabeto:", afd.alfabeto)
    print("Transicoes:")
    for estado in afd.transicoes:
        for simbolo in afd.transicoes[estado]:
            print(f"  {list(estado)} --{simbolo}--> {list(afd.transicoes[estado][simbolo])}")
    print("Estado Inicial:", list(afd.estado_inicial))
    print("Estados Finais:", [list(s) for s in afd.estados_finais])
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
    novos_estados = []
    novas_transicoes = {}
    estado_inicial = frozenset([afn.estado_inicial])
    novos_estados.append(estado_inicial)
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
                    novos_estados.append(novos_estados_atuais)
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

# Func para verificar usando produto cartesiano
def verificar_equivalencia(afn, afd, palavras=None):
    # Produto cartesiano de estados
    estados_produto = {(q1, q2) for q1 in afn.estados for q2 in afd.estados}
    estado_inicial_produto = (afn.estado_inicial, afd.estado_inicial)
    estados_finais_produto = {(q1, q2) for q1 in afn.estados_finais for q2 in afd.estados_finais}

    # Transic do produto
    transicoes_produto = {}
    for (q1, q2) in estados_produto:
        transicoes_produto[(q1, q2)] = {}
        for simbolo in afn.alfabeto.intersection(afd.alfabeto):
            destino_q1 = afn.transicoes.get(q1, {}).get(simbolo, None)
            destino_q2 = afd.transicoes.get(q2, {}).get(simbolo, None)
            if destino_q1 and destino_q2:
                transicoes_produto[(q1, q2)][simbolo] = (next(iter(destino_q1)), destino_q2)

    # Verificar se e aceito
    visitados = set()
    a_visitar = [estado_inicial_produto]

    while a_visitar:
        (q1_atual, q2_atual) = a_visitar.pop()
        if (q1_atual in afn.estados_finais) != (q2_atual in afd.estados_finais):
            return False  # AFN e AFD não são equivalentes
        visitados.add((q1_atual, q2_atual))
        for simbolo in afn.alfabeto.intersection(afd.alfabeto):
            proximo_estado = transicoes_produto.get((q1_atual, q2_atual), {}).get(simbolo, None)
            if proximo_estado and proximo_estado not in visitados:
                a_visitar.append(proximo_estado)

    return True  # AFN e AFD são equivalentes

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
            if simbolo in afd.transicoes[estado_representante]:
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
