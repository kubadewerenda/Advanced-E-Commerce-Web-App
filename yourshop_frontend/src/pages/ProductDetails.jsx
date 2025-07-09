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
import ProductGallery from '../components/ProductDetails/ProductGallery'
import ProductInfo from '../components/ProductDetails/ProductInfo'

const ProductDetails = ({setNumCartItems, setTotalValue}) => {
    const [product, setProduct] = useState({})
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const [selectedVariantIndex, setSelectedVariantIndex] = useState(0)
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

    const variants = product.variants || []
    const selectedVariant = variants[selectedVariantIndex] || null 

    return (
        <div className="max-w-screen-lg mx-auto">
            <Link to="/shop" className="text-center" >Powrót do sklepu</Link>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-x-10 mt-10">
                <ProductGallery 
                    images={product.images}
                    currentImg={currentImg}
                    setCurrentImg={setCurrentImg}
                />
                <ProductInfo 
                    product={product}
                    selectedVariant={selectedVariant}
                    selectedVariantIndex={selectedVariantIndex}
                    setSelectedVariantIndex={setSelectedVariantIndex}
                    variants={variants}
                    quantity={quantity}
                    setQuantity={setQuantity}
                    setNumCartItems={setNumCartItems} 
                    setTotalValue={setTotalValue}
                />
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
        </div>
    )
}

export default ProductDetails