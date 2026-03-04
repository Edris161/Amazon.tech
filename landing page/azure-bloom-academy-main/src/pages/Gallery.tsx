import { useState } from "react";
import { X } from "lucide-react";
import GlassCard from "@/components/GlassCard";
import SectionTitle from "@/components/SectionTitle";
import { galleryImages } from "@/lib/data";

const categories = ["All", ...new Set(galleryImages.map((img) => img.category))];

const Gallery = () => {
  const [filter, setFilter] = useState("All");
  const [lightbox, setLightbox] = useState<string | null>(null);

  const filtered = filter === "All" ? galleryImages : galleryImages.filter((img) => img.category === filter);

  return (
    <div className="min-h-screen pt-24">
      <section className="container mx-auto px-4 py-16">
        <SectionTitle title="Gallery" subtitle="Capturing moments of learning, growth, and joy" />

        {/* Filters */}
        <div className="flex flex-wrap justify-center gap-2 mb-10">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                filter === cat ? "gradient-bg text-primary-foreground" : "glass hover:bg-secondary"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((img) => (
            <GlassCard key={img.id} className="overflow-hidden cursor-pointer group" onClick={() => setLightbox(img.src)}>
              <div className="h-56 overflow-hidden">
                <img src={img.src} alt={img.alt} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
              </div>
              <div className="p-4">
                <span className="text-xs font-medium text-muted-foreground">{img.category}</span>
                <p className="text-sm font-medium mt-1">{img.alt}</p>
              </div>
            </GlassCard>
          ))}
        </div>
      </section>

      {/* Lightbox */}
      {lightbox && (
        <div className="fixed inset-0 z-50 bg-foreground/80 backdrop-blur-sm flex items-center justify-center p-4" onClick={() => setLightbox(null)}>
          <button className="absolute top-6 right-6 text-background" onClick={() => setLightbox(null)}>
            <X className="w-8 h-8" />
          </button>
          <img src={lightbox} alt="" className="max-w-full max-h-[85vh] rounded-2xl shadow-2xl animate-scale-in" onClick={(e) => e.stopPropagation()} />
        </div>
      )}
    </div>
  );
};

export default Gallery;
