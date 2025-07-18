import React from 'react'

const PlaceHolder = () => {
  return (
    <div role="status" className="space-y-8 animate-pulse md:space-y-0 md:space-x-8 rtl:space-x-reverse md:flex md:items-center">
        <div className="flex items-center justify-center w-40 h-40 bg-gray-300 rounded-sm sm:w-96 dark:bg-gray-400 ">
            <svg className="w-10 h-10 text-gray-200 dark:text-gray-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
            </svg>
        </div>
        <div className="w-full">
            <div className="h-4 bg-gray-200 rounded-full dark:bg-gray-400 w-48 mb-4"></div>
            <div className="h-2 bg-gray-200 rounded-full dark:bg-gray-400 w-24 mb-3"></div>
            <div className="h-2 bg-gray-200 rounded-full dark:bg-gray-400 mb-3"></div>
            <div className="h-2 bg-gray-200 rounded-full dark:bg-gray-400 max-w-[440px] mb-3"></div>
            <div className="h-2 bg-gray-200 rounded-full dark:bg-gray-400 max-w-[460px] mb-3"></div>
            <div className="h-2 bg-gray-200 rounded-full dark:bg-gray-400 max-w-[360px]"></div>
            <div className="mt-5 flex items-end justify-between">
                <div className="h-3 bg-gray-200 rounded-full dark:bg-gray-400 w-16"></div>
                <div className="h-4 bg-gray-200 rounded-full dark:bg-gray-400 w-16"></div>
            </div>
        </div>
    </div>
  )
}

export default PlaceHolder