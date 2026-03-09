"use client"; // Required for interactivity (useState)
import { useState } from 'react';
import { Plus, Minus } from 'lucide-react';
import Image from 'next/image';

const faqData = [
  {
    question: "What Makes Your Company Different From General Contractors?",
    answer: "We specialize specifically in heavy industrial construction. Unlike general contractors, we own our heavy machinery and have in-house specialized engineering teams for complex structural work."
  },
  {
    question: "How Do You Ensure Projects Stay On Schedule?",
    answer: "We utilize advanced BIM (Building Information Modeling) and real-time project tracking to identify potential bottlenecks before they cause delays."
  },
  {
    question: "What Safety Standards Do You Follow?",
    answer: "Our team strictly adheres to OSHA and ISO 45001 standards. Safety is our top priority, with mandatory daily briefings and site safety audits."
  },
  {
    question: "Can You Work On Operational Facilities Without Shutdowns?",
    answer: "Yes, we specialize in 'live site' construction, implementing phased workflows that allow your production to continue while we build."
  },
  {
    question: "What Warranty Do You Provide On Industrial Builds?",
    answer: "We offer an industry-leading 10-year structural warranty and a comprehensive 2-year maintenance guarantee on all systems installed."
  }
];

export default function FaqSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-6 lg:px-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
          
          {/* Left Column: Accordion */}
          <div className="space-y-4">
            {faqData.map((item, index) => (
              <div key={index} className="border-b border-gray-200">
                <button
                  onClick={() => setOpenIndex(openIndex === index ? null : index)}
                  className="w-full flex justify-between items-center py-6 text-left hover:text-orange-600 transition-colors"
                >
                  <span className="text-lg font-bold text-slate-900 leading-tight">
                    {item.question}
                  </span>
                  <span className="ml-4 flex-shrink-0">
                    {openIndex === index ? (
                      <Minus className="w-5 h-5 text-orange-600" />
                    ) : (
                      <Plus className="w-5 h-5 text-gray-400" />
                    )}
                  </span>
                </button>
                
                {/* Answer with smooth transition */}
                <div 
                  className={`overflow-hidden transition-all duration-300 ease-in-out ${
                    openIndex === index ? 'max-h-40 pb-6' : 'max-h-0'
                  }`}
                >
                  <p className="text-gray-600 leading-relaxed">
                    {item.answer}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Right Column: Content & Image */}
          <div className="space-y-8">
            <div>
              <h2 className="text-4xl font-bold text-slate-900 mb-6">
                Industrial Expertise — <br />
                <span className="text-orange-600">Your Questions, Answered</span>
              </h2>
              <p className="text-gray-600 text-lg leading-relaxed">
                Every project involves complex decisions. From safety protocols to 
                logistics, we maintain transparent communication methods so you 
                know exactly what’s happening on site at all times.
              </p>
            </div>

            <div className="relative h-64 md:h-80 w-full overflow-hidden rounded-2xl shadow-xl">
              <Image
                src="/pic1.jpg" // Replace with your actual image path
                alt="Welding at industrial site"
                fill
                className="object-cover"
              />
              {/* Blueish Overlay to match the image vibe */}
              <div className="absolute inset-0 bg-blue-900/10 mix-blend-multiply" />
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
