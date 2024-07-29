import tkinter as tk
from tkinter import messagebox
from automoto import (AutomatoFinitoNaoDeterministico, AutomatoFinitoDeterministico,
                      converter_afn_para_afd, minimizar_afd, demonstrar_equivalencia)

class AutomatonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automaton Simulator")
        self.root.geometry("800x600")

        # Variáveis para armazenar AFN e AFD
        self.afn = None
        self.afd = None

        # Criar o layout da interface
        self.create_widgets()

    def create_widgets(self):
        # Frame para os botões
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # Botões
        tk.Button(button_frame, text="Criar AFD", command=self.create_afd).pack(fill='x')
        tk.Button(button_frame, text="Criar AFN", command=self.create_afn).pack(fill='x')
        tk.Button(button_frame, text="Converter AFN para AFD", command=self.convert_afn_to_afd).pack(fill='x')
        tk.Button(button_frame, text="Minimizar AFD", command=self.minimize_afd).pack(fill='x')
        tk.Button(button_frame, text="Demonstrar Equivalência", command=self.demonstrate_equivalence).pack(fill='x')

        # Área de texto para mostrar perguntas e resultados
        self.result_text = tk.Text(self.root, wrap='word', height=20, width=90)
        self.result_text.pack(padx=20, pady=20, expand=True)

        # Campo de entrada para as respostas das perguntas
        self.entry_field = tk.Entry(self.root, width=90)
        self.entry_field.pack(padx=20, pady=10)

        # Configurar o evento de Enter para o campo de entrada
        self.entry_field.bind('<Return>', self.handle_answer)

        # Inicializar variáveis de perguntas e respostas
        self.current_question = None
        self.questions = []
        self.answers = []

        # Variável para armazenar as transições temporariamente
        self.temp_transitions = []

    def create_afn(self):
        self.result_text.delete(1.0, tk.END)
        self.questions = [
            "Digite os estados separados por espaço:",
            "Digite o alfabeto separado por espaço:",
            "Digite uma transição no formato estado simbolo destino (ou deixe em branco para terminar):",
            "Digite o estado inicial:",
            "Digite os estados finais separados por espaço:"
        ]
        self.answers = []
        self.temp_transitions = []
        self.current_question = 0
        self.ask_next_question()

    def create_afd(self):
        self.result_text.delete(1.0, tk.END)
        self.questions = [
            "Digite os estados separados por espaço:",
            "Digite o alfabeto separado por espaço:",
            "Digite uma transição no formato estado simbolo destino (ou deixe em branco para terminar):",
            "Digite o estado inicial:",
            "Digite os estados finais separados por espaço:"
        ]
        self.answers = []
        self.temp_transitions = []
        self.current_question = 0
        self.ask_next_question()

    def ask_next_question(self):
        if self.current_question < len(self.questions):
            self.result_text.insert(tk.END, self.questions[self.current_question] + "\n")
            self.entry_field.delete(0, tk.END)
            self.entry_field.focus_set()
        else:
            self.process_answers()

    def handle_answer(self, event=None):
        answer = self.entry_field.get().strip()
        if not answer:
            if self.current_question == 2:  # Pergunta das transições
                self.answers.append(self.temp_transitions)
                self.temp_transitions = []
                self.current_question += 1
                self.ask_next_question()
            else:
                messagebox.showerror("Erro", "A resposta não pode estar vazia.")
            return

        if self.current_question == 2:  # Pergunta das transições
            self.temp_transitions.append(answer)
            self.result_text.insert(tk.END, f"Transição adicionada: {answer}\n")
            self.entry_field.delete(0, tk.END)
            self.entry_field.focus_set()
        else:
            self.answers.append(answer)
            self.current_question += 1
            self.result_text.insert(tk.END, f"Resposta recebida: {answer}\n")
            self.ask_next_question()

    def process_answers(self):
        # Verificar se todas as respostas foram recebidas corretamente
        if len(self.answers) < 5:
            messagebox.showerror("Erro", "Responda todas as perguntas.")
            return

        estados = set(self.answers[0].split())
        alfabeto = set(self.answers[1].split())
        transicoes_input = self.answers[2]
        transicoes = {}
        for trans in transicoes_input:
            if len(trans.split()) != 3:
                continue
            estado, simbolo, destino = trans.split()
            if estado not in transicoes:
                transicoes[estado] = {}
            if simbolo not in transicoes[estado]:
                transicoes[estado][simbolo] = set()
            transicoes[estado][simbolo].add(destino)
        estado_inicial = self.answers[3]
        estados_finais = set(self.answers[4].split())

        if self.questions[0] == "Digite os estados separados por espaço:":
            self.afn = AutomatoFinitoNaoDeterministico(estados, alfabeto, transicoes, estado_inicial, estados_finais)
            self.result_text.insert(tk.END, "AFN Criado com sucesso!\n")
            self.result_text.insert(tk.END, self.get_afn_string())
        else:
            transicoes_afd = {k: {kk: next(iter(vv)) for kk, vv in v.items()} for k, v in transicoes.items()}
            self.afd = AutomatoFinitoDeterministico(estados, alfabeto, transicoes_afd, estado_inicial, estados_finais)
            self.result_text.insert(tk.END, "AFD Criado com sucesso!\n")
            self.result_text.insert(tk.END, self.get_afd_string())

    def convert_afn_to_afd(self):
        self.result_text.delete(1.0, tk.END)
        if not self.afn:
            messagebox.showerror("Erro", "Primeiro crie um AFN.")
            return

        self.afd = converter_afn_para_afd(self.afn)
        self.result_text.insert(tk.END, "AFN convertido para AFD com sucesso!\n")
        self.result_text.insert(tk.END, self.get_afd_string())

    def minimize_afd(self):
        self.result_text.delete(1.0, tk.END)
        if not self.afd:
            messagebox.showerror("Erro", "Primeiro crie um AFD.")
            return

        self.afd = minimizar_afd(self.afd)
        self.result_text.insert(tk.END, "AFD minimizado com sucesso!\n")
        self.result_text.insert(tk.END, self.get_afd_string())

    def demonstrate_equivalence(self):
        self.result_text.delete(1.0, tk.END)
        if not self.afn or not self.afd:
            messagebox.showerror("Erro", "Crie um AFN e converta-o para AFD antes de demonstrar equivalência.")
            return

        palavras = self.entry_field.get().split()
        resultado = demonstrar_equivalencia(self.afn, self.afd, palavras)
        self.result_text.insert(tk.END, "Equivalência demonstrada:\n")
        self.result_text.insert(tk.END, resultado)

    def get_afn_string(self):
        if not self.afn:
            return ""
        result = "AFN:\n"
        result += f"Estados: {', '.join(self.afn.estados)}\n"
        result += f"Alfabeto: {', '.join(self.afn.alfabeto)}\n"
        result += "Transições:\n"
        for estado, trans in self.afn.transicoes.items():
            for simbolo, destinos in trans.items():
                result += f"  {estado} --{simbolo}--> {', '.join(destinos)}\n"
        result += f"Estado inicial: {self.afn.estado_inicial}\n"
        result += f"Estados finais: {', '.join(self.afn.estados_finais)}\n"
        return result

    def get_afd_string(self):
        if not self.afd:
            return ""
        result = "AFD:\n"
        # Converte cada frozenset em string antes de usar join
        result += f"Estados: {', '.join(map(lambda s: str(s), self.afd.estados))}\n"
        result += f"Alfabeto: {', '.join(self.afd.alfabeto)}\n"
        result += "Transições:\n"
        for estado, transicoes in self.afd.transicoes.items():
            for simbolo, destino in transicoes.items():
                result += f"  {estado} --{simbolo}--> {destino}\n"
        result += f"Estado Inicial: {self.afd.estado_inicial}\n"
        # Converte cada frozenset em string antes de usar join
        result += f"Estados Finais: {', '.join(map(lambda s: str(s), self.afd.estados_finais))}\n"
        return result


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatonApp(root)
    root.mainloop()