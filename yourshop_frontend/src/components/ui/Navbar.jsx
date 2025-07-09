import { MdOutlineShoppingCart } from "react-icons/md"
import { Link } from 'react-router-dom'

const Navbar = ({numCartItems, totalValue}) => {
    return (    
        <nav className="bg-gray-300 rounded-b-2xl">
            <div className="max-w-screen-xl flex flex-col items-center justify-between mx-auto p-4 gap-y-2">
                <div>
                    <div className="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-cta">
                        <ul className="flex flex-col font-light text-normal p-4 md:p-0 mt-4 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0">
                            <li>
                                <a href="/shop" className="block py-2 px-3 md:p-0 text-gray-800" aria-current="page">Sklep</a>
                            </li>
                            <li>
                                <a href="/" className="block py-2 px-3 md:p-0 text-gray-800">O nas</a>
                            </li>
                            <li>
                                <a href="#" className="block py-2 px-3 md:p-0 text-gray-800">Kontakt</a>
                            </li>
                            <li>
                                <a href="#" className="block py-2 px-3 md:p-0 text-gray-800">Opinie</a>
                            </li>
                        </ul>
                    </div>
                </div>
                <div className="flex justify-between w-full md:border-t md:border-gray-500 md:pt-3">
                    <div>
                        <a href="/" className="flex items-center space-x-3 rtl:space-x-reverse">
                            <span className="self-center text-2xl text-gray-100 font-semibold whitespace-nowrap px-3">Your<span className="text-orange-200">Shop</span></span>
                        </a>
                    </div>
                    {/* <div className="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
                        <button type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Get started</button>
                        <button data-collapse-toggle="navbar-cta" type="button" className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-cta" aria-expanded="false">
                            <svg className="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
                                <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 1h15M1 7h15M1 13h15"/>
                            </svg>
                        </button>
                    </div> */}
                    <div className="flex justify-center items-center gap-2">
                        <Link to="/cart" className="relative rounded-full">
                            <MdOutlineShoppingCart size={32} color="#2b2b2b" />
                            {numCartItems > 0 && (
                            <span
                                className="absolute -top-2 -right-2 bg-orange-200 text-gray-800 rounded-full text-xs min-w-[22px] h-[22px] flex items-center justify-center shadow font-bold px-1 border border-white"
                                style={{ lineHeight: "22px" }}
                            >
                                {numCartItems}
                            </span>
                            )}
                        </Link>
                        {totalValue > 0 && (
                            <span className="text-base font-semibold text-[#2b2b2b] px-3 py-1">
                            {totalValue} zł <span className="text-sm text-orange-300">/ brutto</span>
                            </span>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default Navbar