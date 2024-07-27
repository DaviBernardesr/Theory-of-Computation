import tkinter as tk
from tkinter import messagebox
from automoto import (AutomatoFinitoNaoDeterministico, AutomatoFinitoDeterministico,
                      criar_afn, criar_afd, converter_afn_para_afd,
                      minimizar_afd, demonstrar_equivalencia, imprimir_afn, imprimir_afd)

class AutomatonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automaton Simulator")
        self.root.geometry("800x600")  # Tamanho da Tela.

        # Variaveis para armazenar AFN e AFD
        self.afn = None
        self.afd = None

        # Criar o layout da interface
        self.create_widgets()

    def create_widgets(self):
        # Frame para os botões
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # Botoes
        tk.Button(button_frame, text="Criar AFD", command=self.create_afd).pack(fill='x')
        tk.Button(button_frame, text="Criar AFN", command=self.create_afn).pack(fill='x')
        tk.Button(button_frame, text="Converter AFN para AFD", command=self.convert_afn_to_afd).pack(fill='x')
        tk.Button(button_frame, text="Minimizar AFD", command=self.minimize_afd).pack(fill='x')
        tk.Button(button_frame, text="Demonstrar Equivalência", command=self.demonstrate_equivalence).pack(fill='x')

        # Área de texto para mostrar resultados
        self.result_text = tk.Text(self.root, wrap='word', height=20, width=90)
        self.result_text.pack(padx=20, pady=20, expand=True)

    def create_afn(self):
        self.afn = criar_afn()
        self.result_text.insert(tk.END, "AFN Criado com sucesso!\n")
        self.result_text.insert(tk.END, self.get_afn_string())

    def create_afd(self):
        self.afd = criar_afd()
        self.result_text.insert(tk.END, "AFD Criado com sucesso!\n")
        self.result_text.insert(tk.END, self.get_afd_string())

    def convert_afn_to_afd(self):
        if not self.afn:
            messagebox.showerror("Erro", "Primeiro crie um AFN.")
            return

        self.afd = converter_afn_para_afd(self.afn)
        self.result_text.insert(tk.END, "AFN convertido para AFD com sucesso!\n")
        self.result_text.insert(tk.END, self.get_afd_string())

    def minimize_afd(self):
        if not self.afd:
            messagebox.showerror("Erro", "Primeiro crie um AFD.")
            return

        self.afd = minimizar_afd(self.afd)
        self.result_text.insert(tk.END, "AFD minimizado com sucesso!\n")
        self.result_text.insert(tk.END, self.get_afd_string())

    def demonstrate_equivalence(self):
        if not self.afn or not self.afd:
            messagebox.showerror("Erro", "Crie um AFN e converta-o para AFD antes de demonstrar equivalência.")
            return

        palavras = input("Digite as palavras para verificar equivalência, separadas por espaço: ").split()
        resultado = demonstrar_equivalencia(self.afn, self.afd, palavras)
        self.result_text.insert(tk.END, "Equivalência demonstrada:\n")
        self.result_text.insert(tk.END, resultado)

    def get_afn_string(self):
        if not self.afn:
            return ""
        result = "AFN:\n"
        result += f"Estados: {self.afn.estados}\n"
        result += f"Alfabeto: {self.afn.alfabeto}\n"
        result += "Transições:\n"
        for estado, transicoes in self.afn.transicoes.items():
            for simbolo, destinos in transicoes.items():
                result += f"  {estado} --{simbolo}--> {destinos}\n"
        result += f"Estado Inicial: {self.afn.estado_inicial}\n"
        result += f"Estados Finais: {self.afn.estados_finais}\n\n"
        return result

    def get_afd_string(self):
        if not self.afd:
            return ""
        result = "AFD:\n"
        result += f"Estados: {self.afd.estados}\n"
        result += f"Alfabeto: {self.afd.alfabeto}\n"
        result += "Transições:\n"
        for estado, transicoes in self.afd.transicoes.items():
            for simbolo, destino in transicoes.items():
                result += f"  {estado} --{simbolo}--> {destino}\n"
        result += f"Estado Inicial: {self.afd.estado_inicial}\n"
        result += f"Estados Finais: {self.afd.estados_finais}\n\n"
        return result

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatonApp(root)
    root.mainloop()
