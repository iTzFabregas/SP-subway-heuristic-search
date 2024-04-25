import React, { useEffect, useState, useRef } from 'react';

export default function Autocomplete(info) {
    const {input, handleInput} = info
    const [filteredOptions, setFilteredOptions] = useState([]);
    const [options, setOptions] = useState(stations)
    const [showOptions, setShowOptions] = useState(false)
    const inputRef = useRef(null);

    useEffect (() => {
        const filteredOptions = options.filter(
            (option) =>
                option.toLowerCase().indexOf(input.toLowerCase()) > -1
        );
        setFilteredOptions(filteredOptions);
        inputRef.current.focus();
    }, [input])

    const handleOptionClick = (option) => {
        setFilteredOptions([]); 
        inputRef.current.focus();
        handleInput(option);
    };

    return (
        <div className="relative">
            <input
                type="text"
                defaultValue={input}
                value={input}
                onChange={(e) => handleInput(e.target.value)}
                ref={inputRef}
                className="border border-gray-300 rounded-md p-2 w-64"
                onFocus={() => setShowOptions(true)}
                onBlur={() => setShowOptions(false)}
            />
            {showOptions && filteredOptions.length > 0 && (
                <ul className="absolute z-10 bg-white border border-gray-300 rounded-md mt-1 w-64">
                    {filteredOptions.map((option, index) => (
                        <li
                            key={index}
                            onClick={() => handleOptionClick(option)}
                            className="px-3 py-2 cursor-pointer hover:bg-gray-100"
                        >
                            {option}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}


const stations = [
    'Estacao Jabaquara',
    'Estacao Conceicao',
    'Estacao Sao Judas',
    'Estacao Saude',
    'Estacao Praca da arvore',
    'Estacao Santa Cruz',
    'Estacao Vila Mariana',
    'Estacao Paraiso',
    'Estacao Vergueiro',
    'Estacao Sao Joaquim',
    'Estacao Japao-Liberdade',
    'Estacao Se',
    'Estacao Sao Bento',
    'Estacao Luz',
    'Estacao Armenia',
    'Estacao Portuguesa-Tiete',
    'Estacao Carandiru',
    'Estacao Santana',
    'Estacao Jardim Sao Paulo-Ayrton Senna',
    'Estacao Parada Inglesa',
    'Estacao Tucuruvi',
    'Estacao Vila Prudente',
    'Estacao Tamanduatei',
    'Estacao Sacoma',
    'Estacao Alto do Ipiranga',
    'Estacao Santos-Imigrantes',
    'Estacao Chacara Klabin',
    'Estacao Ana Rosa',
    'Estacao Brigadeiro',
    'Estacao Trianon-Masp',
    'Estacao Consolacao',
    'Estacao Clinicas',
    'Estacao S. N. Sra. de Fatima-Sumare',
    'Estacao Vila Madalena',
    'Estacao Corinthians-Itaquera',
    'Estacao Artur Alvim',
    'Estacao Patriarca-Vila Re',
    'Estacao Guilhermina-Esperanca',
    'Estacao Vila Matilde',
    'Estacao Penha',
    'Estacao Carrao-Assai Atacadista',
    'Estacao Tatuape',
    'Estacao Belem',
    'Estacao Bresser-Mooca',
    'Estacao Bras',
    'Estacao Pedro II',
    'Estacao Anhangabau',
    'Estacao Republica',
    'Estacao Santa Cecilia',
    'Estacao Marechal Deodoro',
    'Estacao Palmeiras-Barra Funda',
    'Estacao Vila Sonia Profa. Elisabeth Tenreiro',
    'Estacao Sao Paulo-Morumbi',
    'Estacao Butanta',
    'Estacao Pinheiros',
    'Estacao Faria Lima',
    'Estacao Fradique Coutinho',
    'Estacao Oscar Freire',
    'Estacao Paulista Pernambucanas',
    'Estacao Higienopolis-Mackenzie',
    'Estacao Capao Redondo',
    'Estacao Campo Limpo',
    'Estacao Vila das Belezas',
    'Estacao Giovanni Gronchi',
    'Estacao Santo Amaro',
    'Estacao Largo Treze',
    'Estacao Adolfo Pinheiro',
    'Estacao Alto da Boa Vista',
    'Estacao Borba Gato',
    'Estacao Brooklin',
    'Estacao Campo Belo',
    'Estacao Eucaliptos',
    'Estacao Moema',
    'Estacao AACD-Servidor',
    'Estacao Hospital Sao Paulo',
    'Estacao Santa Cruz',
    'Estacao Chacara Klabin',
    'Estacao Oratorio',
    'Estacao Sao Lucas',
    'Estacao Camilo Haddad',
    'Estacao Vila Tolstoi',
    'Estacao Vila Uniao',
    'Estacao Jd. Planalto',
    'Estacao Sapopemba',
    'Estacao Fazenda da Juta',
    'Estacao Sao Mateus'
];