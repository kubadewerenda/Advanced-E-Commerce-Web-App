import React from 'react'
import { BASE_URL } from '../../api/api'
import { Link } from 'react-router-dom'

const ProductCard = ({product}) => {
    const moreVariantsPrice = product.variants.length > 1 ? "od" : ""
    return (
        <div className="relative bg-gray-200 rounded-xl shadow-md flex transition hover:scale-105 hover:shadow-xl duration-200 min-w-[340px] min-h-[180px] max-w-full p-2 gap-2">
            <Link to={`/products/${product.slug}`}>
                {product.num_of_promotions > 0 && 
                    <div className="absolute left-1/2 top-0 -translate-x-1/2 w-fit rounded-b-2xl p-2 bg-orange-600 shadow-lg">
                        <span className="block text-sm font-light text-white">Promocje: {product.num_of_promotions}!</span>
                    </div>
                }
                <div className="flex flex-col items-center justify-center">
                    <img
                    src={
                    product?.images?.[0]?.image
                        ? BASE_URL + product.images[0].image
                        : "https://via.placeholder.com/400x300?text=No+Image"
                    }
                    alt={product?.images?.[0]?.alt_text || product?.name}
                    className="w-40 h-40 object-fit"
                    />
                </div>
                <div className="flex-1 flex flex-col min-w-0">
                    <h3 className="font-bold text-lg mb-2 text-gray-800 break-words">{product?.name}</h3>
                    <p className="text-gray-400 text-sm flex-1">{product?.category}</p>
                    <p className="text-gray-600 text-sm break-words h-full mt-2">{product?.description.slice(0,100) + "..."}</p>
                    <div className="mt-3 flex items-end justify-between">
                        <span className="text-lg text-gray-600 font-medium">{moreVariantsPrice} <span className="text-lg text-gray-700 font-bold">{product.main_variant.price} zł</span>/szt</span>
                    </div>
                </div>
            </Link>
        </div>
    )
}
export default ProductCard
