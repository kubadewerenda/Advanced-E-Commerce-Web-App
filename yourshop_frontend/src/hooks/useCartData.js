import { useState, useEffect } from "react"
import api from "../api/api"

function useCartData(){
    const [cartItems, setCartItems] = useState([])
    const [cartTotal, setCartTotal] = useState(0.00)
    const [loading, setLoading] = useState(false)

    const cartCode = localStorage.getItem("cart_code")

    useEffect(() => {
        setLoading(true)
        if(cartCode){
            api.get(`/api/cart/${cartCode}`)
            .then(res => {
                console.log(res.data)
                setCartItems(res.data.items)
                setCartTotal(res.data.sum_total)
                setLoading(false)
            })
            .catch(err => {
                console.log(err.message)
                setLoading(false)
            })
        }
    }, [cartCode])

    return {cartItems, setCartItems, cartTotal, setCartTotal, loading}
}

export default useCartData