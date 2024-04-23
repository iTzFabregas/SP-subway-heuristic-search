import { useState } from "react"
import axios from 'axios'
import "./assets/tailwind.css"

function App() {

    const [origin, setOrigin] = useState()
    const [destination, setDestination] = useState()
    const [option, setOption] = useState()

    const [response, setResponse] = useState()

    const handleClick = () => {
        console.log(origin)
        console.log(destination)
        console.log(option)

        const searchBaseURL = `http://127.0.0.1:5000/${option}?s1=${origin}&s2=${destination}`
        axios
            .get(searchBaseURL)
            .then((res) => {
                console.log(res, "Response fetched in app")
                setResponse(res)
            })
            .catch((error) => {
                console.log("Erro fetch full criterio: " + error);
            })

    }

    return (
        <div className="flex flex-col items-center">
            <nav className="flex flex-col bg-01 bg-center w-full h-72 items-center justify-center mb-12 shadow-2xl">
                <h1 className="text-black font-bold font-mono text-9xl bg-opacity-60 bg-gray-100">Qual caminho percorrer?</h1>
            </nav>

            <div className="flex flex-col bg-gray-200 rounded-3xl shadow-2xl w-1/2 h-96 items-center justify-center mb-12">
                <h3>Estação de Origem</h3>
                <input type="text" className="bg-gray-400 mb-5" onChange={(e) => setOrigin(e.target.value)} />

                <h3>Estação de Destino</h3>
                <input type="text" className="bg-gray-400 mb-5" onChange={(e) => setDestination(e.target.value)} />

                <h3>Selecione o tipo de viagem</h3>
                <select defaultValue={"g0"} className="bg-gray-400 p-1 mb-8">
                    <option value="g0" onClick={(e) => setOption(e.target.value)} disabled>Selecione a viagem</option>
                    <option value="g1" onClick={(e) => setOption(e.target.value)} >Viagem com menor duração</option>
                    <option value="g2" onClick={(e) => setOption(e.target.value)} >Viagem com menor caminho percorrido</option>
                    <option value="g3" onClick={(e) => setOption(e.target.value)} >Viagem com maior média das avaliações</option>
                    <option value="g4" onClick={(e) => setOption(e.target.value)} >Viagem com maior número de estações percorridas</option>
                </select>
                <button className="bg-blue-500 p-2 rounded-2xl transform hover:scale-110 transition duration-300" onClick={handleClick}>Encontrar viagem!</button>
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
