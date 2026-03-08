import { Link, useParams } from "react-router-dom";
import { Calendar, ArrowLeft, ArrowRight } from "lucide-react";
import { useEffect, useState } from "react";
import GlassCard from "@/components/GlassCard";
import SectionTitle from "@/components/SectionTitle";

const NewsDetail = () => {
  const { slug } = useParams();
  const [article, setArticle] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/news/")
      .then((res) => res.json())
      .then((data) => {
        const results = data.results ? data.results : data;
        const found = results.find((n: any) => n.slug === slug);
        setArticle(found);
      })
      .catch((error) => console.error("Error fetching news:", error));
  }, [slug]);

  if (!article)
    return (
      <div className="min-h-screen pt-24 text-center py-40">
        Article not found.
      </div>
    );

  return (
    <div className="min-h-screen pt-24">
      <article className="container mx-auto px-4 py-16 max-w-3xl">
        <Link
          to="/news"
          className="inline-flex items-center gap-2 text-primary font-medium mb-6 hover:gap-3 transition-all"
        >
          <ArrowLeft className="w-4 h-4" /> Back to News
        </Link>

        <GlassCard className="overflow-hidden" hover={false}>
          <img
            src={article.image}
            alt={article.title}
            className="w-full h-72 object-cover"
          />

          <div className="p-8">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-xs font-medium gradient-bg text-primary-foreground px-3 py-1 rounded-full">
                {article.category}
              </span>

              <span className="text-sm text-muted-foreground flex items-center gap-1">
                <Calendar className="w-3 h-3" />
                {article.date}
              </span>
            </div>

            <h1 className="text-3xl font-heading font-bold mb-4">
              {article.title}
            </h1>

            <p className="text-muted-foreground leading-relaxed">
              {article.excerpt}
            </p>
          </div>
        </GlassCard>
      </article>
    </div>
  );
};

const News = () => {
  const [newsItems, setNewsItems] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/news/")
      .then((res) => res.json())
      .then((data) => {
        const results = data.results ? data.results : data;
        setNewsItems(results);
      })
      .catch((error) => console.error("Error fetching news:", error));
  }, []);

  return (
    <div className="min-h-screen pt-24">
      <section className="container mx-auto px-4 py-16">
        <SectionTitle
          title="School News"
          subtitle="Stay updated with the latest happenings at ABC International"
        />

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {newsItems.map((news: any) => (
            <Link key={news.slug} to={`/news/${news.slug}`}>
              <GlassCard className="overflow-hidden group h-full">
                <div className="h-48 overflow-hidden">
                  <img
                    src={news.image}
                    alt={news.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                </div>

                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xs font-medium gradient-bg text-primary-foreground px-2.5 py-1 rounded-full">
                      {news.category}
                    </span>

                    <span className="text-xs text-muted-foreground flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {news.date}
                    </span>
                  </div>

                  <h3 className="font-heading font-semibold mb-2 group-hover:text-primary transition-colors">
                    {news.title}
                  </h3>

                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {news.excerpt}
                  </p>

                  <span className="inline-flex items-center gap-1 text-sm text-primary font-medium mt-3">
                    Read More <ArrowRight className="w-3 h-3" />
                  </span>
                </div>
              </GlassCard>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
};

export { NewsDetail };
export default News;