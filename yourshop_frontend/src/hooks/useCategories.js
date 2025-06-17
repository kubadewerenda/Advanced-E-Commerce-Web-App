import { useEffect, useState } from "react";
import api from "../api/api";


export default function useCategories(){
    const [categories, setCategories] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")

    useEffect(() => {
        setLoading(true)
        setError("")
        api.get("/api/categories/")
        .then(res => setCategories(res.data))
        .catch(err => setError(err.message))
        .finally(() => setLoading(false))
    }, [])

    return {categories, loading, error}
}