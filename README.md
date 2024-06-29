# Desafio-Morada-IA

Documentação código teste Morada AI:
Interface de Saque com Flask e Tkinter

Descrição Geral
Este projeto consiste em uma aplicação que permite aos usuários realizar saques monetários através de uma interface gráfica desenvolvida com Tkinter, enquanto um servidor Flask processa as requisições de saque. A aplicação calcula a quantidade mínima de cédulas necessárias para um determinado valor de saque e mantém um registro de todas as tentativas de saque em um arquivo JSON.

Estrutura do Código
O código está dividido em duas principais partes:
1.	Servidor Flask: Responsável por processar a lógica de saque e calcular a quantidade de cédulas.
2.	Interface Tkinter: Interface gráfica para o usuário interagir e solicitar saques.
Dependências
•	Flask – Necessário instalação via pip install flask
•	Requests – Necessário instalação via pip install Requests
•	Tkinter - Necessário instalação via pip install Tkinter
•	Json – Biblioteca padrão 
•	Threading – Biblioteca padrão

Código
Configuração do Servidor Flask
A primeira parte do código configura um servidor Flask que processa requisições de saque.
 
                                                            "from flask import Flask, request, jsonify
                                                            # Configuração do Flask
                                                            app = Flask(__name__)
                                                            
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
                                                                    return jsonify({"Não é possível sacar o valor com as cédulas disponíveis. Por favor, insira outro valor"}), 400
                                                            
                                                                return jsonify(resultado)
                                                            
                                                            def run_flask():
                                                                app.run(port=5000) "

Funções de Interface e Controle
Estas funções permitem a comunicação entre a interface Tkinter e o servidor Flask.
 
                                                                "import threading
                                                                import tkinter as tk
                                                                from tkinter import ttk
                                                                import requests
                                                                import json
                                                                from flask import Flask, request, jsonify
                                                                
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
                                                                        result_label.config(text=f"Erro ao conectar ao servidor: {e}") "


Interface Gráfica Tkinter
A última parte do código define a interface gráfica, configurando o layout e os componentes de interação.
 
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


Execução do Código
Para executar a aplicação esta aplicação, recomenda-se, primeiro, a criação de um ambiente virtual, para maior segurança e afim de evitar possíveis conflitos com versões de bibliotecas. Abra sua IDE de escolha e em seguida a pasta onde contém o arquivo .py e o arquivo JSON e execute o comando abaixo no terminal de seu IDE
                                                                   
                                                                   python -m venv “o nome de sua escola”

Após a etapa simplesmente execute o scritp com o nome de api.py e interface e servidor funcionaram, cada uma em uma thread separada. Com a interface na thread principal. Ao fazer as requisições de saque, o output do resultado irá para o arquivo json registrando a quantidade mínima de cédulas para a operação, bem como possíveis tentativas mal sucedidas de forma linear vertical: ou seja, o último registro no arquivo json é a tentativa mais recente de saque.

                                                                                        ##


Comentários sobre desafio:

Saudações time Morada IA! Desde já agradeço demais ser considerado para a vaga e por ter chegado até aqui. Peço desculpas pela demora em devolver o desafio. Agora respondendo sobre a principal dificuldade nesse projeto: com certeza foi decidir em manter a lógica de cálculo das cédulas junto ou não com as requisições HTTPS. Embora eu tenha certeza que separar as duas seja melhor para manipular, dessa vez eu optei por condensar-lás e deixar ambar em um lugar para maior legibilidade e tracking do que eu estava pensando. A interface, extremamente simplista, foi somente para facilitar o input do saque, tendo valor nulo estético nesse projeto. No mais, desejo boa sorte e se não for dessa vez, até a próxima. 


