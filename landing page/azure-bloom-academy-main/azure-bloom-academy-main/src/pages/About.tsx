import { Target, Eye, Award, Quote } from "lucide-react";
import GlassCard from "@/components/GlassCard";
import SectionTitle from "@/components/SectionTitle";

const timeline = [
  { year: "1995", title: "School Founded", desc: "ABC International School opens with 50 students." },
  { year: "2002", title: "First Expansion", desc: "New science and technology wing added." },
  { year: "2010", title: "National Recognition", desc: "Awarded Best School in the region." },
  { year: "2018", title: "STEM Excellence", desc: "Launched advanced STEM and robotics programs." },
  { year: "2024", title: "Global Partnership", desc: "Partnered with international universities for student exchange." },
];

const achievements = [
  "National Academic Excellence Award 2024",
  "100% College Placement Rate",
  "15 National Science Olympiad Winners",
  "Best Sports Program Award 2023",
  "Green School Certification",
  "International Debate Champions",
];

const About = () => (
  <div className="min-h-screen pt-24">
    {/* Hero */}
    <section className="container mx-auto px-4 py-16">
      <SectionTitle title="About Our School" subtitle="A legacy of excellence, innovation, and holistic education since 1995" />
    </section>

    {/* History */}
    <section className="container mx-auto px-4 py-12">
      <div className="grid md:grid-cols-2 gap-12 items-center">
        <div>
          <h3 className="text-2xl font-heading font-bold mb-4">Our Story</h3>
          <p className="text-muted-foreground leading-relaxed mb-4">
            Founded in 1995 by visionary educators, ABC International School began with a simple mission: to provide world-class education accessible to all. Starting with just 50 students and 5 teachers, we have grown into one of the most respected educational institutions in the country.
          </p>
          <p className="text-muted-foreground leading-relaxed">
            Today, with over 1,500 students and 120 dedicated faculty members, we continue to push the boundaries of educational excellence while maintaining the intimate, nurturing environment that has been our hallmark.
          </p>
        </div>
        <GlassCard className="p-8" hover={false}>
          <img src="https://images.unsplash.com/photo-1523050854058-8df90110c476?w=600&h=400&fit=crop" alt="School campus" className="rounded-xl w-full h-64 object-cover" />
        </GlassCard>
      </div>
    </section>

    {/* Mission & Vision */}
    <section className="container mx-auto px-4 py-16">
      <div className="grid md:grid-cols-2 gap-6">
        <GlassCard className="p-8">
          <div className="w-12 h-12 rounded-xl gradient-bg flex items-center justify-center mb-4">
            <Target className="w-6 h-6 text-primary-foreground" />
          </div>
          <h3 className="text-xl font-heading font-bold mb-3">Our Mission</h3>
          <p className="text-muted-foreground leading-relaxed">
            To empower students with knowledge, skills, and values necessary to become responsible global citizens and lifelong learners who contribute positively to society.
          </p>
        </GlassCard>
        <GlassCard className="p-8">
          <div className="w-12 h-12 rounded-xl gradient-bg flex items-center justify-center mb-4">
            <Eye className="w-6 h-6 text-primary-foreground" />
          </div>
          <h3 className="text-xl font-heading font-bold mb-3">Our Vision</h3>
          <p className="text-muted-foreground leading-relaxed">
            To be a globally recognized institution of learning that nurtures innovation, creativity, and academic excellence while fostering character development and social responsibility.
          </p>
        </GlassCard>
      </div>
    </section>

    {/* Principal Message */}
    <section className="container mx-auto px-4 py-16">
      <GlassCard className="p-10 md:flex gap-8 items-center" hover={false}>
        <img src="https://images.unsplash.com/photo-1560250097-0b93528c311a?w=300&h=300&fit=crop" alt="Principal" className="w-40 h-40 rounded-2xl object-cover shrink-0 mb-6 md:mb-0" />
        <div>
          <Quote className="w-8 h-8 text-primary mb-3 opacity-50" />
          <p className="text-muted-foreground leading-relaxed italic mb-4">
            "Education is not just about academics; it's about nurturing the whole child. At ABC International, we create an environment where every student feels valued, challenged, and inspired to reach their highest potential."
          </p>
          <p className="font-heading font-semibold">Dr. William Harrison</p>
          <p className="text-sm text-muted-foreground">Principal, ABC International School</p>
        </div>
      </GlassCard>
    </section>

    {/* Timeline */}
    <section className="container mx-auto px-4 py-16">
      <SectionTitle title="Our Journey" subtitle="Milestones that define our legacy" />
      <div className="relative max-w-2xl mx-auto">
        <div className="absolute left-4 md:left-1/2 top-0 bottom-0 w-0.5 gradient-bg" />
        {timeline.map((item, i) => (
          <div key={item.year} className={`relative flex items-start mb-10 ${i % 2 === 0 ? "md:flex-row" : "md:flex-row-reverse"}`}>
            <div className="absolute left-4 md:left-1/2 -translate-x-1/2 w-4 h-4 rounded-full gradient-bg border-4 border-background z-10" />
            <div className={`ml-12 md:ml-0 md:w-[calc(50%-2rem)] ${i % 2 === 0 ? "md:pr-8 md:text-right" : "md:pl-8"}`}>
              <GlassCard className="p-5">
                <span className="text-sm font-bold gradient-text">{item.year}</span>
                <h4 className="font-heading font-semibold mt-1">{item.title}</h4>
                <p className="text-sm text-muted-foreground mt-1">{item.desc}</p>
              </GlassCard>
            </div>
          </div>
        ))}
      </div>
    </section>

    {/* Achievements */}
    <section className="container mx-auto px-4 py-16">
      <SectionTitle title="Our Achievements" subtitle="Recognition of our commitment to excellence" />
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 max-w-4xl mx-auto">
        {achievements.map((a) => (
          <GlassCard key={a} className="p-5 flex items-center gap-3">
            <Award className="w-5 h-5 text-primary shrink-0" />
            <span className="text-sm font-medium">{a}</span>
          </GlassCard>
        ))}
      </div>
    </section>
  </div>
);

export default About;
