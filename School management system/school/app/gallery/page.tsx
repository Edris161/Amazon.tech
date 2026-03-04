"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

interface GalleryImage {
  id: number;
  image: string;
}

export default function GalleryPage() {
  const [images, setImages] = useState<GalleryImage[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchImages = async () => {
      try {
        const response = await api.get("gallery/");

        // 🔥 THIS FIXES EVERYTHING
        const data = Array.isArray(response.data)
          ? response.data
          : response.data.results;

        setImages(data || []);
      } catch (error) {
        console.error("Gallery error:", error);
        setImages([]); // prevent crash
      } finally {
        setLoading(false);
      }
    };

    fetchImages();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6">
        {images.length > 0 ? (
          images.map((img) => (
            <div key={img.id}>
              <img
                src={img.image}
                alt="Gallery"
                className="w-full h-48 object-cover rounded-lg"
              />
            </div>
          ))
        ) : (
          <p>No images found.</p>
        )}
      </div>
    </div>
  );
}