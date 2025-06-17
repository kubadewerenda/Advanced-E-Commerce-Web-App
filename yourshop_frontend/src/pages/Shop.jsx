import { useEffect, useState } from "react"
import api from "../api/api"
import ProductContainer from "../components/shop/ProductContainer"
import ShopFilters from "../components/shop/ShopFilters"
import useProductSearch from "../hooks/useProductSearch"
import ShopResultsInfo from "../components/shop/ShopResultsInfo"
import ShopPagination from "../components/shop/ShopPagination"
import ShopError from "../components/shop/ShopError"
import useCategories from "../hooks/useCategories"

const Shop = () => {
    const {categories, loading: categoriesLoading, error: categoriesError} = useCategories()
    const hookData = useProductSearch()
    return (
        <div className="max-w-screen-5xl mx-auto">  
            <ShopFilters {...hookData} categories={categories}/>
            <ShopResultsInfo totalCount={hookData.totalCount} />
            <ProductContainer products={hookData.products} loading={hookData.loading} /> 
            <ShopPagination
                currentPage={hookData.currentPage}
                setCurrentPage={hookData.setCurrentPage}
                totalCount={hookData.totalCount}
                pageSize={hookData.pageSize}    
            />       
            <ShopError error={hookData.error || categoriesError} />
        </div>
    )
}

export default Shop