import React from 'react'
import ProductCard from './ProductCard'
import PlaceHolder from './PlaceHolder/PlaceHolder'

const ProductContainer = ({products, loading}) => {
    const placeNumbers = [...Array(12).keys()].slice(0)
    return (
        <section className="py-10">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-6 mt-5">
                {loading 
                    ? placeNumbers.map(num => <PlaceHolder key={num} />)
                    : products.map(product => <ProductCard key={product.id} product={product} />)
                }
            </div>
        </section>        
    )
}

export default ProductContainer