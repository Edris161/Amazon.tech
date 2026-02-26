
import Image from 'next/image'
const PropertiesListitem = () => {
  return (
    <div className='cursor-pointer'>
      <div className='overflow-hidden aspect-square rounded-xl'>
        <Image
         
         src="/pic1.jpg"
         sizes='( max-width: 768px) 768px, (max-width: 1200px) 768px, 768px'
         className='hover:scale-110 object-cover transition h-full w-full'
         alt="House" 
         height={'20'}
         width={'20'}
         
        />
      </div>
      <div className='mt-2 '>
        <p className='text-lg font-bold'>Property Name</p>
      </div>
      <div className='mt-2'>
          <p className='text-sm text-gray-500'><strong>$200</strong></p>
      </div>
    </div>
  )
}

export default PropertiesListitem