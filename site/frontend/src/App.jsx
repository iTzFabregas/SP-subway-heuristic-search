import "./assets/tailwind.css"

function App() {

    return (
        <div className="flex flex-col items-center">
            <nav className="flex flex-col bg-gray-400 w-full h-72 items-center justify-center mb-8">
                <h1 className="text-blue-700 text-9xl">Qual caminho percorrer???</h1>
            </nav>

            <div className="flex flex-col bg-red-500 w-1/2 h-96 items-center justify-center mb-8">
                <h3>Estação de Origem</h3>
                <input type="text" className="bg-gray-200 " />

                <h3>Estação de Destino</h3>
                <input type="text" className="bg-gray-200 " />

                <h3>Selecione o tipo de viagem</h3>
                <select name="" id="">
                    <option value="">Selecione a viagem</option>
                    <option value="">Viagem com menor duração</option>
                    <option value="">Viagem com menor caminho percorrido</option>
                    <option value="">Viagem com maior média das avaliações</option>
                    <option value="">Viagem com maior número de estações percorridas</option>
                </select>
                <button className="bg-blue-500 p-1 rounded-2xl">Encontrar viagem!</button>
            </div>

            <div className="flex flex-col bg-green-500 w-3/4 h-96 items-center justify-center">

            </div>
        </div>
    )
}

export default App
