from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Tem nada aqui não!'

@app.route('/g1')
# Viagem com menor duração
def graph1():
    # o ideial é retornar:
        # a lista com as estações do caminho
        # o numero de esações que tem no caminho
        # o place-id das estações
        # a duração total
    return(request.args)

@app.route('/g2')
# Viagem com menor caminho percorrido
def graph2():
    # o ideial é retornar:
        # a lista com as estações do caminho
        # o numero de esações que tem no caminho
        # o place-id das estações
        # a distancial total
    return(request.args)

@app.route('/g3')
# Viagem com maior média das avaliações
def graph3():
    # o ideial é retornar:
        # a lista com as estações do caminho
        # o numero de esações que tem no caminho
        # o place-id das estações
        # a avaliação media final
    return(request.args)

@app.route('/g4')
# Viagem com maior número de estações percorridas
def graph4():
    # o ideial é retornar:
        # a lista com as estações do caminho
        # o numero de esações que tem no caminho
        # o place-id das estações
        # o numero maz de estações obtido
    return(request.args)


if __name__ == '__main__':
    app.run(debug=True)
