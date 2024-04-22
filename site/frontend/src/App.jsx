import { useState } from "react"
import "./assets/tailwind.css"

function App() {

    const [origin, setOrigin] = useState()
    const [destination, setDestination] = useState()
    const [option, setOption] = useState()

    const handleOrigin = (e) => {
        setOrigin(e.target.value)
        // verificar se é uma estação valida
    }

    const handleDestination = (e) => {
        setDestination(e.target.value)
        // verificar se é uma estação valida
    }

    const handleOption = (e) => {
        setOption(e.target.value)
    }

    const handleClick = () => {
        console.log(origin)
        console.log(destination)
        console.log(option)

        // ao clicar no botao, ver qual o opçao
        switch (option) {
            case "01":
                // A* no grafo de duração
                break;

            case "02":
                // A* no grafo de distancia
                break;

            case "03":
                // A* no grafo de avaliação
                break;

            case "04":
                // profundidade em algum grafo???
                break;

            default:
                //error
                break;
        }
    }

    return (
        <div className="flex flex-col items-center">
            <nav className="flex flex-col bg-01 bg-center w-full h-72 items-center justify-center mb-12 shadow-2xl">
                <h1 className="text-black font-bold font-mono text-9xl bg-opacity-60 bg-gray-100">Qual caminho percorrer?</h1>
            </nav>

            <div className="flex flex-col bg-gray-200 rounded-3xl shadow-2xl w-1/2 h-96 items-center justify-center mb-12">
                <h3>Estação de Origem</h3>
                <input type="text" className="bg-gray-400 mb-5" onChange={handleOrigin} />

                <h3>Estação de Destino</h3>
                <input type="text" className="bg-gray-400 mb-5" onChange={handleDestination} />

                <h3>Selecione o tipo de viagem</h3>
                <select defaultValue={"00"} className="bg-gray-400 p-1 mb-8">
                    <option value="00" onClick={handleOption} disabled>Selecione a viagem</option>
                    <option value="01" onClick={handleOption} >Viagem com menor duração</option>
                    <option value="02" onClick={handleOption} >Viagem com menor caminho percorrido</option>
                    <option value="03" onClick={handleOption} >Viagem com maior média das avaliações</option>
                    <option value="04" onClick={handleOption} >Viagem com maior número de estações percorridas</option>
                </select>
                <button className="bg-blue-500 p-1 rounded-2xl" onClick={handleClick}>Encontrar viagem!</button>
            </div>
            <div className="flex flex-col mb-8 p-10 w-3/4 h-16 bg-neutral-100 rounded-3xl shadow-xl items-center justify-center">
                <h2>{'Caminho encontrado -> XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}</h2>
            </div>
            <div className="grid grid-cols-2 gap-4 mb-10 px-16 pb-32 w-3/4 bg-neutral-100 rounded-3xl shadow-2xl">
                <div className="flex flex-col gap-4 border border-black bg-gray-300 mx-10 mt-20 w-3/4 p-3 transform hover:scale-105 transition duration-300">
                    <h1>Nome da estação 1</h1>
                    <h2>Endereço da estação</h2>
                    <h3>Nota</h3>
                </div>
                <div className="flex flex-col gap-4 border border-black bg-gray-300 mx-10 mt-20 w-3/4 p-3 transform hover:scale-105 transition duration-300">
                    <h1>Nome da estação 1</h1>
                    <h2>Endereço da estação</h2>
                    <h3>Nota</h3>
                </div>
                <div className="flex flex-col gap-4 border border-black bg-gray-300 mx-10 mt-20 w-3/4 p-3 transform hover:scale-105 transition duration-300">
                    <h1>Nome da estação 1</h1>
                    <h2>Endereço da estação</h2>
                    <h3>Nota</h3>
                </div>
                <div className="flex flex-col gap-4 border border-black bg-gray-300 mx-10 mt-20 w-3/4 p-3 transform hover:scale-105 transition duration-300">
                    <h1>Nome da estação 1</h1>
                    <h2>Endereço da estação</h2>
                    <h3>Nota</h3>
                </div>
                <div className="flex flex-col gap-4 border border-black bg-gray-300 mx-10 mt-20 w-3/4 p-3 transform hover:scale-105 transition duration-300">
                    <h1>Nome da estação 1</h1>
                    <h2>Endereço da estação</h2>
                    <h3>Nota</h3>
                </div>
                <div className="flex flex-col gap-4 border border-black bg-gray-300 mx-10 mt-20 w-3/4 p-3 transform hover:scale-105 transition duration-300">
                    <h1>Nome da estação 1</h1>
                    <h2>Endereço da estação</h2>
                    <h3>Nota</h3>
                </div>
            </div>
        </div>
    )
}

export default App
