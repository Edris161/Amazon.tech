

const SearchFilter = () => {
  return (
      <div className="h-[48px] lg:h-[64] flex items-center justify-between border rounded-full">
      <div className="hidden lg:block"> 
        <div className="flex flex-row items-center justify-between">
           <div className=" cursor-pointer w-[250px] h-[48px] lg:h-[64] px-8 flex flex-col justify-center rounded-full hover:bg-gray-100">
                <p className=" text-xs font-semibold">Where</p>
                <p className="text-sm">Search destinations</p>
            </div>
            <div className="cursor-pointer h-[48px] lg:h-[64] px-8 flex flex-col justify-center rounded-full hover:bg-gray-100">
                <p className=" text-xs font-semibold">Check in</p>
                <p className="text-sm">Add dates </p>
            </div>
            <div className="cursor-pointer h-[48px] lg:h-[64] px-8 flex flex-col justify-center rounded-full hover:bg-gray-100">
                <p className=" text-xs font-semibold">Check out</p>
                <p className="text-sm">Add dates </p>
            </div>
            <div className="cursor-pointer h-[48px] lg:h-[64] px-8 flex flex-col justify-center rounded-full hover:bg-gray-100">
                <p className=" text-xs font-semibold">Guests</p>
                <p className="text-sm">Add guests</p>
            </div>
             
             
        </div>
      </div>
      <div className="p-2">
        <div className="cursor-pointer p-2 lg:p-4 bg-red-400 rounded-full hover:bg-red-500 transition duration-200 text-white">
          <svg viewBox="0 0 32 32" 
           style={{display:'block',fill:'none',height:'16px',width:'16px',stroke:'currentColor',strokeWidth:'4',overflow:'visible'}}
            aria-hidden="true" role="presentation" focusable="false">
              <path d="m20.666 20.666 10 10"></path><path d="m24.0002 12.6668c0 6.2593-5.0741 11.3334-11.3334 11.3334-6.2592 0-11.3333-5.0741-11.3333-11.3334 0-6.2592 5.0741-11.3333 11.3333-11.3333 6.2593 0 11.3334 5.0741 11.3334 11.3333z"
               fill="none">
                </path>
                </svg>
        </div>
      </div>
      </div>
  )
}

export default SearchFilter