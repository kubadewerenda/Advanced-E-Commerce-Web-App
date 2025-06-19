import React, { useEffect, useState } from 'react'
import api, { BASE_URL } from '../api/api'
import { Link, useParams } from 'react-router-dom'
import RelatedProducts from '../components/ProductDetails/RelatedProducts'

const ProductDetails = () => {
    const [product, setProduct] = useState({})
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")

    const [currentImg, setCurrentImg] = useState(0)

    const {slug} = useParams();

    useEffect(() => {
        setLoading(true)
        api.get(`api/products/${slug}`)
        .then(res => {
            console.log(res.data)
            setProduct(res.data)
            setCurrentImg(0)
            window.scrollTo({top: 0, behavior: "smooth"})
        })
        .catch(err => {
            console.log(err.message)
            setError(err.message)
        })
        .finally(() => setLoading(false))
    }, [slug])

    if(loading){
        return (
            <div className="flex justify-center items-center text-center">
                Ładowanie...
            </div>
        )
    }


    return (
        <div className="max-w-screen-5xl mx-auto">
            <Link to="/shop" className="text-center" >Powrót do sklepu</Link>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-30 mt-10">
                <div className="flex flex-col gap-5 w-full justify-center items-center">
                    <div className="w-[600px] h-[480px] flex items-center justify-center bg-white rounded-xl shadow-xl">
                        <img 
                            src={
                                product?.images?.[currentImg]?.image
                                ? BASE_URL + product.images[currentImg].image
                                : "https://via.placeholder.com/400x300?text=No+Image"
                            }
                            alt={product?.images?.[currentImg]?.alt_text || product?.name}
                            className="object-contain w-full h-full rounded-x"
                        />
                    </div>
                    <div className="flex flex-wrap gap-2 mt-4 overflow-x-auto w-full px-2">
                        {product?.images?.length > 0 && (
                            product.images.map((img, i) => (
                                <button
                                    key={img.id}
                                    onClick={() => setCurrentImg(i)}
                                    className={`w-48 h-32 rounded-md border overflow-hidden ${currentImg === i ? 'border-gray-400' : 'border-gray-300'}`}
                                >
                                    <img src={BASE_URL + img.image} alt={img.alt_text} className="w-full h-full object-contain" />                                
                                </button>
                            ))
                        )}
                    </div>
                </div>
                <div className="flex flex-col gap-y-2 w-full">
                    <h1 className="text-3xl text-gray-950 font-medium">{product.name}</h1>
                    <hr />
                    <span className="text-sm text-gray-600 font-light">{`Kod produktu: ${product.sku}`}</span>    
                    <p className="text-lg font-semibold">{`${product.price} zł/szt`}</p>                
                </div>
            </div>  
            <RelatedProducts products={product.related_products}/>        
        </div>
    )
}

export default ProductDetails