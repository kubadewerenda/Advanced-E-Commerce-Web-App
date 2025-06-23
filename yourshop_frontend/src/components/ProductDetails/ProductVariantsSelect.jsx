import { useEffect, useRef, useState } from 'react'
import { RiArrowDropDownLine } from "react-icons/ri";
import { RiArrowDropUpLine } from "react-icons/ri";

const ProductVariantsSelect = ({variants, selectedVariantIndex, setSelectedVariantIndex, setQuantity}) => {
    const [open, setOpen] = useState(false)
    const ref = useRef(null)

    useEffect(() => {
        function handleClickOutside(e){
            if(ref.current && !ref.current.contains(e.target)){
                setOpen(false)
            }
        }
        document.addEventListener("mousedown", handleClickOutside)
        return () => document.removeEventListener("mousedown", handleClickOutside)
    }, [])

    function getVariantLabel(v){
        if (!v) return "Brak danych";
        return [v.size, v.color].filter(Boolean).join(" / ") || "Standard"
    }

    if(variants.length === 1) return null

    return (
        <div className="relative w-60" ref={ref}>
            <label className="text-sm text-gray-700 font-medium">Wybierz {variants[0]?.size ? "rozmiar" : "kolor"}:</label>
            <button 
                type="button"
                className="w-full border-b-2 border-gray-800 bg-white text-left text-lg font-semibold text-gray-700 flex justify-between items-center"
                onClick={() => setOpen((o) => !o)}
            >
                {getVariantLabel(variants[selectedVariantIndex])}
                <span className="ml-1">{open ? <RiArrowDropUpLine size={32} /> : <RiArrowDropDownLine size={32} />}</span>
            </button>
            {open && (
                <ul className="absolute z-10 w-full bg-white shadow">
                    {variants.map((v, index) => (
                        <li 
                            key={v.id}
                            onClick={() => {
                                setSelectedVariantIndex(index)
                                setQuantity(1)
                                setOpen(false)
                            }}
                            className={`p-2 hover:bg-gray-400 text-lg border-b cursor-pointer ${index === selectedVariantIndex ? "bg-gray-300 font-semibold" : ""}`}
                        >
                            {getVariantLabel(v)}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    )
}

export default ProductVariantsSelect