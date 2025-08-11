import math
import tkinter as tk
from tkinter import messagebox

clan_bonuses = {
    "Aburame":      {'vida': 20, 'chakra': 80, 'ninjutsu': 50, 'speed': 50, 'taijutsu': 20},
    "Chinoike":     {'vida': 30, 'chakra': 60, 'ninjutsu': 60, 'speed': 30, 'taijutsu': 40},
    "Hatake":       {'vida': 20, 'chakra': 70, 'ninjutsu': 50, 'speed': 40, 'taijutsu': 40},
    "Hebi":         {'vida': 20, 'chakra': 70, 'ninjutsu': 50, 'speed': 50, 'taijutsu': 30},
    "Hoshigaki":    {'vida': 40, 'chakra': 60, 'ninjutsu': 60, 'speed': 30, 'taijutsu': 30},
    "Hyuuga":       {'vida': 30, 'chakra': 50, 'ninjutsu': 40, 'speed': 40, 'taijutsu': 60},
    "Kazekage":     {'vida': 30, 'chakra': 60, 'ninjutsu': 60, 'speed': 30, 'taijutsu': 40},
    "Lee":          {'vida': 20, 'chakra': 10, 'ninjutsu': 0,  'speed': 60, 'taijutsu': 90},
    "Nara":         {'vida': 20, 'chakra': 80, 'ninjutsu': 60, 'speed': 30, 'taijutsu': 30},
    "Kami":         {'vida': 25, 'chakra': 70, 'ninjutsu': 70, 'speed': 50, 'taijutsu': 10},
    "Raikage":      {'vida': 35, 'chakra': 50, 'ninjutsu': 30, 'speed': 80, 'taijutsu': 30},
    "Kyou":         {'vida': 40, 'chakra': 80, 'ninjutsu': 70, 'speed': 50, 'taijutsu': 10},
    "Sarutobi":     {'vida': 30, 'chakra': 60, 'ninjutsu': 55, 'speed': 40, 'taijutsu': 40},
    "Uchiha":       {'vida': 20, 'chakra': 70, 'ninjutsu': 50, 'speed': 50, 'taijutsu': 30},
    "Uzumaki":      {'vida': 35, 'chakra': 75, 'ninjutsu': 50, 'speed': 20, 'taijutsu': 45},
    "Yuki":         {'vida': 25, 'chakra': 65, 'ninjutsu': 60, 'speed': 40, 'kenjutsu': 35},
    "Senju":        {'vida': 35, 'chakra': 75, 'ninjutsu': 50, 'speed': 30, 'taijutsu': 35}
}

def rounding(valor):
    parte_decimal = valor - int(valor)
    return math.ceil(valor) if parte_decimal >= 0.5 else math.floor(valor)

def calculateStatus(request, bonus):
    try:
        forca = request.get('forca')
        chakra = request.get('chakra')
        destreza = request.get('destreza')

        vida = (forca * 0.75) + (chakra * 0.6) + (destreza * 0.5)
        chakra_result = (chakra * 0.5)
        speed = (destreza * 0.1)
        taijutsu = (forca * 0.2) + (destreza * 0.1)
        ninjutsu = (chakra * 0.2) + (destreza * 0.1)
        kenjutsu = (destreza * 0.2)
        stamina = (forca * 1.2) + (chakra * 1.2)

        # Aplicar bônus de clã
        vida *= 1 + (bonus.get('vida', 0) / 100)
        chakra_result *= 1 + (bonus.get('chakra', 0) / 100)
        speed *= 1 + (bonus.get('speed', 0) / 100)
        taijutsu *= 1 + (bonus.get('taijutsu', 0) / 100)
        ninjutsu *= 1 + (bonus.get('ninjutsu', 0) / 100)
        kenjutsu *= 1 + (bonus.get('kenjutsu', 0) / 100)

        return {
            '📌 Vida': rounding(vida),
            '📌 Chakra': rounding(chakra_result),
            '📌 Velocidade': rounding(speed),
            '📌 Ninjutsu': rounding(ninjutsu),
            '📌 Taijutsu': rounding(taijutsu),
            '📌 Kenjutsu': rounding(kenjutsu),
            '📌 Stamina': rounding(stamina)
        }
    except Exception as e:
        return {'error': str(e)}

def showResult(resultados):
    resultado_janela = tk.Toplevel()
    resultado_janela.title("Resultado dos Status")
    resultado_janela.geometry("300x220")

    texto = tk.Text(resultado_janela, font=("Arial", 16))
    texto.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    for chave, valor in resultados.items():
        texto.insert(tk.END, f"{chave}: {valor}\n")

def calculatorStart(bonus):
    def calcular():
        try:
            forca_val = int(entry_forca.get())
            chakra_val = int(entry_chakra.get())
            destreza_val = int(entry_destreza.get())

            dados = {
                'forca': forca_val,
                'chakra': chakra_val,
                'destreza': destreza_val
            }

            resultado = calculateStatus(dados, bonus)
            showResult(resultado)
        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números inteiros válidos.")

    # Criar nova janela de cálculo
    janela = tk.Tk()
    janela.title("Calculadora de Status Ninja")
    janela.geometry("300x220")

    tk.Label(janela, text="Força:").pack()
    entry_forca = tk.Entry(janela)
    entry_forca.pack()

    tk.Label(janela, text="Chakra:").pack()
    entry_chakra = tk.Entry(janela)
    entry_chakra.pack()

    tk.Label(janela, text="Destreza:").pack()
    entry_destreza = tk.Entry(janela)
    entry_destreza.pack()

    tk.Button(janela, text="Calcular Status", command=calcular).pack(pady=16)
    janela.mainloop()

def selectClan():
    def selecionar(nome_cla):
        bonus = clan_bonuses[nome_cla]
        janela_cla.destroy()
        calculatorStart(bonus)

    janela_cla = tk.Tk()
    janela_cla.title("Escolha seu Clã")
    janela_cla.geometry("400x600")

    tk.Label(janela_cla, text="Selecione seu clã ninja:", font=("Arial", 14)).pack(pady=10)

    quadro = tk.Frame(janela_cla)
    quadro.pack(fill=tk.BOTH, expand=True)

    for nome in sorted(clan_bonuses.keys()):
        tk.Button(quadro, text=nome, width=20, command=lambda n=nome: selecionar(n)).pack(pady=2)

    janela_cla.mainloop()

# Iniciar com a escolha de clã
selectClan()
