import React from 'react'
import Image from 'next/image'
import ReservationSidebar from '@/app/components/properties/ReservationSidebar'

const PropertyDetailPage = () => {
  return (
    <main className='max-w-[1500px] mx-auto px-6 pb-6'>
       <div className='w-full h-[64vh] mb-4 overflow-hidden rounded-xl relative'>
        <Image
          src={'/pic1.jpg'}
          className='object-cover w-full h-full '
          alt='beach house'
          width={400}
          height={24}
        />
       </div>
       <div className=' grid gird-cols-1 md:grid-cols-5 gap-4'>
          <div className='py-6 pr-6 col-span-3'>

           <h1 className='mb-4 text-4xl'>Property name</h1>

           <span className='mb-6 block text-lg text-gray-600'>
            4-guests - 2-bedrooms- 1-bathroom
           </span>
           <hr />
           <div className='py-6 flex items-center space-x-4'>
            <Image
            src='/edris.jpg'
            width={50}
            height={50}
            className='rounded-full' 
            alt='profile'
            />
            
            <p><strong>John Doe</strong> is your host</p>
            <hr />
            <p className='mt-6 text-lg'>
              Lorem ipsum dolor sit amet consectetur 
              adipisicing elit. Repellendus, reprehenderit 
              nesciunt odit dolores dolorem eaque fugit 
              
             dolorum, ipsum laboriosam minus itaque con
              sequuntur non! Accusamus architecto 
              dolores, aliquid expedita deleniti nulla.

            </p>
           </div>
          </div>
          <div>
           <ReservationSidebar />
          </div>
       </div>
    </main>
    
  )
}

export default PropertyDetailPage