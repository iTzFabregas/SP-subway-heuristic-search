import { useState } from "react"
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid';

import "./assets/tailwind.css"

import Stations from './components/Stations'
import Autocomplete from "./components/Autocomplete";

function App() {

    const [origin, setOrigin] = useState('')
    const [destination, setDestination] = useState('')
    const [option, setOption] = useState()

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

    const handleInput1 = (value) => {
        setOrigin(value)
    }
    const handleInput2 = (value) => {
        setDestination(value)
    }

    return (
        <div className="flex flex-col items-center">
            <nav className="flex flex-col bg-01 bg-center w-full h-72 items-center justify-center mb-12 shadow-2xl text-center">
                <h1 className="text-black font-bold font-mono text-9xl bg-opacity-60 bg-gray-100">Qual caminho percorrer?</h1>
            </nav>

            <div className="flex flex-col bg-gray-200 rounded-3xl shadow-2xl w-1/2 h-96 items-center justify-center mb-12">
                <h3>Estação de Origem</h3>
                <input type="text" className="bg-white mb-5" onChange={(e) => setOrigin(e.target.value)} />
                {/* <Autocomplete handleInput={handleInput1} key={uuidv4()} /> */}

                <h3>Estação de Destino</h3>
                <input type="text" className="bg-white mb-5" onChange={(e) => setDestination(e.target.value)} />
                {/* <Autocomplete handleInput={handleInput2} key={uuidv4()} /> */}

                <h3>Selecione o tipo de viagem</h3>
                <select defaultValue={"g0"} className="bg-white p-1 mb-8">
                    <option value="g0" onClick={(e) => setOption(e.target.value)} disabled>Selecione a viagem</option>
                    <option value="g1" onClick={(e) => setOption(e.target.value)} >Viagem com menor duração</option>
                    <option value="g2" onClick={(e) => setOption(e.target.value)} >Viagem com menor caminho percorrido</option>
                    <option value="g3" onClick={(e) => setOption(e.target.value)} >Viagem com maior média das avaliações</option>
                    <option value="g4" onClick={(e) => setOption(e.target.value)} >Viagem com maior número de estações percorridas</option>
                </select>
                <button className="bg-blue-500 p-2 rounded-2xl transform hover:scale-110 transition duration-300 disabled:bg-blue-300 disabled:text-blue-500" onClick={handleClick} disabled={status === 'loading'}>Encontrar viagem!</button>
            </div>

            {status !== 'idle' && <div className="flex flex-col mb-8 p-10 w-3/4 h-fit bg-neutral-100 rounded-3xl shadow-xl items-center justify-center">
                {status === 'loading' && <p>LOADING...</p>}
                {status === 'error' && <p>ERROR...</p>}

                {status === 'ready' && <h3>{response[0]}</h3>}
                {status === 'ready' && <h3>{response[1]}</h3>}
            </div>}

            {status === 'ready' && <Stations stations={response[2][1]} key={uuidv4()} />}
        </div>
    )
}

export default App
