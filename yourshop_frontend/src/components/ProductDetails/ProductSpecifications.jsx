import React from 'react'

const ProductSpecifications = ({mainSpecifications, variantSpecifications}) => {
    return (
        <div className="w-full rounded-sm bg-gray-200 shadow-lg p-6 mx-auto flex flex-col gap-6 mt-10">
            <h3 className="text-3xl font-bold text-gray-900">Parametry</h3>
            <table className="w-full rounded shadow table-fixed">
                <colgroup>
                    <col className="w-2/5" />
                    <col className="w-3/5 min-w-[200px]" />
                </colgroup>
                <tbody>
                    {mainSpecifications && mainSpecifications.map(spec => (
                        <tr key={`main-${spec.id}`} className="even:bg-gray-300 hover:bg-gray-50 transition-colors text-lg font-light text-gray-900">
                            <td className="py-4 px-4 font-medium text-gray-800">{spec.name}</td>
                            <td className="py-4 px-4 whitespace-nowrap">{spec.value}</td>
                        </tr>
                    ))}
                    {variantSpecifications && variantSpecifications.map(spec => (
                        <tr key={`variant-${spec.id}`} className="even:bg-gray-300 hover:bg-gray-50 transition-colors text-lg font-light text-gray-900">
                            <td className="py-4 px-4 font-medium text-gray-800">{spec.name}</td>
                            <td className="py-4 px-4 whitespace-nowrap">{spec.value}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}

export default ProductSpecifications