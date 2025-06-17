import React from 'react'

export const Footer = () => {
    return (
        <footer className="absolute bottom-0 right-0 bg-gray-900 w-full">  
            <div className="flex justify-center items-center my-4">
                <p className="text-white text-sm">&copy; YourShop {new Date().getFullYear()} | Made by Jakub Dewerenda</p>
            </div>
        </footer>
    )
}

export default Footer
