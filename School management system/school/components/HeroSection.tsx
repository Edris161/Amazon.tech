interface HeroProps {
  title: string;
  subtitle: string;
  ctaText: string;
  ctaLink: string;
  backgroundImage: string;
}

export default function HeroSection({ title, subtitle, ctaText, ctaLink, backgroundImage }: HeroProps) {
  return (
    <section
      className="h-[80vh] flex items-center justify-center text-white"
      style={{
        background: `url(${backgroundImage}) center/cover no-repeat`,
      }}
    >
      <div className="text-center bg-black/40 p-6 rounded-lg">
        <h1 className="text-4xl font-bold mb-4">{title}</h1>
        <p className="mb-6">{subtitle}</p>
        <a href={ctaLink} className="bg-primary px-6 py-3 rounded-lg hover:bg-blue-700">
          {ctaText}
        </a>
      </div>
    </section>
  );
}