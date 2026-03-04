"use client";

import { useEffect, useState } from "react";
import SectionTitle from "../../components/SectionTitle";
import Link from "next/link";
import api from "../../lib/api";

interface NewsItem {
  id: number;
  title: string;
  slug: string;
  summary: string;
  image: string;
  date: string;
}

export default function NewsPage() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("news/")
      .then((res) => {
        console.log(res.data);
        setNews(Array.isArray(res.data) ? res.data : res.data.results);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching news:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="text-center mt-12">Loading news...</p>;
  if (news.length === 0) return <p className="text-center mt-12">No news found.</p>;

  return (
    <div className="container mx-auto px-4 py-12">
      <SectionTitle title="Latest News" />

      <div className="grid md:grid-cols-3 gap-8 mt-8">
        {news.map((item) => (
          <Link
            key={item.id}
            href={`/news/${item.slug}`}
            className="bg-white shadow-md rounded-lg overflow-hidden hover:shadow-xl transition"
          >
            <img
              src={item.image || "/images/news-placeholder.jpg"}
              alt={item.title}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <h3 className="font-bold text-lg">{item.title}</h3>
              <p className="text-gray-600 text-sm mt-2">{item.summary}</p>
              <p className="text-gray-400 text-xs mt-2">{new Date(item.date).toLocaleDateString()}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}