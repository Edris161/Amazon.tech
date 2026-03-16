import AboutSection from '@/components/About'
import CtaBanner from '@/components/CtaBanner'
import FaqSection from '@/components/Faq'
import Footer from '@/components/Footer'
import HeroSection from '@/components/Hero'
import ServicesSection from '@/components/Services'
import TeamSection from '@/components/Team'
import Navbar from '@/components/Navbar'

const page = () => {
  return (
    <div>
      <Navbar />    
      <HeroSection />
      <AboutSection />
      <ServicesSection /> 
      <FaqSection />
      <TeamSection  />
      <CtaBanner />
      <Footer />
    </div>
  )
}

export default page