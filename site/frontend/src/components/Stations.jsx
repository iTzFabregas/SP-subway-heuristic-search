import React from "react";

import "../assets/tailwind.css"

export default function Stations(info) {
    const { stations } = info

    return (
        <div className="grid grid-cols-2 gap-4 mb-10 px-16 pb-32 w-3/4 bg-neutral-100 rounded-3xl shadow-2xl">
            {stations.map((station) => {
                return (
                    <div className="flex flex-col gap-4 border border-black bg-gray-300 mx-10 mt-20 w-3/4 p-3 transform hover:scale-105 transition duration-300">
                        <h1>Nome da estação 1</h1>
                        <h2>{station}</h2>
                        <h2>Endereço da estação</h2>
                        <h3>Nota</h3>
                    </div>
                )
            })} 
        </div>
    )
}
