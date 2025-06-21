import React from 'react'

const ProductSpecifications = ({mainSpecifications, variantSpecifications}) => {
    return (
        <div className="mt-12">
            <h3 className="text-3xl font-semibold text-gray-800">Parametry</h3>
            <table className="w-full mt-8 border-2 border-gray-300 rounded shadow table-fixed">
                <colgroup>
                    <col className="w-2/5" />  {/* Parametr */}
                    <col className="w-3/5 min-w-[200px]" />  {/* Wartość */}
                </colgroup>
                <thead>
                    <tr className="bg-gray-100 text-gray-700 border-b-2 border-gray-300">
                        <th className="py-2 px-4 text-left font-semibold text-xl">Parametr</th>
                        <th className="py-2 px-4 text-left font-semibold text-xl">Wartość</th>
                    </tr>
                </thead>
                <tbody>
                    {mainSpecifications && mainSpecifications.map(spec => (
                        <tr key={`main-${spec.id}`} className="even:bg-gray-200 hover:bg-gray-50 transition-colors text-lg font-light text-gray-900">
                            <td className="py-4 px-4">{spec.name}</td>
                            <td className="py-4 px-4 whitespace-nowrap">{spec.value}</td>
                        </tr>
                    ))}
                    {variantSpecifications && variantSpecifications.map(spec => (
                        <tr key={`variant-${spec.id}`} className="even:bg-gray-200 hover:bg-gray-50 transition-colors text-lg font-light text-gray-900">
                            <td className="py-4 px-4">{spec.name}</td>
                            <td className="py-4 px-4 whitespace-nowrap">{spec.value}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default ProductSpecifications