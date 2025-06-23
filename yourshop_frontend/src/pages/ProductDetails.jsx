import React, { useEffect, useState } from 'react'
import api, { BASE_URL } from '../api/api'
import { Link, useParams } from 'react-router-dom'
import RelatedProducts from '../components/ProductDetails/RelatedProducts'
import ProductVariantsSelect from '../components/ProductDetails/ProductVariantsSelect'
import ProductSpecifications from '../components/ProductDetails/ProductSpecifications'
import CustomNumInput from '../components/ui/CustomInputs/CustomNumInput'
import ProductDescription from '../components/ProductDetails/ProductDescription'

const ProductDetails = () => {
    const [product, setProduct] = useState({})
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")

    const [selectedVariantIndex, setSelectedVariantIndex] = useState(0)

    const variants = product.variants || []
    const selectedVariant = variants[selectedVariantIndex] || null

    const [currentImg, setCurrentImg] = useState(0)

    const [quantity, setQuantity] = useState(1)

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

        // const maxProducts = 5
        // const viewed = JSON.
    }, [slug])

    const price = selectedVariant?.discount_price ? <span className="text-orange-600"><span className="line-through text-gray-700 mr-2">{selectedVariant?.price.replace(".", ",")}</span>{selectedVariant?.discount_price.replace(".", ",")} zł</span> :
        <span className="text-gray-700">{selectedVariant?.price.replace(".", ",")} zł</span>

    if(loading){
        return (
            <div className="flex justify-center items-center text-center">
                Ładowanie...
            </div>
        )
    }


    return (
        <div className="max-w-screen-lg mx-auto">
            <Link to="/shop" className="text-center" >Powrót do sklepu</Link>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-30 mt-10">
                <div className="flex flex-col gap-5 w-full justify-center items-center">
                    <div className="w-[600px] h-[480px] flex items-center justify-center bg-white rounded-xl shadow-xl">
                        <img 
                            src={
                                product?.images?.[currentImg]?.image
                                ? BASE_URL + product.images[currentImg].image
                                : "https://placehold.co/600x400"
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
                <div className="w-full rounded-sm bg-gray-200 shadow-lg p-6 mx-auto flex flex-col gap-6">
                    <div className="flex flex-col gap-2">
                        <h1 className="text-4xl font-bold text-gray-900">{product.name}</h1>
                        <span className="text-sm text-gray-400">{selectedVariant ? `Kod produktu: ${selectedVariant.sku}` : "Ładowanie..."}</span>
                    </div>
                    
                    {product.promotions?.length > 0 && (
                        <div className="flex flex-col items-start mt-2">
                            <span className="bg-orange-600 text-sm text-white font-semibold rounded-l-md rounded-r-2xl px-3 py-1 mb-1 shadow">
                            Promocje!
                            </span>
                            <span className="text-gray-800 text-sm">
                            Dostępne dla&nbsp;
                            {product.promotions[0].size ? "rozmiarów" : "kolorów"}:&nbsp;
                            <span className="font-semibold">
                                {product.promotions
                                .map(promo => promo.size || promo.color)
                                .join(", ")}
                            </span>
                            </span>
                        </div>
                    )}

                    {selectedVariant && (
                        <div className="flex items-end mt-2">
                            <p className="text-3xl font-extrabold">
                                {price}
                                <span className="text-lg text-gray-800 ml-1 font-light">/ szt</span>
                                {selectedVariant?.discount_percent !== null && <span className="bg-orange-600 text-xl text-white font-semibold rounded-l-md rounded-r-2xl ml-4 p-1.5">-{selectedVariant?.discount_percent}% zniżki</span>}
                            </p>
                        </div>
                    )}

                    <div>
                        <ProductVariantsSelect 
                            variants={variants}
                            selectedVariantIndex={selectedVariantIndex}
                            setSelectedVariantIndex={setSelectedVariantIndex}
                            setQuantity={setQuantity}
                        />
                    </div>

                    <div>
                        <label className="mb-1 block text-sm text-gray-400">Liczba sztuk</label>
                        <CustomNumInput 
                        stock={selectedVariant?.stock || 0}
                        quantity={quantity}
                        setQuantity={setQuantity}
                        />
                        <span className="text-sm text-gray-400">{`z ${selectedVariant?.stock ?? 0} sztuk`}</span>
                    </div>

                    <div className="flex flex-col gap-3 mt-2">
                        <button className="w-full bg-gray-500 hover:bg-gray-600 text-white rounded text-lg py-3 font-bold tracking-widest transition">
                        DODAJ DO KOSZYKA
                        </button>
                        <button className="w-full bg-gray-500 hover:bg-gray-600 text-white rounded text-lg py-3 font-bold tracking-widest transition">
                        KUP I ZAPŁAĆ
                        </button>
                    </div>
                </div>
            </div> 
            <ProductSpecifications mainSpecifications={product.specifications || []} variantSpecifications={selectedVariant?.specifications || []}/>
            <ProductDescription description={product.description}/>
            <RelatedProducts products={product.related_products}/>  
                  
        </div>
    )
}

export default ProductDetails