import { PhoneCall } from 'lucide-react';

export default function CtaBanner() {
  return (
    <section className="py-12 md:py-20 px-6">
      <div className="container mx-auto">
        {/* Main Banner Container with Gradient */}
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-orange-600 to-red-500 py-16 px-8 text-center text-white shadow-2xl">
          
          {/* Subtle Decorative Circle Overlay */}
          <div className="absolute top-0 left-0 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
          
          <div className="relative z-10 max-w-3xl mx-auto">
            {/* Header */}
            <h2 className="text-3xl md:text-5xl font-bold mb-6 leading-tight">
              Building Your Vision, <br />
              One Project at a Time
            </h2>
            
            {/* Subtext */}
            <p className="text-orange-50 text-lg md:text-xl mb-10 opacity-90">
              Ready to start your next industrial project? Our team is standing by 
              to provide a comprehensive quote and expert consultation.
            </p>

            {/* CTA Button */}
            <button className="inline-flex items-center gap-3 bg-white text-orange-600 px-8 py-4 rounded-full font-bold text-lg hover:bg-orange-50 transition-all hover:scale-105 shadow-lg group">
              <PhoneCall className="w-5 h-5 transition-transform group-hover:rotate-12" />
              <span>+91 123 456 7890</span>
            </button>
          </div>

          {/* Bottom Decorative Circle */}
          <div className="absolute bottom-0 right-0 translate-x-1/3 translate-y-1/3 w-96 h-96 bg-black/10 rounded-full blur-3xl" />
        </div>
      </div>
    </section>
  );
}
