import React, { useEffect, useRef, useState } from 'react'
import api, { BASE_URL } from '../api/api'
import { Link, useParams } from 'react-router-dom'
import SwiperProducts from '../components/ProductDetails/SwiperProducts'
import ProductVariantsSelect from '../components/ProductDetails/ProductVariantsSelect'
import ProductSpecifications from '../components/ProductDetails/ProductSpecifications'
import CustomNumInput from '../components/ui/CustomInputs/CustomNumInput'
import ProductDescription from '../components/ProductDetails/ProductDescription'

import { TbTruckDelivery } from "react-icons/tb"
import { MdOutlineForward30 } from "react-icons/md"
import { LuWallet } from "react-icons/lu"

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
            addRecentlyViewed(res.data)
        })
        .catch(err => {
            console.log(err.message)
            setError(err.message)
        })
        .finally(() => setLoading(false))
    }, [slug])

    const price = selectedVariant?.discount_price ? <span className="text-orange-600"><span className="line-through text-gray-700 mr-2">{selectedVariant?.price.replace(".", ",")}</span>{selectedVariant?.discount_price.replace(".", ",")} zł</span> :
        <span className="text-gray-700">{selectedVariant?.price.replace(".", ",")} zł</span>


    const [open, setOpen] = useState(false)
    
    const ref = useRef(null)
    
    useEffect(() => {
        function handleClickOutside(e){
            if(ref.current && !ref.current.contains(e.target)){
                setOpen(false)
            }
        }
        document.addEventListener("mousedown", handleClickOutside)
        return () => document.removeEventListener("mousedown", handleClickOutside)
    }, [])

    if(loading){
        return (
            <div className="flex justify-center items-center text-center">
                Ładowanie...
            </div>
        )
    }

    function addRecentlyViewed(product){
        const maxProducts = 5
        const viewed = JSON.parse(localStorage.getItem("recently_viewed") || "[]")
        const exists = viewed.find(p => p.id === product.id)

        let newViewed = exists ? viewed.filter(p => p.id !== product.id) : viewed
        newViewed = [{
            id: product.id,
            name: product.name,
            images: product.images,
            slug: product.slug,
            description: product.description,
            variants: product.variants
        }, ...newViewed]

        if (newViewed.length > maxProducts) newViewed = newViewed.slice(0, maxProducts)

        localStorage.setItem("recently_viewed", JSON.stringify(newViewed))
    }


    return (
        <div className="max-w-screen-lg mx-auto">
            <Link to="/shop" className="text-center" >Powrót do sklepu</Link>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-x-10 mt-10">
                <div className="col-span-3 flex flex-col gap-5 w-full justify-start items-center">
                    <div className="w-full h-[400px] flex items-center justify-center bg-white rounded-xl shadow-xl">
                        <img 
                            src={
                                product?.images?.[currentImg]?.image
                                ? BASE_URL + product.images[currentImg].image
                                : "https://placehold.co/600x400"
                            }
                            onClick={() => setOpen((o) => !o)}
                            alt={product?.images?.[currentImg]?.alt_text || product?.name}
                            className="object-contain w-full h-full rounded-x"
                        />
                    </div>
                    <div className="flex flex-wrap gap-0.5 mt-4 overflow-x-auto w-full justify-center">
                        {product?.images?.length > 0 && (
                            product.images.map((img, i) => (
                                <button
                                    key={img.id}
                                    onClick={() => setCurrentImg(i)}
                                    onMouseEnter={() => setCurrentImg(i)}
                                    className={`w-24 h-20 border overflow-hidden ${currentImg === i ? 'border-gray-400' : 'border-gray-300'}`}
                                >
                                    <img src={BASE_URL + img.image} alt={img.alt_text} className="w-full h-full object-contain" />                                
                                </button>
                            ))
                        )}
                    </div>
                </div>
                <div className="col-span-2 w-full rounded-sm bg-gray-200 shadow-lg p-6 mx-auto flex flex-col gap-6">
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

                    <div className="flex items-start gap-y-2 flex-col">
                        <div className="flex items-center text-md text-gray-600 font-medium">
                            <TbTruckDelivery size={32} color="#666666" />
                            <span className="ml-2"><span className="font-bold">Wysyłka </span>w 2 dni</span>
                        </div>

                        <div className="flex items-center text-md text-gray-600 font-medium">
                            <MdOutlineForward30 size={32} color="#666666" />
                            <span className="ml-2"><span className="font-bold">Zwrot </span>do 30 dni</span>
                        </div>

                        <div className="flex items-center text-md text-gray-600 font-medium">
                            <LuWallet size={32} color="#666666" />
                            <span className="ml-2"><span className="font-bold">Płatności </span>online lub za pobraniem</span>
                        </div>
                    </div>
                </div>
            </div> 
            <ProductSpecifications mainSpecifications={product.specifications || []} variantSpecifications={selectedVariant?.specifications || []}/>
            <ProductDescription description={product.description}/>
            <SwiperProducts 
                products={JSON.parse(localStorage.getItem("recently_viewed") || "[]")}
                title={"Ostatnio odwiedzone"}
            /> 
            <SwiperProducts 
                products={product.related_products}
                title={"Zobacz też"}
            />
            {open && (
                <div
                    className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex justify-center items-center"
                    onClick={() => setOpen(false)}
                    ref={ref}
                >
                    <div className="relative">
                        <img
                            src={
                                product?.images?.[currentImg]?.image
                                ? BASE_URL + product.images[currentImg].image
                                : "https://placehold.co/600x400"
                            }
                            alt={product?.images?.[currentImg]?.alt_text || product?.name}
                            className="object-fit w-[800px] h-[650px] max-w-[95vw] max-h-[80vh] rounded-xl shadow-2xl"
                            onClick={e => e.stopPropagation()}
                        />
                        <button
                            className="absolute top-2 right-2 text-white text-3xl font-bold cursor-pointer bg-black/40 rounded-full w-10 h-10 flex items-center justify-center"
                            onClick={() => setOpen(false)}
                        >
                        ×
                        </button>
                        <button 
                            className="absolute top-0 left-0 w-1/2 h-full bg-black/30"
                            onClick={e => {
                                e.stopPropagation()
                                if(currentImg > 0) setCurrentImg(i => i - 1)
                            }}
                        >
                        </button>
                        <button 
                            className="absolute top-0 right-0 w-1/2 h-full bg-black/30"
                            onClick={e => {
                                e.stopPropagation()
                                if(currentImg < (product?.images?.length - 1)) setCurrentImg(i => i + 1)
                            }}
                        >
                        </button>
                    </div>
                </div>
            )}                  
        </div>
    )
}

export default ProductDetails