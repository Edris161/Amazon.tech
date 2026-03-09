import Image from 'next/image';
import { Check } from 'lucide-react';

export default function AboutSection() {
  return (
    <section className="py-16 md:py-24 bg-white">
      <div className="container mx-auto px-6 lg:px-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          {/* Left Column: Text Content */}
          <div className="space-y-6">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 leading-tight">
              Built on Integrity, <br />
              <span className="text-orange-600">Engineered for Progress</span>
            </h2>
            
            <p className="text-gray-600 leading-relaxed max-w-lg">
              With decades of experience in heavy construction, we combine cutting-edge 
              technology with solid workmanship. Our mission is to deliver infrastructure 
              solutions that are durable, efficient, and always within budget.
            </p>

            <ul className="space-y-4">
              {[
                "Industry-Proven Capabilities",
                "Safety-First Approach",
                "Tailored End-to-End Solutions"
              ].map((item, index) => (
                <li key={index} className="flex items-center gap-3 font-medium text-slate-800">
                  <div className="bg-orange-100 p-1 rounded-full">
                    <Check className="w-4 h-4 text-orange-600 stroke-[3px]" />
                  </div>
                  {item}
                </li>
              ))}
            </ul>
          </div>

          {/* Right Column: Overlapping Image Collage */}
          <div className="relative h-[400px] md:h-[500px]">
            {/* Top/Back Image */}
            <div className="absolute top-0 right-0 w-[80%] h-[70%] overflow-hidden rounded-xl shadow-2xl">
              <Image
                src="/pic4.jpg" // Replace with your image
                alt="High-rise construction"
                fill
                className="object-cover"
              />
            </div>

            {/* Bottom/Front Image (Overlapping) */}
            <div className="absolute bottom-0 left-0 w-[60%] h-[60%] overflow-hidden rounded-xl border-8 border-white shadow-2xl z-10">
              <Image
                src="/pic3.jpg" // Replace with your image
                alt="Construction detail"
                fill
                className="object-cover"
              />
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
