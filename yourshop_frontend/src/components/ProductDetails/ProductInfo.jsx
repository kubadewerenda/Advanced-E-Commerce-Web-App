import ProductVariantsSelect from "./ProductVariantsSelect"
import CustomNumInput from "../ui/CustomInputs/CustomNumInput"
import { TbTruckDelivery } from "react-icons/tb"
import { MdOutlineForward30 } from "react-icons/md"
import { LuWallet } from "react-icons/lu"
import api from "../../api/api"

const ProductInfo = ({
    product,
    selectedVariant,
    selectedVariantIndex,
    setSelectedVariantIndex,
    variants,
    quantity,
    setQuantity,
}) => {
    const cart_code = localStorage.getItem("cart_code");

    const price = selectedVariant?.discount_price ? <span className="text-orange-600"><span className="line-through text-gray-700 mr-2">{selectedVariant?.price.replace(".", ",")}</span>{selectedVariant?.discount_price.replace(".", ",")} zł</span> :
        <span className="text-gray-700">{selectedVariant?.price.replace(".", ",")} zł</span>

    const newItem = {cart_code: cart_code, variant_sku: selectedVariant?.sku, quantity: quantity}

    function addProductToCart(){
        console.log(selectedVariant.sku)
        api.post("api/add_to_cart/", newItem)
        .then(res => {
            console.log(res.data)
        })
        .catch(err => {
            console.log(err.message)
        })
    }
        
    return (
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
                    Dostępne dla wariantów:&nbsp;
                    <span className="font-semibold">
                        {product.promotions
                        .map(promo => promo.name)
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
                <button 
                    onClick={addProductToCart}
                    disabled={!selectedVariant}
                    className="w-full bg-gray-500 hover:bg-gray-600 text-white rounded text-lg py-3 font-bold tracking-widest transition">
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
    )
}

export default ProductInfo