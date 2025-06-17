import { BrowserRouter, Routes, Route } from "react-router-dom"
import MainLayout from "./layouts/MainLayout"
import Shop from "./pages/Shop"
import ProductDetails from "./pages/ProductDetails"

function App() {

    return (
        <BrowserRouter>
            <MainLayout>
                <Routes>
                    <Route path="/shop" element={<Shop />}></Route>
                    <Route path="products/:slug" element={<ProductDetails />}></Route>
                </Routes> 
            </MainLayout>         
        </BrowserRouter>
    )
  }

export default App
