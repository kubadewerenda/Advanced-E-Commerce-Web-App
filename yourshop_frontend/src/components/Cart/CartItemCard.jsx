import React, { useState } from 'react'
import api, { BASE_URL } from '../../api/api'
import CustomNumInput from '../ui/CustomInputs/CustomNumInput'
import { GiTrashCan } from "react-icons/gi"

const CartItemCard = ({item}) => {
    const [quantity, setQuantity] = useState(item.quantity)

    const itemID = {item_id: item.id}

    function deleteCartItem(){
        const confirmDelete = window.confirm("Napewno chcesz usunąć produkt?")
        if(confirmDelete){
            api.post("api/ci_delete/", itemID)
            .then(res => {
                console.log(res.data)
            })
            .catch(err => {
                console.log(err.message)
            })
        }
    }

    const regularPrice = item.variant.price * item.quantity
    const itemPrice = item.variant.discount_price ? <p className="text-orange-600 text-xl font-medium"><span className="line-through text-gray-700 mr-2">{regularPrice} zł</span>{item.total} zł</p> : 
                    <p className="text-gray-700 text-xl font-medium">{item.total} zł</p>

    return (
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
    )
}

export default CartItemCard