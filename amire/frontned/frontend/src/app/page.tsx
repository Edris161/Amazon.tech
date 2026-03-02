import { fetchAPI } from "@/lib/api";
import Link from "next/link";

export default async function HomePage() {
  const categories = await fetchAPI("/categories/");

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold mb-6">Categories</h1>

      <div className="grid grid-cols-3 gap-6">
        {categories.map((category: any) => (
          <Link
            key={category.id}
            href={`/categories/${category.slug}`}
            className="border p-4 rounded-lg shadow hover:shadow-lg transition"
          >
            <h2 className="text-xl font-semibold">
              {category.name}
            </h2>
          </Link>
        ))}
      </div>
    </div>
  );
}