import { BookOpen, Download, ClipboardList, GraduationCap } from "lucide-react";
import GlassCard from "@/components/GlassCard";
import SectionTitle from "@/components/SectionTitle";

const levels = [
  {
    title: "Primary School",
    grades: "Grade 1-5",
    subjects: [
      "English",
      "Mathematics",
      "Science",
      "Social Studies",
      "Art & Craft",
      "Physical Education",
    ],
    desc: "Building strong foundations through interactive and play-based learning.",
  },
  {
    title: "Middle School",
    grades: "Grade 6-8",
    subjects: [
      "English",
      "Mathematics",
      "Physics",
      "Chemistry",
      "Biology",
      "History",
      "Geography",
      "Computer Science",
    ],
    desc: "Developing critical thinking and analytical skills.",
  },
  {
    title: "High School",
    grades: "Grade 9-12",
    subjects: [
      "English",
      "Advanced Mathematics",
      "Physics",
      "Chemistry",
      "Biology",
      "Computer Science",
      "Economics",
      "Psychology",
    ],
    desc: "Preparing students for higher education and career readiness.",
  },
];

const stats = [
  { icon: BookOpen, label: "50+ Courses" },
  { icon: GraduationCap, label: "AP Programs" },
  { icon: ClipboardList, label: "Project-Based" },
  { icon: Download, label: "Digital Learning" },
];

const exams = [
  {
    term: "Continuous Assessment",
    desc: "Regular quizzes, assignments, and class participation (30%)",
  },
  {
    term: "Mid-Term Exams",
    desc: "Comprehensive assessments halfway through each semester (30%)",
  },
  {
    term: "Final Exams",
    desc: "End-of-term examinations covering full syllabus (40%)",
  },
];

const Academics = () => {
  return (
    <div className="min-h-screen pt-24">

      {/* Page Header */}
      <section className="container mx-auto px-4 py-16">
        <SectionTitle
          title="Academics"
          subtitle="Comprehensive curriculum designed for 21st-century learners"
        />
      </section>

      {/* Curriculum */}
      <section className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-2 gap-8 items-center mb-16">

          <div>
            <h3 className="text-2xl font-heading font-bold mb-4">
              Our Curriculum
            </h3>

            <p className="text-muted-foreground leading-relaxed mb-4">
              We follow an internationally recognized curriculum that combines
              academic rigor with practical application. Our programs emphasize
              critical thinking, creativity, collaboration, and communication.
            </p>

            <p className="text-muted-foreground leading-relaxed">
              Each student receives personalized attention with small class
              sizes, ensuring optimal learning outcomes.
            </p>
          </div>

          <GlassCard className="p-8" hover={false}>
            <div className="grid grid-cols-2 gap-4">
              {stats.map((item) => (
                <div
                  key={item.label}
                  className="text-center p-4 rounded-xl bg-secondary/50"
                >
                  <item.icon className="w-6 h-6 text-primary mx-auto mb-2" />
                  <span className="text-sm font-medium">{item.label}</span>
                </div>
              ))}
            </div>
          </GlassCard>

        </div>
      </section>

      {/* Programs */}
      <section className="container mx-auto px-4 py-8">
        <SectionTitle title="Programs Offered" />

        <div className="grid lg:grid-cols-3 gap-6">
          {levels.map((level) => (
            <GlassCard key={level.title} className="p-8">

              <div className="gradient-bg text-primary-foreground text-xs font-semibold px-3 py-1 rounded-full inline-block mb-4">
                {level.grades}
              </div>

              <h3 className="text-xl font-heading font-bold mb-2">
                {level.title}
              </h3>

              <p className="text-sm text-muted-foreground mb-4">
                {level.desc}
              </p>

              <h4 className="text-sm font-semibold mb-2">Subjects:</h4>

              <div className="flex flex-wrap gap-2">
                {level.subjects.map((s) => (
                  <span
                    key={s}
                    className="text-xs bg-secondary px-2.5 py-1 rounded-full"
                  >
                    {s}
                  </span>
                ))}
              </div>

            </GlassCard>
          ))}
        </div>
      </section>

      {/* Examination */}
      <section className="container mx-auto px-4 py-16">

        <SectionTitle
          title="Examination System"
          subtitle="Fair and comprehensive assessment methodology"
        />

        <GlassCard className="p-8 max-w-3xl mx-auto" hover={false}>

          <div className="space-y-4">
            {exams.map((item) => (
              <div
                key={item.term}
                className="flex gap-4 p-4 rounded-xl bg-secondary/50"
              >
                <div className="w-2 h-2 rounded-full gradient-bg mt-2 shrink-0" />

                <div>
                  <h4 className="font-semibold text-sm">{item.term}</h4>
                  <p className="text-sm text-muted-foreground">
                    {item.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <button className="mt-6 gradient-bg text-primary-foreground px-6 py-3 rounded-xl font-semibold hover:opacity-90 transition-opacity flex items-center gap-2 mx-auto">
            <Download className="w-4 h-4" />
            Download Syllabus
          </button>

        </GlassCard>

      </section>

    </div>
  );
};

export default Academics;