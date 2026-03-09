import Image from "next/image";
import { Facebook, Twitter, Instagram } from "lucide-react";

const teamMembers = [
  {
    name: "Michael Carter",
    role: "Chief Industrial Engineer",
    image: "/PIC.jpeg",
  },
  {
    name: "Sarah Johnson",
    role: "Construction Project Manager",
    image: "/PIC.jpeg",
  },
  {
    name: "David Williams",
    role: "Mechanical Systems Specialist",
    image: "/PIC.jpeg",
  },
];

export default function TeamSection() {
  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-6 text-center">
        {/* Section Heading */}
        <div className="max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
            The Masterminds Behind Industrial Excellence
          </h2>
          <p className="text-gray-600">
            Meet the visionary engineers and builders who have shaped the most robust environments.
          </p>
        </div>

        {/* Team Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
          {teamMembers.map((member, index) => (
            <div key={index} className="flex flex-col items-center group">
              
              {/* Image Container */}
              <div className="relative w-full aspect-[4/3] mb-6 overflow-hidden rounded-xl bg-gray-100">
                <Image
                  src={member.image}
                  alt={member.name}
                  fill
                  className="object-cover transition-transform duration-500 group-hover:scale-105"
                />
              </div>

              {/* Info */}
              <h3 className="text-xl font-bold text-slate-900 mb-2">
                {member.name}
              </h3>

              <p className="text-sm text-gray-500 mb-6 max-w-[280px]">
                {member.role}
              </p>

              {/* Social Links */}
              <div className="flex gap-4">
                <a
                  href="#"
                  className="p-2 bg-orange-50 rounded-full text-orange-600 hover:bg-orange-600 hover:text-white transition-colors"
                >
                  <Facebook className="w-4 h-4" />
                </a>

                <a
                  href="#"
                  className="p-2 bg-orange-50 rounded-full text-orange-600 hover:bg-orange-600 hover:text-white transition-colors"
                >
                  <Twitter className="w-4 h-4" />
                </a>

                <a
                  href="#"
                  className="p-2 bg-orange-50 rounded-full text-orange-600 hover:bg-orange-600 hover:text-white transition-colors"
                >
                  <Instagram className="w-4 h-4" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}