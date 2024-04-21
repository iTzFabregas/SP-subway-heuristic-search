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
            <nav className="flex flex-col bg-gray-400 w-full h-72 items-center justify-center mb-8">
                <h1 className="text-blue-700 text-9xl">Qual caminho percorrer?</h1>
            </nav>

            <div className="flex flex-col bg-red-500 w-1/2 h-96 items-center justify-center mb-8">
                <h3>Estação de Origem</h3>
                <input type="text" className="bg-gray-200" onChange={handleOrigin}/>

                <h3>Estação de Destino</h3>
                <input type="text" className="bg-gray-200" onChange={handleDestination}/>

                <h3>Selecione o tipo de viagem</h3>
                <select defaultValue={"00"}>
                    <option value="00" onClick={handleOption} disabled>Selecione a viagem</option>
                    <option value="01" onClick={handleOption} >Viagem com menor duração</option>
                    <option value="02" onClick={handleOption} >Viagem com menor caminho percorrido</option>
                    <option value="03" onClick={handleOption} >Viagem com maior média das avaliações</option>
                    <option value="04" onClick={handleOption} >Viagem com maior número de estações percorridas</option>
                </select>
                <button className="bg-blue-500 p-1 rounded-2xl" onClick={handleClick}>Encontrar viagem!</button>
            </div>

            <div className="flex flex-col bg-green-500 w-3/4 h-96 items-center justify-center">

            </div>
        </div>
    )
}

export default App
