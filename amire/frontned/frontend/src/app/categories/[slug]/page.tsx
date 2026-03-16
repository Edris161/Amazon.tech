import { fetchAPI } from "@/lib/api";
import Link from "next/link";

interface Props {
  params: {
    slug: string;
  };
}

export default async function CategoryPage({ params }: Props) {
  const slug = params.slug;

  // Fetch category
  const category = await fetchAPI(`/categories/${slug}/`);

  // Fetch products in this category
  const products = await fetchAPI(`/products/?category__slug=${slug}`);

  return (
    <div className="p-10">
      <h1 className="text-3xl font-bold mb-8">
        {category.name}
      </h1>

      {products.length === 0 ? (
        <p>No products found in this category.</p>
      ) : (
        <div className="grid grid-cols-3 gap-6">
          {products.map((product: any) => (
            <Link
              key={product.id}
              href={`/products/${product.slug}`}
              className="border p-4 rounded-lg shadow hover:shadow-lg transition"
            >
              <img
                src={product.image}
                alt={product.name}
                className="h-40 w-full object-cover mb-4"
              />

              <h2 className="text-xl font-semibold">
                {product.name}
              </h2>

              <p className="text-gray-600">
                {product.company_name}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}