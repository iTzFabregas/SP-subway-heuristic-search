import "../assets/tailwind.css"

export default function Stations(info) {
    const { stations } = info
    const definirCor1 = (station) => {
        if (station['result']['rating'] < 4.0) {
            return 'text-red-600';
        }
        if (station['result']['rating'] < 4.5) {
            return 'text-yellow-500';
        }
        return 'text-green-600';
    }

    return (
        <div className="flex flex-col items-center justify-center gap-4 mb-10 px-16 pb-32 w-11/12 bg-neutral-100 rounded-1xl shadow-2xl">
        <h1 className="text-4xl font-bold mt-12 z-10 text-center underline decoration-sky-500">
            Navegue pelas estações ideais 
        </h1>
            
        {stations.map((station) => {
                return (
                    <div className="flex flex-col xl:flex-row gap-4 bg-gray-100 border-4 border-sky-500 rounded-sm shadow-lg mx-10 mt-20 w-3/4 p-3">
                        <div>
                            <img src={`https://maps.googleapis.com/maps/api/place/photo?maxheight=288&photo_reference=${station['result']['photos'][0]['photo_reference']}&key=AIzaSyA_prM8fOfjOLNI_pDa0w1IO0L5ePMMaaU`} className="me-5"></img>
                        </div>
                        <div className="flex flex-col justify-between">
                            <h1 className="font-bold text-lg text-sky-500">{'Estação: ' + station['result']['name']}</h1>
                            <h3 className="text-sm">{station['result']['formatted_address']}</h3>
                            <h2 className={`text-lg ${definirCor1(station)}`}>{station['result']['rating'] + '★ de ' + station['result']['user_ratings_total'] + ' reviews'}</h2>
                            {station['result']['wheelchair_accessible_entrance'] && <h3 className="border border-green-600 bg-green-300 w-fit p-1 text-green-600 font-bold">Acesso para cadeirantes</h3>}
                            {!station['result']['wheelchair_accessible_entrance'] && <h3 className="border border-red-600 bg-red-300 w-fit p-1 text-red-600 font-bold">Sem acesso para cadeirantes</h3>}
                            {station['result']['website'] && <a href={station['result']['website']} target="_blank" rel="noopener noreferrer" className="text-blue-600 transform hover:underline hover:cursor-pointer transition duration-300">Click here for more informations...</a>}
                        </div>
                    </div>
                )
            })}
        </div>
    )
}
