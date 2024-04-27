import React, { useEffect, useState } from "react";

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

    const definirCor2 = (station) => {
        if (station['result']['website']) {
            return 'bg-blue-200';
        }
        return 'bg-red-200';
    }

    return (
        <div className="grid grid-cols-1 gap-4 mb-10 px-16 pb-32 w-3/4 bg-neutral-100 rounded-3xl shadow-2xl">
            {stations.map((station) => {
                return (    
                    <a href={station['result']['website']} target="_blank" rel="noopener noreferrer">
                        <div className={`flex flex-col xl:flex-row gap-4 border border-black bg-gray-200 mx-10 mt-20 w-3/4 p-3 transform hover:shadow-2xl hover:${definirCor2(station)} transition duration-300`}>
                            <div>
                                <img src={`https://maps.googleapis.com/maps/api/place/photo?maxheight=288&photo_reference=${station['result']['photos'][0]['photo_reference']}&key=AIzaSyA_prM8fOfjOLNI_pDa0w1IO0L5ePMMaaU`}></img>
                            </div>
                            <div className="flex flex-col justify-between">
                                <h1 className="font-bold text-md">{'Estação: ' + station['result']['name']}</h1>
                                <h3 className="text-sm">{station['result']['formatted_address']}</h3>
                                <h2 className={`text-lg ${definirCor1(station)}`}>{station['result']['rating'] + '★ de ' + station['result']['user_ratings_total'] + ' reviews'}</h2>
                                {station['result']['wheelchair_accessible_entrance'] && <h3 className="border border-green-600 bg-green-300 w-fit p-1 text-green-600 font-bold">Acesso para cadeirantes</h3>}
                                {!station['result']['wheelchair_accessible_entrance'] && <h3 className="border border-red-600 bg-red-300 w-fit p-1 text-red-600 font-bold">Sem acesso para cadeirantes</h3>}
                            </div>
                        </div>
                    </a>
                )
            })}
        </div>
    )
}
