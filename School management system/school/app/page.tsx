import HeroSection from "../components/HeroSection";
import Card from "../components/Card";

export default function HomePage() {
  return (
    <div>
      <HeroSection
        title="Welcome to ABC International School"
        subtitle="Excellence in Education Since 1990"
        ctaText="Admissions"
        ctaLink="/admissions"
        backgroundImage="/images/hero.jpg"
      />

      <section className="container mx-auto my-12">
        <h2 className="text-3xl font-bold mb-6">Why Choose Us</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card title="Experienced Teachers" description="Our teachers are highly qualified." />
          <Card title="Modern Curriculum" description="Updated curriculum for 21st century skills." />
          <Card title="Safe Environment" description="We provide a secure and friendly campus." />
        </div>
      </section>
    </div>
  );
}