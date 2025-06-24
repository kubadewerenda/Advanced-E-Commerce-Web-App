import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, Autoplay } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import { BASE_URL } from '../../api/api';
import { Link } from 'react-router-dom'

const SwiperProducts = ({products, title}) => {
    if(!products?.length) return null

    return (
        <div className="my-12 mt-10 w-full rounded-sm bg-gray-200 shadow-lg p-6 mx-auto flex flex-col gap-6">
            <h3 className="text-3xl font-bold text-gray-800">{title}</h3>
            <div>
                <Swiper
                    modules={[Navigation, Pagination, Autoplay]}
                    navigation
                    pagination={{clickable: true}}
                    spaceBetween={10}
                    slidesPerView={2}
                    loop={products.length > 3}
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
                                        src={ BASE_URL + prod.images?.[0]?.image}
                                        alt={prod.name}
                                        className="w-full h-32 object-contain mb-2"
                                        loading="lazy"
                                    />
                                    <div className="font-medium text-sm line-clamp-2">
                                        {prod.name}
                                    </div>
                                    <div className="font-light text-sm line-clamp-2">
                                        {prod.description.slice(0,30)}...
                                    </div>
                                    <div className="flex-end font-bold text-base text-gray-600 mt-auto">
                                        <p>
                                            {prod.variants?.length > 1 ? `od ${prod.variants?.[0]?.price}` : prod.variants?.[0]?.price} zł
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

export default SwiperProducts