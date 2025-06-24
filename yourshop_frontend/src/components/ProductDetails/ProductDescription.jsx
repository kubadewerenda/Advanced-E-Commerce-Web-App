import React from 'react'

const ProductDescription = ({description}) => {
    return (
        <section id="section" className="w-full rounded-sm bg-gray-200 shadow-lg mx-auto flex flex-col gap-6 mt-10 p-6">
            <h3 className="text-3xl font-bold text-gray-900">Opis</h3>
            <p className="text-xl font-semibold text-gray-800">{description}</p>            
        </section>
    )
}

export default ProductDescription