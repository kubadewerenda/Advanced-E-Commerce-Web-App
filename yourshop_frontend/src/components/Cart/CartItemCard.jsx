import React, { useEffect, useRef, useState } from 'react'
import api, { BASE_URL } from '../../api/api'
import CustomNumInput from '../ui/CustomInputs/CustomNumInput'
import { GiTrashCan } from "react-icons/gi"
import { Link } from 'react-router-dom'


const CartItemCard = ({item, cartItems, setCartItems, cartTotal, setCartTotal, setNumCartItems, setTotalValue}) => {
    const [quantity, setQuantity] = useState(item.quantity)
    const [actualTotal, setActualTotal] = useState(item.total)
    const [regularPrice, setRegularPrice] = useState(item.variant.price * item.quantity)
    const [loading, setLoading] = useState(false)

    const firstRender = useRef(true)
    const prevQuantity = useRef(quantity)

    const itemID = {item_id: item.id}
    const itemData = {item_id: item.id, quantity: quantity}

    function deleteCartItem(){
        const confirmDelete = window.confirm("Napewno chcesz usunąć produkt?")
        if(confirmDelete){
            api.post("api/ci_delete/", itemID)
            .then(res => {
                console.log(res.data)

                setCartItems(cartItems.filter(cartItem => cartItem.id != item.id))
                
                setCartTotal(cartItems.filter(cartItem => cartItem.id != item.id)
                .reduce((acc, curr) => acc + curr.total, 0))

                setTotalValue(cartItems.filter(cartItem => cartItem.id != item.id)
                .reduce((acc, curr) => acc + curr.total, 0))

                setNumCartItems(cartItems.filter(cartItem => cartItem.id != item.id)
                .reduce((acc, curr) => acc + curr.quantity, 0))
            })
            .catch(err => {
                console.log(err.message)
            })
        }
    }

    useEffect(() => {
        if(firstRender.current){
            firstRender.current = false
            prevQuantity.current = quantity
        }

        if(prevQuantity.current === quantity) return
        prevQuantity.current == quantity

        setLoading(true)
        api.patch("api/ci_up_quantity/", itemData)
        .then(res => {
            console.log(res.data)

            setCartTotal(cartItems.map((cartItem) => cartItem.id === item.id ? res.data.data : cartItem)
            .reduce((acc, curr) => acc + curr.total, 0))

            setNumCartItems(cartItems.map((cartItem) => cartItem.id === item.id ? res.data.data : cartItem)
            .reduce((acc, curr) => acc + curr.quantity, 0))

            setTotalValue(cartItems.map((cartItem) => cartItem.id === item.id ? res.data.data : cartItem)
            .reduce((acc, curr) => acc + curr.total, 0))

            setRegularPrice(res.data.data.variant.price * res.data.data.quantity)
            setActualTotal(res.data.data.total)

            setLoading(false)
        })
        .catch(err => {
            console.log(err.message)
            setLoading(false)
        })
    }, [quantity])

    const itemPrice = item.variant.discount_price ? <p className="text-orange-600 text-xl font-medium"><span className="line-through text-gray-700 mr-2">{regularPrice} zł</span>{actualTotal} zł</p> : 
                    <p className="text-gray-700 text-xl font-medium">{actualTotal} zł</p>

    return (
        <Link to={`/products/${item.variant.product.slug}`}>
            <div className="flex justify-between w-full items-center gap-5 bg-gray-300 p-3">
                <img 
                    src={BASE_URL + item.variant.product.main_image} 
                    alt={item.variant.product} 
                    className="w-28 h-22"
                />
                <div>
                    <h4 className="text-lg text-gray-900 font-medium">{item.variant.product.name}</h4>
                    <p className="text-sm text-gray-800 font-normal">Wariant: {item.variant.variant_name}</p>
                </div>
                <div className="flex flex-col">
                    <CustomNumInput 
                        stock={item.variant.stock}
                        quantity={quantity}
                        setQuantity={setQuantity}
                    />
                    <p>z {item.variant.stock} szt</p>
                </div>
                <div className="">
                    {itemPrice}
                    <p>{item.variant.discount_price ? item.variant.discount_price : item.variant.price}<span>/szt</span></p>
                </div>
                <div>
                    <button
                        onClick={deleteCartItem}
                        className="hover:scale-110 duration-300"
                    >
                        <GiTrashCan size={24} color="#666666"/>
                    </button>
                </div>
            </div>
        </Link>           
    )
}

export default CartItemCard