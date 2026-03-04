import Card from "../../components/Card";
import SectionTitle from "../../components/SectionTitle";

export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-12 space-y-16">

      {/* School History */}
      <section>
        <SectionTitle title="Our History" />
        <p className="text-gray-700 leading-relaxed mt-4">
          ABC International School was founded in 1990 with the mission to provide quality education to students from diverse backgrounds. 
          Over the past 30 years, we have grown into a leading institution recognized for academic excellence and holistic development.
        </p>
      </section>

      {/* Mission & Vision */}
      <section className="grid md:grid-cols-2 gap-8">
        <div className="bg-white shadow-md rounded-lg p-6">
          <h3 className="font-bold text-xl mb-4">Our Mission</h3>
          <p className="text-gray-700">
            To nurture young minds by providing an environment that fosters creativity, critical thinking, and lifelong learning.
          </p>
        </div>
        <div className="bg-white shadow-md rounded-lg p-6">
          <h3 className="font-bold text-xl mb-4">Our Vision</h3>
          <p className="text-gray-700">
            To be a world-class institution where students excel academically, socially, and emotionally, preparing them to face global challenges.
          </p>
        </div>
      </section>

      {/* Principal Message */}
      <section className="flex flex-col md:flex-row items-center gap-8">
        <img 
          src="/images/principal.jpg" 
          alt="Principal" 
          className="w-64 h-64 object-cover rounded-full shadow-lg"
        />
        <div>
          <SectionTitle title="Message from Principal" />
          <p className="text-gray-700 mt-4">
            Welcome to ABC International School! Our commitment is to inspire every student to achieve their full potential. 
            We focus on excellence in academics, creativity, and character development, ensuring a balanced and thriving learning environment.
          </p>
        </div>
      </section>

      {/* Achievements */}
      <section>
        <SectionTitle title="Our Achievements" />
        <div className="grid md:grid-cols-3 gap-6 mt-6">
          <Card title="100+ Awards" description="Recognized nationally for academic excellence." />
          <Card title="30+ Years" description="Providing quality education since 1990." />
          <Card title="5000+ Graduates" description="Our alumni are successful across the globe." />
        </div>
      </section>

      {/* Timeline */}
      <section>
        <SectionTitle title="Our Journey" />
        <div className="relative border-l-2 border-blue-500 mt-6 ml-4">
          <TimelineItem year="1990" description="ABC International School was founded." />
          <TimelineItem year="2000" description="Introduced new science and technology programs." />
          <TimelineItem year="2010" description="Opened modern library and sports complex." />
          <TimelineItem year="2020" description="Celebrated 30 years of excellence in education." />
        </div>
      </section>
    </div>
  );
}

// Timeline Item Component
interface TimelineItemProps {
  year: string;
  description: string;
}

function TimelineItem({ year, description }: TimelineItemProps) {
  return (
    <div className="mb-8 ml-4 relative">
      <div className="absolute -left-6 w-4 h-4 bg-blue-500 rounded-full top-2"></div>
      <p className="font-bold">{year}</p>
      <p className="text-gray-700">{description}</p>
    </div>
  );
}