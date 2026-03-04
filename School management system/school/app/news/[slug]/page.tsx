"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import api from "../../../lib/api";

interface NewsItem {
  id: number;
  title: string;
  content: string;
  image: string;
  date: string;
}

export default function NewsDetailPage() {
  const { slug } = useParams();
  const [news, setNews] = useState<NewsItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`news/${slug}/`)
      .then(res => {
        setNews(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching news detail:", err);
        setLoading(false);
      });
  }, [slug]);

  if (loading) return <p className="text-center mt-12">Loading news...</p>;
  if (!news) return <p className="text-center mt-12">News not found.</p>;

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-4">{news.title}</h1>
      <p className="text-gray-400 text-sm mb-4">{new Date(news.date).toLocaleDateString()}</p>
      <img
        src={news.image || "/images/news-placeholder.jpg"}
        alt={news.title}
        className="w-full h-64 object-cover rounded-lg mb-6"
      />
      <div className="text-gray-700 leading-relaxed">{news.content}</div>
    </div>
  );
}