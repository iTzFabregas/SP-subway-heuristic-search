import { useState } from "react"
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid';

import "./assets/tailwind.css"

import Stations from './components/Stations'

function App() {

    const [origin, setOrigin] = useState('')
    const [destination, setDestination] = useState('')
    const [option, setOption] = useState() // 'g1', 'g2', 'g3', 'g4'

    const [status, setStatus] = useState('idle') // 'idle', 'loading', 'error', 'ready'
    const [response, setResponse] = useState([])

    const handleClick = () => {
        console.log(origin)
        console.log(destination)
        console.log(option)

        setStatus('loading')
        const searchBaseURL = `http://127.0.0.1:5000/${option}?s1=${origin}&s2=${destination}`
        axios
            .get(searchBaseURL)
            .then((res) => {
                console.log(res, "Response fetched in app")
                setResponse(res.data)
                setStatus('ready')
            })
            .catch((error) => {
                console.log("Erro fetch full criterio: " + error);
                setStatus('error')
            })
    }

    const handleOption = (e) => {
        setOption(e.target.value)
        setStatus('idle')
    }


    return (
        <div className="flex flex-col items-center bg-gradient-to-b from-blue-400 to-sky-400">
            <div className="flex flex-col items-center relative w-full h-screen">
                <div className="absolute inset-0 bg-03 bg-center bg-cover filter blur"></div>
                <div className="flex flex-col justify-center items-center h-full text-white text-center relative w-3/4">
                   <h1 className="text-6xl font-bold mb-4 relative z-10 underline decoration-sky-500">
                        Qual melhor caminho para sua necessidade?
                    </h1>
                    <p className="text-3xl relative z-10 w-3/4 mt-6">
                        Digite a estação de origem e estação de destino e selecione
                        o modo como deseja percorrer: menor tempo, menor distância,
                        melhores avaliações do Google ou caminho que passa por mais estações.
                    </p>
                    <div className="flex flex-col gap-5 items-center bg-gray-100 border-4 border-sky-500 rounded-sm shadow-lg w-102 p-8 my-12">
                        <div className="flex flex-row gap-10">
                            <div>
                                <h3 className="text-lg mb-2 font-bold text-sky-500">Estação de Origem</h3>
                                <input type="text" className="bg-white p-2 rounded-sm mb-4 border-4 border-sky-500 text-gray-500" onChange={(e) => setOrigin(e.target.value)} />
                            </div>
                            <div>
                                <h3 className="text-lg mb-2 font-bold text-sky-500">Estação de Destino</h3>
                                <input type="text" className="bg-white p-2 rounded-sm mb-4 border-4 border-sky-500 text-gray-500" onChange={(e) => setDestination(e.target.value)} />
                            </div>
                            <div>
                                <h3 className="text-lg mb-2 font-bold text-sky-500">Selecione o tipo de viagem</h3>
                                <select defaultValue={"g0"} className="bg-white p-2.5 rounded-sm border-4 border-sky-500 text-gray-500" onChange={handleOption}>
                                    <option value="g0" disabled>Selecione a viagem</option>
                                    <option value="g1">Viagem com menor duração</option>
                                    <option value="g2">Viagem com menor caminho percorrido</option>
                                    <option value="g3">Viagem com maior média das avaliações</option>
                                    <option value="g4">Viagem com maior número de estações percorridas</option>
                                </select>
                            </div>
                        </div>
                        <button className="bg-sky-500 p-2 w-3/5 rounded-sm hover:bg-blue-600 transition duration-300 text-white" onClick={handleClick} disabled={status === 'loading'}>Encontrar viagem!</button>
                    </div>
                </div>
                {status !== 'idle' &&
                    <div className="flex mb-8 gap-7">
                        <img class="z-10 w-24 animate-bounce" src="./blue-arrow.png" alt="Descrição da imagem" />
                    </div>}
            </div>

            {status !== 'idle' &&
                <div className="flex flex-col my-12 p-10 w-3/4 h-fit bg-neutral-100 rounded-1xl shadow-xl items-center justify-center">
                    {status === 'loading' && <p>LOADING...</p>}
                    {status === 'error' && <p>ERROR...</p>}

                    {status === 'ready' && <h3>{response[0]}</h3>}
                    {status === 'ready' &&
                        <div className="flex flex-row mt-5">
                            <h3>{response[1]}</h3>
                            <h3>&nbsp;&nbsp;</h3>
                            {option === 'g1' && <h3> minutos</h3>}
                            {option === 'g2' && <h3> kilometros</h3>}
                            {option === 'g3' && <h3> ★</h3>}
                            {option === 'g4' && <h3> estações</h3>}
                        </div>}
                </div>}

            {status === 'ready' && <Stations stations={response[2]} key={uuidv4()} />}
        </div>
    )
}

export default App
