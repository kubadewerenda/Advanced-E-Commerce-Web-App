import { useState, useCallback, useEffect, useRef } from "react";
import api from "../api/api";
import { useSearchParams } from "react-router-dom";

const DEFAULTS = {
    page: 1,
    page_size: 2,
    q: "",
    ordering: "",
    category: "",
    subcategory: "",
    price_min: "",
    price_max: "",
}

function getParam(searchParams, key){
    const v = searchParams.get(key)
    if(v === null || v === undefined) return DEFAULTS[key]
    if(["page", "page_size"].includes(key)) return Number(v) || DEFAULTS[key]
    if (key === "category" && (v === "null" || v === "undefined")) return ""
    return v;
}

export default function useProductSearch() {
    const [products, setProducts] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const [totalCount, setTotalCount] = useState(0)

    const [searchParams, setSearchParams] = useSearchParams()

    const debounceTimeout = useRef()

    //======== PARAMS Z SEARCHPARAMS ========
    const q = getParam(searchParams, "q")
    const ordering = getParam(searchParams, "ordering")
    const category = getParam(searchParams, "category")
    const subcategory = getParam(searchParams, "subcategory")
    const priceMin = getParam(searchParams, "price_min")
    const priceMax = getParam(searchParams, "price_max")
    const page = getParam(searchParams, "page")
    const pageSize = getParam(searchParams, "page_size")

    const setFilter = useCallback((params) => {
        const sp = new URLSearchParams(window.location.search)
        Object.entries(params).forEach(([key, value]) => {
            if(value === "" || value === null) sp.delete(key)
            else sp.set(key, value)
        })
        if(!("page" in params)) sp.set("page", 1)
        setSearchParams(sp.toString())
    }, [setSearchParams])

    const resetFilters = () => setSearchParams(DEFAULTS)

    //======== DYNAMICZNE ZAPYTANIE ========
    useEffect(() => {
        setLoading(true)

        if(debounceTimeout.current) clearTimeout(debounceTimeout.current)
        
        const doFetch = () => {
            let params = []

            if(q) params.push(`q=${encodeURIComponent(q)}`)
            if(ordering) params.push(`ordering=${ordering}`)
            if(category) params.push(`category=${category}`)
            if(subcategory) params.push(`subcategory=${subcategory}`)
            if(priceMin) params.push(`price_min=${priceMin}`)
            if(priceMax) params.push(`price_max=${priceMax}`)

            params.push(`page=${page}`)
            params.push(`page_size=${pageSize}`)

            const url = `api/products?${params.join("&")}`

            api.get(url)
            .then(res => {
                console.log(res.data.results)
                setProducts(res.data.results)
                setTotalCount(res.data.count)
                setError("")
            })
            .catch(err => setError(err.message))
            .finally(() => setLoading(false))            
        }

        if (q) {
            debounceTimeout.current = setTimeout(doFetch, 400)//debounce 400ms na search q
        }else{
            doFetch()
        }

        window.scrollTo({top: 0, behavior: "smooth"})

        return () => {
            if(debounceTimeout.current) clearTimeout(debounceTimeout.current)
        }

    }, [q, ordering, category, subcategory, priceMin, priceMax, page, pageSize])

    return {
        products, loading, error, totalCount,
        query: q, 
        setQuery: val => setFilter({q: val}),
        sort: ordering, 
        setSort: val => setFilter({ordering: val}),
        category, 
        setCategory: val => setFilter({category: val, subcategory: "" }),
        subcategory, 
        setSubcategory: val => setFilter({subcategory: val}),
        priceFrom: priceMin, 
        setPriceFrom: val => setFilter({price_min: val}),
        priceTo: priceMax, 
        setPriceTo: val => setFilter({price_max: val}),
        currentPage: page, 
        setCurrentPage: val => setFilter({page: val}),
        pageSize,
        setPageSize: val => setFilter({page_size: val}),
        resetFilters,
        generateLink: () => `/shop?${searchParams.toString()}`
    }
}
