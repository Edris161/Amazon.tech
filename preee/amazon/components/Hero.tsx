import Image from 'next/image';

export default function HeroSection() {
  return (
    <section className="relative h-[80vh] min-h-[600px] w-full overflow-hidden bg-black text-white">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 z-0">
        <Image
          src="/hero.jpg" // Replace witheroh your image path
          alt="Construction Site"
          fill
          className="object-cover opacity-60" // Adjust opacity for text readability
          priority
        />
        {/* Gradient overlay for better text contrast */}
        <div className="absolute inset-0 bg-gradient-to-r from-black/70 to-transparent" />
      </div>

      {/* Hero Content */}
      <div className="container relative z-10 mx-auto flex h-full flex-col justify-center px-6 lg:px-12">
        <div className="max-w-2xl">
          <span className="mb-4 inline-block font-semibold uppercase tracking-wider text-orange-500">
            Professional Construction
          </span>
          <h1 className="mb-6 text-5xl font-bold leading-tight md:text-7xl">
            Building the Future with <span className="italic text-gray-300">Precision and Power</span>
          </h1>
          <p className="mb-8 text-lg text-gray-300 md:text-xl">
            From ground-breaking to completion, we provide the industrial solutions your project deserves.
          </p>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-4">
            <button className="rounded bg-orange-600 px-8 py-4 font-bold transition hover:bg-orange-700">
              Discover +
            </button>
            <button className="rounded border-2 border-white px-8 py-4 font-bold transition hover:bg-white hover:text-black">
              Get in Touch
            </button>
          </div>

          {/* Trust Indicators (Stars & Experience) */}
          <div className="mt-10 flex items-center gap-4">
            <div className="flex text-yellow-500">
              {[...Array(5)].map((_, i) => (
                <span key={i}>★</span>
              ))}
            </div>
            <div>
              <p className="text-2xl font-bold">2000+</p>
              <p className="text-sm text-gray-400">Satisfied Customers</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
