import { useEffect, useRef, useState } from 'react'
import { BASE_URL } from '../../api/api'

const ProductGallery = ({images = [], currentImg, setCurrentImg}) => {
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

    return (
        <div className="col-span-3 flex flex-col gap-5 w-full justify-start items-center">
            <div className="w-full h-[400px] flex items-center justify-center bg-white rounded-xl shadow-xl">
                <img 
                    src={
                        images?.[currentImg]?.image
                        ? BASE_URL + images[currentImg].image
                        : "https://placehold.co/600x400"
                    }
                    onClick={() => setOpen((o) => !o)}
                    alt={images?.[currentImg]?.alt_text || ""}
                    className="object-contain w-full h-full rounded-x"
                />
            </div>
            <div className="flex flex-wrap gap-0.5 mt-4 overflow-x-auto w-full justify-center">
                {images?.length > 0 && (
                    images.map((img, i) => (
                        <button
                            key={img.id}
                            onClick={() => setCurrentImg(i)}
                            onMouseEnter={() => setCurrentImg(i)}
                            className={`w-24 h-20 border overflow-hidden ${currentImg === i ? 'border-gray-400' : 'border-gray-300'}`}
                        >
                            <img src={BASE_URL + img.image} alt={img.alt_text} className="w-full h-full object-contain" />                                
                        </button>
                    ))
                )}
            </div>
            {open && (
                <div
                    className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex justify-center items-center"
                    onClick={() => setOpen(false)}
                    ref={ref}
                >
                    <div className="relative">
                        <img
                            src={
                                images?.[currentImg]?.image
                                ? BASE_URL + images[currentImg].image
                                : "https://placehold.co/600x400"
                            }
                            alt={images?.[currentImg]?.alt_text || ""}
                            className="object-fit w-[800px] h-[650px] max-w-[95vw] max-h-[80vh] rounded-xl shadow-2xl"
                            onClick={e => e.stopPropagation()}
                        />
                        <button
                            className="absolute top-2 right-2 text-white text-3xl font-bold cursor-pointer bg-black/40 rounded-full w-10 h-10 flex items-center justify-center"
                            onClick={() => setOpen(false)}
                        >
                        ×
                        </button>
                        <button 
                            className="absolute top-0 left-0 w-1/2 h-full bg-transparent"
                            onClick={e => {
                                e.stopPropagation()
                                if(currentImg > 0) setCurrentImg(i => i - 1)
                            }}
                        >
                        </button>
                        <button 
                            className="absolute top-0 right-0 w-1/2 h-full bg-transparent"
                            onClick={e => {
                                e.stopPropagation()
                                if(currentImg < (images?.length - 1)) setCurrentImg(i => i + 1)
                            }}
                        >
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}

export default ProductGallery