import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, Autoplay } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import { BASE_URL } from '../../api/api';
import { Link } from 'react-router-dom'

const RelatedProducts = ({products}) => {
    if(!products?.length) return null
    return (
        <div className="my-12 max-w-screen-lg mx-auto">
            <div className="flex items-center justify-start">
                <h3 className="text-3xl text-gray-800 font-light">Powiązane produkty</h3>
            </div>
            <hr />
            <div className="mt-5">
                <Swiper
                    modules={[Navigation, Pagination, Autoplay]}
                    navigation
                    pagination={{clickable: true}}
                    spaceBetween={10}
                    slidesPerView={2}
                    loop={true}
                    breakpoints={{
                    640: { slidesPerView: 2 },
                    768: { slidesPerView: 2 },
                    1024: { slidesPerView: 2 }
                    }}
                    autoplay={{
                        delay: 2500,
                        disableOnInteraction: false, 
                        pauseOnMouseEnter: true  
                    }}
                    className="p-10"
                >
                    {products.map(prod => (
                        <SwiperSlide key={prod.id} className="p-10">
                            <Link to={`/products/${prod.slug}`} onClick={e => e.stopPropagation()}>
                                <div className="bg-white rounded-sm shadow-sm p-3 hover:shadow-xl transition h-full flex flex-col">
                                    <img
                                        src={ BASE_URL + prod.images[0].image}
                                        alt={prod.name}
                                        className="w-full h-32 object-contain mb-2"
                                        loading="lazy"
                                    />
                                    <div className="font-medium text-sm line-clamp-2">{prod.name}</div>
                                    <div className="font-light text-sm line-clamp-2">{`${prod.description.slice(0,30)}...`}</div>
                                    <div className="flex-end font-bold text-base text-gray-600 mt-auto">
                                        <p>
                                            {prod.price} zł
                                        </p>
                                    </div>
                                </div>
                            </Link>
                        </SwiperSlide>
                        ))}
                </Swiper>
            </div>
        </div>
    )
}

export default RelatedProducts