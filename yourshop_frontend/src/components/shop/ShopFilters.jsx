import { useEffect, useMemo } from "react"

const ShopFilters = ({
    query, setQuery,
    sort, setSort,
    category, setCategory,
    subcategory, setSubcategory,
    priceFrom, setPriceFrom,
    priceTo, setPriceTo,
    pageSize, setPageSize,
    categories,
    resetFilters,
}) => {
    const subcategories =  categories.find(cat => cat.slug === category)?.children || []

    return (
        <form onSubmit={e => e.preventDefault()} className="mb-6 flex flex-wrap gap-2 items-end">
            <input 
                type="text" 
                name="q" 
                value={query}
                onChange={e => setQuery(e.target.value)}
                className="border px-3 py-2 rounded-lg" 
            />

            <select 
                value={sort} 
                onChange={e => setSort(e.target.value)}
                className="border px-3 py-2 rounded-lg"
            >
                <option value="">Sortowanie</option>
                <option value="price">Cena: Najtańsze</option>
                <option value="-price">Cena: Najdroższe</option>
                <option value="-created_at">Najnowsze</option>
                <option value="created_at">Najstarsze</option>
            </select>

            <select 
                value={category} 
                onChange={e => {
                    setCategory(e.target.value)
                    setSubcategory("")
                }}
                className="border px-3 py-2 rounded-lg"
            >
                <option value="">Kategoria</option>
                {categories.map(cat => (
                    <option value={cat.slug} key={cat.id}>{cat.name}</option>
                ))}
            </select>

            <select 
                value={subcategory} 
                onChange={e => setSubcategory(e.target.value)}
                className="border px-3 py-2 rounded-lg"
            >
                <option value="">Podkategoria</option>
                {subcategories.map(sub => (
                    <option value={sub.slug} key={sub.id}>{sub.name}</option>
                ))}
            </select>

            <input 
                type="number"
                placeholder="Cena od:"
                value={priceFrom}
                onChange={e => setPriceFrom(e.target.value)}
                className="border px-3 py-2 rounded-lg w-28"
                min="0" 
                step="any"
            />

            <input 
                type="number"
                placeholder="Cena do:"
                value={priceTo}
                onChange={e => setPriceTo(e.target.value)}
                className="border px-3 py-2 rounded-lg w-28"
                min="0" 
                step="any"
            />

            {/* <select 
                value={pageSize} 
                onChange={e => {
                    setCurrentPage(1)
                    setPageSize(e.target.value)
                }}
                className="border px-3 py-2 rounded-lg w-12"
            >
                <option value="12">Produktów na stronie</option>
                <option value="2">2</option>
                <option value="24">12</option>
                <option value="64">24</option>
            </select> */}

            {/* <button type="submit" className="bg-gray-600 text-white px-4 py-2 rounded-lg">
                Filtruj
            </button> */}
            <button type="button" onClick={resetFilters} className="bg-gray-300 text-gray-700 px-3 py-2 rounded-lg ml-2">
                Resetuj
            </button>
        </form>
    )
}

export default ShopFilters