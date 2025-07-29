import React from 'react'
import CartItemCard from './CartItemCard'

const CartItems = ({cartItems, setCartItems, cartTotal, setCartTotal, setNumCartItems, setTotalValue}) => {
    return (
        <div className="col-span-4 flex flex-col gap-5 w-full justify-center items-start">
            {cartItems.map(cartItem => <CartItemCard 
                                            key={cartItem.id} 
                                            item={cartItem}
                                            cartItems={cartItems}
                                            setCartItems={setCartItems}
                                            cartTotal={cartTotal}
                                            setCartTotal={setCartTotal}
                                            setNumCartItems={setNumCartItems}
                                            setTotalValue={setTotalValue}
                                        />
            )}
        </div>
    )
}

export default CartItems