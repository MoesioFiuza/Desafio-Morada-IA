import threading
import tkinter as tk
from tkinter import ttk
import requests
import json
import os
from flask import Flask, request, jsonify

# Configuração do Flask
app = Flask(__name__)

# Criar o arquivo JSON vazio se não existir
if not os.path.exists('tentativas_saque.json'):
    with open('tentativas_saque.json', 'w') as f:
        json.dump([], f)

@app.route('/api/saque', methods=['POST'])
def realizar_saque():
    data = request.get_json()
    valor = data.get('valor')
    
    if valor is None or not isinstance(valor, int) or valor <= 0:
        return jsonify({"erro": "Valor inválido. Insira um número inteiro positivo."}), 400

    # Lógica para calcular a quantidade mínima de cédulas
    cedulas = [100, 50, 20, 10, 5, 2]
    resultado = {}
    for cedula in cedulas:
        resultado[str(cedula)], valor = divmod(valor, cedula)
    
    if valor > 0:
        return jsonify({"erro": "Não é possível sacar o valor com as cédulas disponíveis. Por favor, insira outro valor"}), 400

    return jsonify(resultado)

def run_flask():
    app.run(port=5000)

def realizar_saque_interface(valor_entry, result_label):
    try:
        valor = int(valor_entry.get())
        response = requests.post('http://localhost:5000/api/saque', json={"valor": valor})
        response_data = response.json()
        
        if response.status_code == 200:
            result_label.config(text="Saque realizado com sucesso!")
        else:
            result_label.config(text=f"Erro: {response_data['erro']}")

        # Carregar tentativas anteriores do arquivo JSON
        try:
            with open('tentativas_saque.json', 'r') as f:
                tentativas = json.load(f)
        except FileNotFoundError:
            tentativas = []

        # Adicionar nova tentativa
        tentativa = {"valor": valor, "resultado": response_data}
        tentativas.append(tentativa)

        # Salvar todas as tentativas de volta no arquivo JSON
        with open('tentativas_saque.json', 'w') as f:
            json.dump(tentativas, f, indent=4)

    except ValueError:
        result_label.config(text="Por favor, insira um valor numérico válido.")
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Erro ao conectar ao servidor: {e}")

def show_main_app(root):
    # Configurar estilos
    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), foreground='black', background='#ff6600')
    style.configure('TLabel', font=('Helvetica', 12), foreground='black')
    style.configure('TEntry', font=('Helvetica', 12))

    # Configurar layout
    root.configure(bg='white')
    root.geometry("400x300")
    
    title_label = tk.Label(root, text="Interface de Saque", font=('Helvetica', 24, 'bold'), fg='black', bg='white')
    title_label.pack(pady=20)

    frame = tk.Frame(root, bg='white')
    frame.pack(pady=10)

    valor_label = ttk.Label(frame, text="Valor do Saque:", background='white')
    valor_label.grid(row=0, column=0, padx=10, pady=10)

    valor_entry = ttk.Entry(frame)
    valor_entry.grid(row=0, column=1, padx=10, pady=10)

    # Exibir cédulas disponíveis
    cedulas_label = tk.Label(root, text="Cédulas disponíveis: 100, 50, 20, 10, 5, 2", font=('Helvetica', 12), fg='black', bg='white')
    cedulas_label.pack(pady=10)

    result_label = tk.Label(root, text="", font=('Helvetica', 12), fg='black', bg='white')
    result_label.pack(pady=10)

    btn_saque = ttk.Button(root, text="Realizar Saque", command=lambda: realizar_saque_interface(valor_entry, result_label))
    btn_saque.pack(pady=10)

def run_tkinter():
    root = tk.Tk()
    root.title("Interface de Saque")

    # Mostrar a aplicação principal
    show_main_app(root)

    root.mainloop()

if __name__ == '__main__':
    # Iniciar o servidor Flask em uma nova thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Executar Tkinter na thread principal
    run_tkinter()
