import React from 'react'

const ShopError = ({error}) => {
    if(!error) return null
    return (
        <div className="bg-red-100 text-red-700 px-4 rounded-lg my-6 text-center">
            {error}
        </div>
    )
}

export default ShopError