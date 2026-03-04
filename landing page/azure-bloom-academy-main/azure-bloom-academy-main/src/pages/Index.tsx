import { Link } from "react-router-dom";
import { ArrowRight, Award, BookOpen, Users, Star, Calendar, GraduationCap, Globe, Trophy, Heart, Clock, MapPin, Phone, Mail, ChevronRight, Play, Shield, Lightbulb, Palette } from "lucide-react";
import GlassCard from "@/components/GlassCard";
import SectionTitle from "@/components/SectionTitle";
import { newsItems, staffMembers } from "@/lib/data";
import heroImage from "@/assets/hero-school.jpg";

const highlights = [
  { icon: Award, title: "Excellence in Education", desc: "Ranked among the top 10 schools nationally for academic performance and student outcomes." },
  { icon: Users, title: "Expert Faculty", desc: "120+ highly qualified teachers with an average of 15 years of teaching experience." },
  { icon: BookOpen, title: "Holistic Development", desc: "Balanced curriculum combining academics, sports, arts, and character building." },
  { icon: Globe, title: "Global Exposure", desc: "International exchange programs with partner schools in 12 countries worldwide." },
  { icon: Shield, title: "Safe Environment", desc: "24/7 security, CCTV surveillance, and trained counselors for student wellbeing." },
  { icon: Lightbulb, title: "Modern Facilities", desc: "State-of-the-art STEM labs, smart classrooms, and a digital learning ecosystem." },
];

const programs = [
  { title: "Primary School", grades: "Grade 1-5", icon: "🧒", desc: "Building strong foundations through play-based and interactive learning.", color: "from-blue-500 to-cyan-400" },
  { title: "Middle School", grades: "Grade 6-8", icon: "📚", desc: "Developing critical thinking, creativity, and leadership skills.", color: "from-indigo-500 to-blue-400" },
  { title: "High School", grades: "Grade 9-12", icon: "🎓", desc: "Preparing students for top universities and career success.", color: "from-violet-500 to-indigo-400" },
];

const testimonials = [
  { name: "Mrs. Anita Patel", role: "Parent of Grade 10 Student", text: "ABC International has been a transformative experience for my daughter. The teachers genuinely care about each student's growth, and the environment encourages curiosity and confidence.", avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&h=100&fit=crop" },
  { name: "Rajesh Kumar", role: "Alumni, Class of 2022", text: "The foundation I received at ABC International prepared me for engineering at MIT. The STEM program and mentorship were exceptional.", avatar: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=100&h=100&fit=crop" },
  { name: "Dr. Lisa Chang", role: "Parent of Grade 7 Student", text: "What impressed me most is their focus on the whole child — academics, sports, arts, and emotional intelligence. My son loves going to school every day.", avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop" },
];

const events = [
  { date: "Mar 15", title: "Parent-Teacher Conference", desc: "Mid-term progress discussion for all grades.", time: "9:00 AM - 3:00 PM" },
  { date: "Mar 22", title: "Annual Sports Day", desc: "Inter-house athletics and team sports competition.", time: "8:00 AM - 5:00 PM" },
  { date: "Apr 5", title: "Science & Innovation Fair", desc: "Students showcase STEM projects and experiments.", time: "10:00 AM - 4:00 PM" },
  { date: "Apr 18", title: "Cultural Festival", desc: "Music, dance, drama, and art performances.", time: "5:00 PM - 9:00 PM" },
];

const partners = [
  "Cambridge Assessment", "IB World Schools", "Microsoft Education", "Google for Education", "National Geographic Learning", "British Council"
];

const Index = () => (
  <div className="min-h-screen">
    {/* Hero */}
    <section className="relative h-screen flex items-center justify-center overflow-hidden">
      <img src={heroImage} alt="ABC International School campus" className="absolute inset-0 w-full h-full object-cover" />
      <div className="absolute inset-0 hero-overlay" />
      <div className="relative z-10 text-center px-4 max-w-4xl animate-fade-in">
        <div className="glass-strong inline-block px-4 py-1.5 rounded-full mb-6">
          <span className="text-sm font-medium">🎓 Admissions Open for 2026-27</span>
        </div>
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-heading font-bold text-primary-foreground mb-6 leading-tight">
          ABC International School
        </h1>
        <p className="text-lg md:text-xl text-primary-foreground/90 mb-8 max-w-2xl mx-auto">
          Nurturing minds, shaping futures. Where every student discovers their potential and becomes a global citizen.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link to="/admissions" className="gradient-bg text-primary-foreground px-8 py-3.5 rounded-xl font-semibold hover:opacity-90 transition-opacity flex items-center gap-2">
            Apply Now <ArrowRight className="w-4 h-4" />
          </Link>
          <Link to="/contact" className="glass-strong px-8 py-3.5 rounded-xl font-semibold hover-lift">
            Contact Us
          </Link>
          <button className="glass-strong px-6 py-3.5 rounded-xl font-semibold hover-lift flex items-center gap-2">
            <Play className="w-4 h-4" /> Virtual Tour
          </button>
        </div>
      </div>
      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 rounded-full border-2 border-primary-foreground/50 flex items-start justify-center p-1.5">
          <div className="w-1.5 h-2.5 bg-primary-foreground/70 rounded-full" />
        </div>
      </div>
    </section>

    {/* Announcement Ticker */}
    <section className="gradient-bg py-3 overflow-hidden">
      <div className="flex animate-[slide_20s_linear_infinite] whitespace-nowrap gap-12 text-primary-foreground text-sm font-medium">
        {["📢 Admissions open for 2026-27 session", "🏆 Our students secured 15 gold medals at National Olympiad", "📅 Annual Sports Day on March 22nd", "🎨 Cultural Festival coming up in April", "📢 Admissions open for 2026-27 session", "🏆 Our students secured 15 gold medals at National Olympiad"].map((text, i) => (
          <span key={i} className="flex items-center gap-2">{text} <span className="opacity-50">•</span></span>
        ))}
      </div>
    </section>

    {/* Quick Stats Bar */}
    <section className="container mx-auto px-4 -mt-8 relative z-20">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { num: "1500+", label: "Students Enrolled", icon: Users },
          { num: "120+", label: "Expert Faculty", icon: GraduationCap },
          { num: "30+", label: "Years of Excellence", icon: Trophy },
          { num: "98%", label: "University Placement", icon: Award },
        ].map((stat) => (
          <GlassCard key={stat.label} className="p-5 text-center">
            <stat.icon className="w-6 h-6 text-primary mx-auto mb-2" />
            <div className="text-2xl md:text-3xl font-heading font-bold gradient-text mb-0.5">{stat.num}</div>
            <div className="text-xs text-muted-foreground">{stat.label}</div>
          </GlassCard>
        ))}
      </div>
    </section>

    {/* About Preview */}
    <section className="container mx-auto px-4 py-20">
      <div className="grid md:grid-cols-2 gap-12 items-center">
        <div>
          <SectionTitle title="Welcome to ABC International" subtitle="A legacy of excellence since 1995" center={false} />
          <p className="text-muted-foreground leading-relaxed mb-4">
            At ABC International School, we believe in providing a nurturing environment where students can thrive academically, socially, and emotionally. Our innovative curriculum and dedicated faculty ensure every child reaches their full potential.
          </p>
          <p className="text-muted-foreground leading-relaxed mb-6">
            With a student-to-teacher ratio of 15:1, personalized learning plans, and a focus on 21st-century skills, we prepare our students not just for exams, but for life.
          </p>
          <div className="flex flex-wrap gap-3 mb-6">
            {["CBSE Affiliated", "ISO Certified", "Green Campus", "Smart Classrooms"].map((tag) => (
              <span key={tag} className="text-xs font-medium bg-secondary px-3 py-1.5 rounded-full">{tag}</span>
            ))}
          </div>
          <Link to="/about" className="inline-flex items-center gap-2 gradient-bg text-primary-foreground px-6 py-3 rounded-xl font-semibold hover:opacity-90 transition-opacity">
            Learn More About Us <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
        <div className="relative">
          <GlassCard className="p-3 overflow-hidden" hover={false}>
            <img src="https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=600&h=400&fit=crop" alt="Students in classroom" className="rounded-xl w-full h-72 object-cover" />
          </GlassCard>
          <GlassCard className="absolute -bottom-6 -left-6 p-4 animate-float" hover={false}>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full gradient-bg flex items-center justify-center">
                <Trophy className="w-5 h-5 text-primary-foreground" />
              </div>
              <div>
                <div className="text-sm font-bold">#1 Ranked</div>
                <div className="text-xs text-muted-foreground">In Regional Schools</div>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>
    </section>

    {/* Programs */}
    <section className="py-20 bg-secondary/30">
      <div className="container mx-auto px-4">
        <SectionTitle title="Our Programs" subtitle="Comprehensive education from primary through high school" />
        <div className="grid md:grid-cols-3 gap-6">
          {programs.map((program) => (
            <GlassCard key={program.title} className="p-8 group">
              <div className="text-4xl mb-4">{program.icon}</div>
              <div className="text-xs font-semibold gradient-text mb-2">{program.grades}</div>
              <h3 className="text-xl font-heading font-bold mb-2">{program.title}</h3>
              <p className="text-sm text-muted-foreground mb-4">{program.desc}</p>
              <Link to="/academics" className="inline-flex items-center gap-1 text-sm text-primary font-medium group-hover:gap-2 transition-all">
                Explore Curriculum <ChevronRight className="w-4 h-4" />
              </Link>
            </GlassCard>
          ))}
        </div>
      </div>
    </section>

    {/* Why Choose Us */}
    <section className="container mx-auto px-4 py-20">
      <SectionTitle title="Why Choose ABC International?" subtitle="Discover what makes us the preferred choice for over 1,500 families" />
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {highlights.map((item) => (
          <GlassCard key={item.title} className="p-7">
            <div className="w-12 h-12 rounded-xl gradient-bg flex items-center justify-center mb-4">
              <item.icon className="w-6 h-6 text-primary-foreground" />
            </div>
            <h3 className="font-heading font-semibold text-lg mb-2">{item.title}</h3>
            <p className="text-muted-foreground text-sm">{item.desc}</p>
          </GlassCard>
        ))}
      </div>
    </section>

    {/* Featured Faculty */}
    <section className="py-20 bg-secondary/30">
      <div className="container mx-auto px-4">
        <SectionTitle title="Meet Our Faculty" subtitle="Passionate educators dedicated to your child's success" />
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {staffMembers.slice(0, 4).map((member) => (
            <GlassCard key={member.id} className="overflow-hidden group">
              <div className="h-52 overflow-hidden">
                <img src={member.image} alt={member.name} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
              </div>
              <div className="p-5">
                <h3 className="font-heading font-semibold">{member.name}</h3>
                <span className="text-xs font-medium gradient-text">{member.subject}</span>
                <p className="text-xs text-muted-foreground mt-1.5 line-clamp-2">{member.bio}</p>
              </div>
            </GlassCard>
          ))}
        </div>
        <div className="text-center mt-8">
          <Link to="/staff" className="inline-flex items-center gap-2 border border-border px-6 py-3 rounded-xl font-semibold hover:bg-secondary transition-colors">
            View All Faculty <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </section>

    {/* Upcoming Events */}
    <section className="container mx-auto px-4 py-20">
      <div className="grid lg:grid-cols-2 gap-12 items-start">
        <div>
          <SectionTitle title="Upcoming Events" subtitle="Mark your calendar for exciting school activities" center={false} />
          <div className="space-y-4">
            {events.map((event) => (
              <GlassCard key={event.title} className="p-5 flex gap-5 items-start">
                <div className="w-16 h-16 rounded-xl gradient-bg flex flex-col items-center justify-center text-primary-foreground shrink-0">
                  <span className="text-xs font-medium opacity-80">{event.date.split(" ")[0]}</span>
                  <span className="text-xl font-bold leading-tight">{event.date.split(" ")[1]}</span>
                </div>
                <div>
                  <h4 className="font-heading font-semibold">{event.title}</h4>
                  <p className="text-sm text-muted-foreground mt-0.5">{event.desc}</p>
                  <div className="flex items-center gap-1 mt-2 text-xs text-muted-foreground">
                    <Clock className="w-3 h-3" /> {event.time}
                  </div>
                </div>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Latest News */}
        <div>
          <SectionTitle title="Latest News" subtitle="What's happening at our school" center={false} />
          <div className="space-y-4">
            {newsItems.slice(0, 4).map((news) => (
              <Link key={news.slug} to={`/news/${news.slug}`}>
                <GlassCard className="p-4 flex gap-4 items-center group">
                  <img src={news.image} alt={news.title} className="w-20 h-20 rounded-xl object-cover shrink-0 group-hover:scale-105 transition-transform" />
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-[10px] font-medium gradient-bg text-primary-foreground px-2 py-0.5 rounded-full">{news.category}</span>
                      <span className="text-[10px] text-muted-foreground">{news.date}</span>
                    </div>
                    <h4 className="text-sm font-heading font-semibold group-hover:text-primary transition-colors">{news.title}</h4>
                    <p className="text-xs text-muted-foreground line-clamp-1 mt-0.5">{news.excerpt}</p>
                  </div>
                </GlassCard>
              </Link>
            ))}
          </div>
          <div className="mt-4">
            <Link to="/news" className="inline-flex items-center gap-2 text-primary font-semibold text-sm hover:gap-3 transition-all">
              View All News <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>
    </section>

    {/* Testimonials */}
    <section className="py-20 bg-secondary/30">
      <div className="container mx-auto px-4">
        <SectionTitle title="What Parents & Alumni Say" subtitle="Hear from our community about their ABC International experience" />
        <div className="grid md:grid-cols-3 gap-6">
          {testimonials.map((t) => (
            <GlassCard key={t.name} className="p-7">
              <div className="flex items-center gap-1 mb-4">
                {[1, 2, 3, 4, 5].map((s) => (
                  <Star key={s} className="w-4 h-4 fill-primary text-primary" />
                ))}
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed mb-5 italic">"{t.text}"</p>
              <div className="flex items-center gap-3">
                <img src={t.avatar} alt={t.name} className="w-10 h-10 rounded-full object-cover" />
                <div>
                  <div className="text-sm font-semibold">{t.name}</div>
                  <div className="text-xs text-muted-foreground">{t.role}</div>
                </div>
              </div>
            </GlassCard>
          ))}
        </div>
      </div>
    </section>

    {/* Gallery Preview */}
    <section className="container mx-auto px-4 py-20">
      <SectionTitle title="Campus Life" subtitle="A glimpse into the vibrant life at ABC International" />
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400&h=300&fit=crop",
          "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=400&h=300&fit=crop",
          "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400&h=600&fit=crop",
          "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=400&h=300&fit=crop",
          "https://images.unsplash.com/photo-1544717305-2782549b5136?w=400&h=600&fit=crop",
          "https://images.unsplash.com/photo-1523050854058-8df90110c476?w=400&h=300&fit=crop",
          "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=400&h=300&fit=crop",
          "https://images.unsplash.com/photo-1594608661623-aa0bd3a69d98?w=400&h=300&fit=crop",
        ].map((src, i) => (
          <div key={i} className={`rounded-2xl overflow-hidden group ${i === 2 || i === 4 ? "row-span-2" : ""}`}>
            <img src={src} alt="Campus life" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
          </div>
        ))}
      </div>
      <div className="text-center mt-8">
        <Link to="/gallery" className="inline-flex items-center gap-2 gradient-bg text-primary-foreground px-6 py-3 rounded-xl font-semibold hover:opacity-90 transition-opacity">
          <Palette className="w-4 h-4" /> Explore Full Gallery
        </Link>
      </div>
    </section>

    {/* Partners */}
    <section className="py-16 bg-secondary/30">
      <div className="container mx-auto px-4">
        <p className="text-center text-sm text-muted-foreground mb-6 font-medium">Trusted by leading education organizations</p>
        <div className="flex flex-wrap justify-center gap-6 md:gap-10">
          {partners.map((p) => (
            <GlassCard key={p} className="px-6 py-3" hover={false}>
              <span className="text-sm font-semibold text-muted-foreground">{p}</span>
            </GlassCard>
          ))}
        </div>
      </div>
    </section>

    {/* Quick Contact */}
    <section className="container mx-auto px-4 py-20">
      <div className="grid md:grid-cols-3 gap-6">
        <GlassCard className="p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl gradient-bg flex items-center justify-center shrink-0">
            <Phone className="w-5 h-5 text-primary-foreground" />
          </div>
          <div>
            <h4 className="font-semibold text-sm">Call Us</h4>
            <p className="text-sm text-muted-foreground">+1 (555) 123-4567</p>
            <p className="text-xs text-muted-foreground">Mon-Fri, 8AM-5PM</p>
          </div>
        </GlassCard>
        <GlassCard className="p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl gradient-bg flex items-center justify-center shrink-0">
            <Mail className="w-5 h-5 text-primary-foreground" />
          </div>
          <div>
            <h4 className="font-semibold text-sm">Email Us</h4>
            <p className="text-sm text-muted-foreground">info@abcschool.edu</p>
            <p className="text-xs text-muted-foreground">We reply within 24 hours</p>
          </div>
        </GlassCard>
        <GlassCard className="p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl gradient-bg flex items-center justify-center shrink-0">
            <MapPin className="w-5 h-5 text-primary-foreground" />
          </div>
          <div>
            <h4 className="font-semibold text-sm">Visit Us</h4>
            <p className="text-sm text-muted-foreground">123 Education Lane</p>
            <p className="text-xs text-muted-foreground">Knowledge City, ST 12345</p>
          </div>
        </GlassCard>
      </div>
    </section>

    {/* CTA */}
    <section className="container mx-auto px-4 pb-20">
      <div className="relative overflow-hidden rounded-3xl">
        <div className="absolute inset-0 gradient-bg" />
        <div className="relative z-10 p-12 md:p-16 text-center text-primary-foreground">
          <Heart className="w-10 h-10 mx-auto mb-4 opacity-80" />
          <h2 className="text-3xl md:text-4xl font-heading font-bold mb-4">Ready to Join Our Family?</h2>
          <p className="opacity-90 mb-8 max-w-xl mx-auto">
            Give your child the gift of an exceptional education. Admissions are now open for the 2026-27 academic year. Limited seats available.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link to="/admissions" className="bg-primary-foreground text-foreground px-8 py-3.5 rounded-xl font-semibold hover:opacity-90 transition-opacity flex items-center gap-2">
              Start Application <ArrowRight className="w-4 h-4" />
            </Link>
            <Link to="/contact" className="border border-primary-foreground/30 text-primary-foreground px-8 py-3.5 rounded-xl font-semibold hover:bg-primary-foreground/10 transition-colors">
              Schedule a Visit
            </Link>
          </div>
        </div>
      </div>
    </section>
  </div>
);

export default Index;
