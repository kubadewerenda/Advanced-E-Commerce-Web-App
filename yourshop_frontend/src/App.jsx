import { BrowserRouter, Routes, Route } from "react-router-dom"
import MainLayout from "./layouts/MainLayout"
import Shop from "./pages/Shop"
import ProductDetails from "./pages/ProductDetails"
import Cart from "./pages/Cart"
import { useEffect, useState } from "react"
import api from "./api/api"

const App = () => {
    const [numCartItems, setNumCartItems] = useState(0);
    const [totalValue, setTotalValue] = useState(0);
    const cartCode = localStorage.getItem("cart_code");

    useEffect(() => {
        if(cartCode){
            api.get(`api/cart_num_of_items?cart_code=${cartCode}`)
            .then(res => {
                console.log(res.data)
                setNumCartItems(res.data.num_of_items)
                setTotalValue(res.data.sum_total)
            })
            .catch(err => {
                console.log(err.message)
            })
        }
    }, [])

    console.log(totalValue)

    return (
        <BrowserRouter>
            <MainLayout numCartItems={numCartItems} totalValue={totalValue}>
                <Routes>
                    <Route path="/shop" element={<Shop />} />
                    <Route path="products/:slug" element={<ProductDetails setNumCartItems={setNumCartItems} setTotalValue={setTotalValue} />} />
                    <Route path="koszyk/:cart_code" element={<Cart setNumCartItems={setNumCartItems}/>} />
                </Routes> 
            </MainLayout>         
        </BrowserRouter>
    )
  }

export default App
