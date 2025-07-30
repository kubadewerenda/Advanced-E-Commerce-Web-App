import React from 'react'

const CartSummary = ({cartTotal}) => {
    const tax = 0.23
    const delivery = 15.00

    const priceB = cartTotal.toFixed(2).replace(".", ",")
    const priceN = (cartTotal * (1 - tax)).toFixed(2).replace(".", ",")

    const finallPrice = (cartTotal + delivery).toFixed(2).replace(".", ",")

    return (
        <div className="col-span-2 flex flex-col w-full h-fit gap-3 justify-start items-center bg-gray-300 p-5">
            <div className="flex flex-col gap-0.5 justify-center items-start">
                <p className="text-md text-gray-800 font-normal">Wartość produktów: <span className="font-bold text-amber-500">{priceB} zł</span>/brutto</p>
                <p className="text-sm text-gray-700 font-light">Wartość produktów: <span className="font-medium text-gray-800">{priceN} zł</span>/netto</p>
            </div>
            <div className="flex items-center self-start">
                <p className="text-md text-gray-800 font-normal">Dostawa od 15,00 zł</p>
            </div>
            <div className="flex flex-col border-t-2 border-gray-500 w-full justify-center items-center gap-2 py-3">
                <div className="flex justify-between items-center w-full">
                    <p className="text-md text-gray-800 font-medium">Razem z dostawą</p>
                    <p className="text-md text-amber-500 font-medium">{finallPrice} <span className="text-gray-800">zł</span></p>
                </div>
                <button className="max-w-full w-56 h-10 bg-gray-500 text-md text-amber-100 font-medium hover:bg-amber-100 hover:text-gray-500 duration-300">
                    Zamów i zapłać
                </button>
            </div>
        </div>
    )
}

export default CartSummary