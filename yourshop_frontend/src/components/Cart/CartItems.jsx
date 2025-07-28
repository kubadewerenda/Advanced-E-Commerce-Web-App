import React from 'react'
import CartItemCard from './CartItemCard'

const CartItems = ({cartItems}) => {
    return (
        <div className="col-span-4 flex flex-col gap-5 w-full justify-center items-start">
            {cartItems.map(cartItem => <CartItemCard key={cartItem.id} item={cartItem}/>)}
        </div>
    )
}

export default CartItems