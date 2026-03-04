import SectionTitle from "../../components/SectionTitle";
import Card from "../../components/Card";

export default function AcademicsPage() {
  // Dummy data for classes and subjects
  const classes = [
    {
      name: "Primary School",
      description: "Foundation classes for ages 6-10 focusing on basic literacy, numeracy, and creativity.",
      subjects: ["Mathematics", "English", "Science", "Art", "Physical Education"],
    },
    {
      name: "Middle School",
      description: "Developing critical thinking and broader knowledge for ages 11-13.",
      subjects: ["Mathematics", "English", "Science", "History", "Geography", "Computer Studies"],
    },
    {
      name: "High School",
      description: "Advanced academics preparing students for higher education and global challenges.",
      subjects: ["Mathematics", "Physics", "Chemistry", "Biology", "English Literature", "Computer Science", "Economics"],
    },
  ];

  return (
    <div className="container mx-auto px-4 py-12 space-y-16">

      {/* Classes Offered */}
      <section>
        <SectionTitle title="Classes Offered" />
        <div className="grid md:grid-cols-3 gap-6 mt-6">
          {classes.map((cls) => (
            <Card
              key={cls.name}
              title={cls.name}
              description={cls.description}
              image="" // optional image later
            />
          ))}
        </div>
      </section>

      {/* Subjects for each class */}
      <section>
        <SectionTitle title="Subjects Overview" />
        <div className="grid md:grid-cols-3 gap-6 mt-6">
          {classes.map((cls) => (
            <div key={cls.name} className="bg-white shadow-md rounded-lg p-6">
              <h3 className="font-bold text-xl mb-4">{cls.name}</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                {cls.subjects.map((subj) => (
                  <li key={subj}>{subj}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* Curriculum Information */}
      <section>
        <SectionTitle title="Curriculum" />
        <p className="text-gray-700 leading-relaxed mt-4">
          Our curriculum follows international standards and is designed to develop knowledge, critical thinking, and social skills.
          Students engage in project-based learning, collaborative activities, and examinations that assess both understanding and creativity.
        </p>
      </section>

      {/* Examination System */}
      <section>
        <SectionTitle title="Examination System" />
        <p className="text-gray-700 leading-relaxed mt-4">
          Students are evaluated through continuous assessments, quizzes, midterm exams, and final exams. 
          Our system ensures fair evaluation and helps identify areas of improvement for each student.
        </p>
      </section>

      {/* Download Syllabus Button */}
      <section className="text-center mt-8">
        <a
          href="/documents/syllabus.pdf"
          className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
          download
        >
          Download Full Syllabus
        </a>
      </section>

    </div>
  );
}