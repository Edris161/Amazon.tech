import AboutSection from '@/components/About'
import CtaBanner from '@/components/CtaBanner'
import FaqSection from '@/components/Faq'
import HeroSection from '@/components/Hero'
import ServicesSection from '@/components/Services'
import TeamSection from '@/components/Team'
import React from 'react'

const page = () => {
  return (
    <div>
      <HeroSection />
      <AboutSection />
      <ServicesSection /> 
      <FaqSection />
      <TeamSection  />
      <CtaBanner />
    </div>
  )
}

export default page