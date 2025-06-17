import React from 'react'

const ShopPagination = ({currentPage, setCurrentPage, totalCount, pageSize}) => {
    const totalPages = Math.ceil(totalCount/pageSize)
    if(totalPages <= 1) return null

    const getPages = () => {
        let pages = []
        let start = Math.max(1, currentPage - 3)
        let end = Math.min(totalPages, currentPage + 3)
        for(let i = start; i <= end; i++){
            pages.push(i)
        }
        return pages
    }

    return (
        <div className="flex justify-center gap-2 mt-6 flex-wrap">
            <button
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(currentPage - 1)}
                className="px-4 py-2 rounded-lg bg-gray-200"
            >
                Poprzendia
            </button>

            {getPages().map(i => (
                <button 
                    key={i}
                    onClick={() => setCurrentPage(i)}
                    className={`px-3 py-2 ${currentPage === i ? 'bg-gray-600 text-white' : 'bg-gray-100'}`}
                >
                    {i}
                </button>
            ))}

            <button
                disabled={currentPage >= totalPages}
                onClick={() => setCurrentPage(currentPage + 1)}
                className="px-4 py-2 rounded-lg bg-gray-200"
            >
                Następna
            </button>
        </div>
    )
}

export default ShopPagination