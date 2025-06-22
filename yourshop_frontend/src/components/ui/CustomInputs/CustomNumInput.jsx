const CustomNumInput = ({stock, quantity, setQuantity}) => {
    const handlePlus = () => setQuantity(q => Math.min(stock, q + 1))
    const handleMinus = () => setQuantity(q => Math.max(1, q - 1))
    
    return (
        <div className="w-full flex flex-col gap-3">
            <div className="flex items-center">
                <button
                    type="button"
                    onClick={handleMinus}
                    className="w-10 h-10 border border-gray-700 bg-white text-gray-700 text-2xl hover:bg-gray-300 transition"
                >-</button>
                <input 
                    type="number" 
                    min={1}
                    max={stock}
                    value={quantity}
                    onChange={e => setQuantity(Math.max(1, Math.min(stock, Number(e.target.value) || 1)))}
                    className="no-spinner w-16 h-10 border-t border-b text-center bg-gray-300 text-lg focus:outline-none"
                />
                <button
                    type="button"
                    onClick={handlePlus}
                    className="w-10 h-10 border border-gray-700 bg-white text-gray-700 text-2xl hover:bg-gray-300 transition"
                >+</button>
            </div>
        </div>
    )
}

export default CustomNumInput