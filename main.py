import tkinter as tk
from tkinter import messagebox
from automoto import (AFD, AFN, afn_para_afd, minimizar_afd, simular_afd, simular_afn, verifica_equivalencia)
from turing import TuringMachine


class TheoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automaton Simulator")
        self.root.geometry("800x800")

        self.afn = None
        self.afd = None
        self.tm = None
        self.current_mode = None

        # Interface
        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # AFN/AFD
        tk.Button(button_frame, text="Criar AFD", command=self.create_afd).pack(fill='x')
        tk.Button(button_frame, text="Criar AFN", command=self.create_afn).pack(fill='x')
        tk.Button(button_frame, text="Converter AFN para AFD", command=self.convert_afn_to_afd).pack(fill='x')
        tk.Button(button_frame, text="Minimizar AFD", command=self.minimize_afd).pack(fill='x')
        tk.Button(button_frame, text="Demonstrar Equivalência", command=self.demonstrate_equivalence).pack(fill='x')

        # TURING
        tk.Button(button_frame, text="Criar Máquina de Turing", command=self.create_turing_machine).pack(fill='x')

        self.entry_field = tk.Entry(self.root, width=90)
        self.entry_field.pack(padx=20, pady=10)

        # ENTER
        self.entry_field.bind('<Return>', self.handle_answer)

        self.current_question = None
        self.questions = []
        self.answers = []
        self.temp_transitions = []

        tk.Label(button_frame, text="Digite a palavra para simular:").pack(pady=5)
        self.word_entry = tk.Entry(button_frame, width=50)
        self.word_entry.pack(pady=5)
        self.simulate_button = tk.Button(button_frame, text="Simular AFD", command=self.simulate_afd, state='disabled')
        self.simulate_button.pack(pady=10)

        tk.Label(button_frame, text="Digite a palavra para simular na Máquina de Turing:").pack(pady=5)
        self.turing_word_entry = tk.Entry(button_frame, width=50)
        self.turing_word_entry.pack(pady=5)
        self.simulate_turing_button = tk.Button(button_frame, text="Simular Máquina de Turing",
                                                command=self.simulate_turing, state='disabled')
        self.simulate_turing_button.pack(pady=10)

        self.result_text = tk.Text(self.root, wrap='word', height=20, width=90)
        self.result_text.pack(padx=20, pady=20, expand=True)

    def create_afn(self):
        self.result_text.delete(1.0, tk.END)
        self.current_mode = "AFN"  # Define o modo atual como AFN
        self.questions = [
            "[AFN] Digite os estados separados por espaço:",
            "Digite o alfabeto separado por espaço:",
            "Digite uma transição no formato estado simbolo destino1 destino2 ... (ou deixe em branco para terminar):",
            "Digite o estado inicial:",
            "Digite os estados finais separados por espaço:"
        ]
        self.answers = []
        self.temp_transitions = []
        self.current_question = 0
        self.ask_next_question()

    def create_afd(self):
        self.result_text.delete(1.0, tk.END)
        self.current_mode = "AFD"  # Define o modo atual como AFD
        self.questions = [
            "[AFD] Digite os estados separados por espaço:",
            "Digite o alfabeto separado por espaço:",
            "Digite uma transição no formato estado simbolo destino (ou deixe em branco para terminar):",
            "Digite o estado inicial:",
            "Digite os estados finais separados por espaço:"
        ]
        self.answers = []
        self.temp_transitions = []
        self.current_question = 0
        self.ask_next_question()

    def create_turing_machine(self):
        self.result_text.delete(1.0, tk.END)
        self.questions = [
            "[Máquina de Turing] Digite os estados separados por espaço:",
            "Digite o alfabeto separado por espaço:",
            "Digite o alfabeto da fita separado por espaço:",
            "Digite uma transição no formato estado simbolo próximo_estado símbolo_escrita direção (L/R) (ou deixe em branco para terminar):",
            "Digite o estado inicial:",
            "Digite o estado de aceitação:",
            "Digite o estado de rejeição:"
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
            self.entry_field.delete(0, tk.END)
            self.process_answers()

    def handle_answer(self, event=None):
        answer = self.entry_field.get().strip()

        if not answer:
            if (self.current_question == 2 and self.current_mode in ["AFN", "AFD"]) or (
                    self.current_question == 3 and "Máquina de Turing" in self.questions[0]):
                self.answers.append(self.temp_transitions)
                self.temp_transitions = []
                self.current_question += 1
                self.ask_next_question()
            else:
                messagebox.showerror("Erro", "A resposta não pode estar vazia.")
            return

        if self.current_question == 3 and "Máquina de Turing" in self.questions[0]:  # Pergunta das transições de Turing
            if len(answer.split()) == 5:  # Formato esperado para uma transição
                self.temp_transitions.append(answer)
                self.result_text.insert(tk.END, f"Transição adicionada: {answer}\n")
            else:
                messagebox.showwarning("Aviso",
                                       "Formato de transição incorreto. Use: estado simbolo próximo_estado símbolo_escrita direção (L/R).")
            self.entry_field.delete(0, tk.END)
            self.entry_field.focus_set()

        elif self.current_question == 2 and self.current_mode in ["AFN", "AFD"]:  
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
        if len(self.answers) < len(self.questions):
            messagebox.showerror("Erro", "Responda todas as perguntas.")
            return

        if "Máquina de Turing" in self.questions[0]:
            self.process_turing_answers()
        else:
            self.process_afn_afd_answers()

    def process_turing_answers(self):
        estados = set(self.answers[0].split())
        alfabeto = set(self.answers[1].split())
        alfabeto_fita = set(self.answers[2].split())
        transicoes_input = self.answers[3]

        # Construir o dicionario de transições
        transicoes = {}
        for trans in transicoes_input:
            if len(trans.split()) == 5:
                estado, simbolo, prox_estado, simbolo_escrita, direcao = trans.split()
                # Adiciona a transic ao discionario
                transicoes[(estado, simbolo)] = (prox_estado, simbolo_escrita, direcao)

        estado_inicial = self.answers[4]  
        estado_aceitacao = self.answers[5]  
        estado_rejeicao = self.answers[6]  

        self.tm = TuringMachine(estados, alfabeto, alfabeto_fita, transicoes, estado_inicial, estado_aceitacao,
                                estado_rejeicao)

        self.result_text.insert(tk.END, "Máquina de Turing criada com sucesso!\n")
        self.result_text.insert(tk.END, self.get_turing_machine_description())

        self.simulate_turing_button.config(state='normal')

    def process_afn_afd_answers(self):
        estados = set(self.answers[0].split())
        alfabeto = set(self.answers[1].split())
        transicoes_input = self.answers[2]
        estado_inicial = self.answers[3]
        estados_finais = set(self.answers[4].split())

        transicoes = {}
        for trans in transicoes_input:
            partes = trans.split()
            if len(partes) >= 2:
                estado = partes[0]
                simbolo = partes[1]
                destinos = partes[2:]

                if estado not in transicoes:
                    transicoes[estado] = {}
                if simbolo not in transicoes[estado]:
                    transicoes[estado][simbolo] = []
                transicoes[estado][simbolo].extend(destinos)

        if self.current_mode == "AFN":
            self.afn = AFN(estados, alfabeto, transicoes, estado_inicial, estados_finais)
            self.result_text.insert(tk.END, "AFN criado com sucesso!\n")
            self.result_text.insert(tk.END, self.get_afn_description())
            self.simulate_button.config(state='normal')

        elif self.current_mode == "AFD":
            self.afd = AFD(estados, alfabeto, transicoes, estado_inicial, estados_finais)
            self.result_text.insert(tk.END, "AFD criado com sucesso!\n")
            self.result_text.insert(tk.END, self.get_afd_description())
            self.simulate_button.config(state='normal')

    def convert_afn_to_afd(self):
        if self.afn is None:
            messagebox.showerror("Erro", "Nenhum AFN foi criado.")
            return
        self.afd = afn_para_afd(self.afn)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "AFN convertido para AFD com sucesso!\n")
        self.result_text.insert(tk.END, self.get_afd_description())
        self.simulate_button.config(state='normal')

    def minimize_afd(self):
        if self.afd is None:
            messagebox.showerror("Erro", "Nenhum AFD foi criado.")
            return
        self.afd = minimizar_afd(self.afd)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "AFD minimizado com sucesso!\n")
        self.result_text.insert(tk.END, self.get_afd_description())

    def demonstrate_equivalence(self):
        if self.afn is None or self.afd is None:
            messagebox.showerror("Erro", "AFN e AFD devem estar criados para demonstrar equivalência.")
            return
        if verifica_equivalencia(self.afn, self.afd):
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "AFN e AFD são equivalentes!\n")
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "AFN e AFD NÃO são equivalentes.\n")

    def simulate_afd(self):
        if self.afd is None:
            messagebox.showerror("Erro", "Nenhum AFD foi criado.")
            return
        palavra = self.word_entry.get().strip()
        if not palavra:
            messagebox.showerror("Erro", "Digite uma palavra para simular.")
            return
        aceito = simular_afd(self.afd, palavra)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"A palavra '{palavra}' foi {'aceita' if aceito else 'rejeitada'} pelo AFD.\n")

    def simulate_turing(self):
        if self.tm is None:
            messagebox.showerror("Erro", "Nenhuma Máquina de Turing foi criada.")
            return
        palavra = self.turing_word_entry.get().strip()
        if not palavra:
            messagebox.showerror("Erro", "Digite uma palavra para simular na Máquina de Turing.")
            return
        resultado = self.tm.simulate(palavra)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"A palavra '{palavra}' foi {resultado} pela Máquina de Turing.\n")

    def get_afn_description(self):
        if not self.afn:
            return "AFN não criado."
        afn = self.afn
        description = (
            f"AFN:\n"
            f"Estados: {afn.ests}\n"
            f"Alfabeto: {afn.alfa}\n"
            f"Transições:\n"
        )
        for est, trans in afn.trans.items():
            for simb, dests in trans.items():
                description += f"  {est} --{simb}--> {', '.join(dests)}\n"
        description += (
            f"Estado Inicial: {afn.ini}\n"
            f"Estados Finais: {afn.fins}\n"
        )
        return description

    def get_afd_description(self):
        if not self.afd:
            return "AFD não criado."
        afd = self.afd
        description = (
            f"AFD:\n"
            f"Estados: {afd.ests}\n"
            f"Alfabeto: {afd.alfa}\n"
            f"Transições:\n"
        )
        for est, trans in afd.trans.items():
            for simb, dest in trans.items():
                description += f"  {est} --{simb}--> {dest}\n"
        description += (
            f"Estado Inicial: {afd.ini}\n"
            f"Estados Finais: {afd.fins}\n"
        )
        return description

    def get_turing_machine_description(self):
        if not self.tm:
            return "Máquina de Turing não criada."
        tm = self.tm
        description = (
            f"Máquina de Turing:\n"
            f"Estados: {tm.states}\n"
            f"Alfabeto: {tm.alphabet}\n"
            f"Alfabeto da Fita: {tm.tape_alphabet}\n"  
            f"Transições:\n"
        )
        for (estado, simbolo), (prox_estado, simbolo_escrita, direcao) in tm.transitions.items():
            description += f"  {estado} --{simbolo}--> {prox_estado}, {simbolo_escrita}, {direcao}\n"
        description += (
            f"Estado Inicial: {tm.initial_state}\n"  
            f"Estado de Aceitação: {tm.accept_state}\n"  
            f"Estado de Rejeição: {tm.reject_state}\n"
        )
        return description

#Inicializa
root = tk.Tk()
app = TheoryApp(root)
root.mainloop()
