import Link from "next/link"
import Image from "next/image"
import SearchFilter from "./SearchFilter"
 
const Navbar = () => {
  return (
   <nav className="w-full fixed top-0 left-0 py-6 bg-white border-b z-10">
    <div className="max-w-[1500px] mx-auto px-6 ">
      <div className="flex justify-between items-center">
        <Link href='/'>
          <Image src="/airbnb.png" alt="logo" width={180} height={38} />
        </Link>
        <div className="flex space-x-6">
              <SearchFilter />
        </div>
        <div className="flex items-center space-x-6">
             add propertye 
        </div>
      </div>
    </div>
   </nav>
  )
}

export default Navbar 