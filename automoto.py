class AFD:
    def __init__(self, ests, alfa, trans, ini, fins):
        self.ests = ests
        self.alfa = alfa
        self.trans = trans
        self.ini = ini
        self.fins = fins

class AFN:
    def __init__(self, ests, alfa, trans, ini, fins):
        self.ests = ests
        self.alfa = alfa
        self.trans = trans
        self.ini = ini
        self.fins = fins

def criar_afd():
    ests = set(input("Estados (separados por espaço): ").split())
    alfa = set(input("Alfabeto (separado por espaço): ").split())
    trans = {est: {} for est in ests}

    for est in ests:
        print(f"Transições para {est}:")
        for simb in alfa:
            dest = input(f"  {est} --{simb}--> (vazio para nenhum): ")
            if dest:
                trans[est][simb] = dest

    ini = input("Estado inicial: ")
    fins = set(input("Estados finais (separados por espaço): ").split())

    return AFD(ests, alfa, trans, ini, fins)

def criar_afn():
    ests = set(input("Estados (separados por espaço): ").split())
    alfa = set(input("Alfabeto (separado por espaço): ").split())
    trans = {est: {} for est in ests}

    for est in ests:
        print(f"Transições para {est}:")
        for simb in alfa:
            dests = set(input(f"  {est} --{simb}--> (separados por espaço, vazio para nenhum): ").split())
            if dests:
                trans[est][simb] = dests

    ini = input("Estado inicial: ")
    fins = set(input("Estados finais (separados por espaço): ").split())

    return AFN(ests, alfa, trans, ini, fins)

def afn_para_afd(afn):
    novos_ests = set()
    novas_trans = {}
    ini = frozenset([afn.ini])
    novos_ests.add(ini)
    novas_trans[ini] = {}

    a_processar = [ini]
    fins = set()

    while a_processar:
        atual = a_processar.pop()
        novas_trans[atual] = {}

        for simb in afn.alfa:
            novos_atuais = set()
            for sub in atual:
                if sub in afn.trans and simb in afn.trans[sub]:
                    novos_atuais.update(afn.trans[sub][simb])
            novos_atuais = frozenset(novos_atuais)

            if novos_atuais:
                novas_trans[atual][simb] = novos_atuais

                if novos_atuais not in novos_ests:
                    novos_ests.add(novos_atuais)
                    a_processar.append(novos_atuais)

                if novos_atuais & set(afn.fins):
                    fins.add(novos_atuais)

    return AFD(
        ests=novos_ests,
        alfa=afn.alfa,
        trans=novas_trans,
        ini=ini,
        fins=fins
    )

def imprimir_afd(afd):
    print("AFD:")
    print("Estados:", afd.ests)
    print("Alfabeto:", afd.alfa)
    print("Transições:")
    for est in afd.trans:
        for simb in afd.trans[est]:
            print(f"  {est} --{simb}--> {afd.trans[est][simb]}")
    print("Estado Inicial:", afd.ini)
    print("Estados Finais:", afd.fins)
    print()

def imprimir_afn(afn):
    print("AFN:")
    print("Estados:", afn.ests)
    print("Alfabeto:", afn.alfa)
    print("Transições:")
    for est, trans in afn.trans.items():
        for simb, dests in trans.items():
            print(f"  {est} --{simb}--> {dests}")
    print("Estado Inicial:", afn.ini)
    print("Estados Finais:", afn.fins)
    print()

def simular_afn(afn, palavra):
    atuais = {afn.ini}
    for simb in palavra:
        novos = set()
        for est in atuais:
            if est in afn.trans and simb in afn.trans[est]:
                novos.update(afn.trans[est][simb])
        atuais = novos
    return bool(atuais & afn.fins)

def simular_afd(afd, palavra):
    atual = afd.ini
    for simb in palavra:
        if atual in afd.trans and simb in afd.trans[atual]:
            atual = afd.trans[atual][simb]
        else:
            return False
    return atual in afd.fins

def minimizar_afd(afd):
    P = [afd.fins, set(afd.ests) - set(afd.fins)]
    W = [afd.fins]

    while W:
        A = W.pop()
        for simb in afd.alfa:
            X = set()
            for est in afd.ests:
                if simb in afd.trans.get(est, {}) and afd.trans[est][simb] in A:
                    X.add(est)
            for Y in P[:]:
                inter = X & Y
                dif = Y - X
                if inter and dif:
                    P.remove(Y)
                    P.append(inter)
                    P.append(dif)
                    if Y in W:
                        W.remove(Y)
                        W.append(inter)
                        W.append(dif)
                    else:
                        if len(inter) <= len(dif):
                            W.append(inter)
                        else:
                            W.append(dif)

    novos_ests = {frozenset(part) for part in P}
    novo_ini = next(part for part in novos_ests if afd.ini in part)
    novos_fins = {part for part in novos_ests if part & afd.fins}

    novas_trans = {}
    for part in novos_ests:
        rep = next(iter(part))
        novas_trans[part] = {}
        for simb in afd.alfa:
            if simb in afd.trans.get(rep, {}):
                dest = afd.trans[rep][simb]
                for part_dest in novos_ests:
                    if dest in part_dest:
                        novas_trans[part][simb] = part_dest
                        break

    return AFD(
        ests=novos_ests,
        alfa=afd.alfa,
        trans=novas_trans,
        ini=novo_ini,
        fins=novos_fins
    )

def verifica_equivalencia(afn, afd):
    afd = minimizar_afd(afd)

    def executa_afd(estado_inicial, transicoes, palavra):
        estado_atual = estado_inicial
        for simbolo in palavra:
            if simbolo in transicoes.get(estado_atual, {}):
                estado_atual = transicoes[estado_atual][simbolo]
            else:
                return False
        return estado_atual in afd.fins

    def gera_palavras(alfabeto):
        from itertools import product
        for i in range(1, 10):  # Limite do comprimento das palavras
            for palavra in product(alfabeto, repeat=i):
                yield ''.join(palavra)

    for palavra in gera_palavras(afd.alfa):  # Atualize para usar `afd.alfa`
        if executa_afd(afd.ini, afd.trans, palavra) != \
           simular_afn(afn, palavra):
            return False
    return True
