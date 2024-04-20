from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Tem nada aqui não!'

# como vai ser as rotas? cada rota se refere a uma opção do seletor?

if __name__ == '__main__':
    app.run(debug=True)
