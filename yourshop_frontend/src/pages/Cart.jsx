import { useEffect, useState } from "react"
import api from "../api/api"
import useCartData from "../hooks/useCartData"
import CartItems from "../components/Cart/CartItems"


const Cart = ({setNumCartItems, setTotalValue}) => {
    const {cartItems, setCartItems, cartTotal, setCartTotal, loading} = useCartData()

    if(loading){
        return <p>Ładowanie...</p>
    }

    if(cartItems.length < 1){
        return (
          <div className="flex justify-center items-center text-xl text-black">
              Koszyk jest pusty!
          </div>
        )
    }

    return (
      <div className="max-w-screen-lg mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-6 gap-x-10 mt-10">
              <CartItems 
                  cartItems={cartItems}
                  setCartItems={setCartItems}
                  cartTotal={cartTotal}
                  setCartTotal={setCartTotal}
                  setNumCartItems={setNumCartItems}
                  setTotalValue={setTotalValue}
              />  
          </div>
      </div>
    )
}

export default Cart