import React, { useState } from 'react'

const ShopResultsInfo = ({totalCount}) => {
    let text = ""
    if(totalCount){
        text = `Znaleziono ${totalCount} produktów.`
    }else{
        text = "Brak określonych produktów."
    }

    return (
        <div className="text-gray-500 mb-3 text-lg text-center">
            <span className="font-semibold text-lg">{text}</span>
        </div>
    )
}

export default ShopResultsInfo