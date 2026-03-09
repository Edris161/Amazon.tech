import {
  Factory,
  Construction,
  Building2,
  Settings,
  Truck,
  Wrench
} from "lucide-react";

const services = [
  {
    title: "Industrial Manufacturing",
    description:
      "High-quality manufacturing solutions designed for efficiency, durability, and modern industrial standards.",
    icon: <Factory size={32} />
  },
  {
    title: "Construction Engineering",
    description:
      "Professional construction services delivering reliable infrastructure and structural excellence.",
    icon: <Construction size={32} />
  },
  {
    title: "Building Solutions",
    description:
      "Innovative building systems tailored for commercial and industrial environments.",
    icon: <Building2 size={32} />
  },
  {
    title: "Technical Maintenance",
    description:
      "Advanced maintenance services to ensure equipment reliability and operational continuity.",
    icon: <Settings size={32} />
  },
  {
    title: "Industrial Logistics",
    description:
      "Efficient transport and logistics services to support large-scale industrial operations.",
    icon: <Truck size={32} />
  },
  {
    title: "Equipment Repair",
    description:
      "Professional repair services for industrial machines and heavy equipment.",
    icon: <Wrench size={32} />
  }
];

export default function ServicesSection() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-6 text-center">
        <div className="max-w-3xl mx-auto mb-16">
          <h2 className="text-4xl font-bold text-slate-900 mb-4">
            Our Industrial Services
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <div
              key={index}
              className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
            >
              <div className="mb-6 flex justify-center">
                <div className="p-4 bg-orange-50 rounded-lg text-orange-600">
                  {service.icon}
                </div>
              </div>

              <h3 className="text-xl font-bold text-slate-900 mb-3">
                {service.title}
              </h3>

              <p className="text-gray-600 text-sm leading-relaxed mb-6">
                {service.description}
              </p>

              <button className="text-orange-600 font-bold text-sm uppercase tracking-wider">
                Read More →
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}