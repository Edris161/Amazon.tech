import { Link } from "react-router-dom";
import { Download, ArrowRight, CheckCircle } from "lucide-react";
import GlassCard from "@/components/GlassCard";
import SectionTitle from "@/components/SectionTitle";
import { feeStructure } from "@/lib/data";

const steps = [
  { step: 1, title: "Submit Application", desc: "Fill out the online application form with required details." },
  { step: 2, title: "Document Verification", desc: "Submit academic records and identification documents." },
  { step: 3, title: "Entrance Assessment", desc: "Student takes an age-appropriate assessment test." },
  { step: 4, title: "Interview", desc: "Family interview with the admissions committee." },
  { step: 5, title: "Confirmation", desc: "Receive admission offer and complete enrollment." },
];

const requirements = [
  "Completed application form",
  "Birth certificate (original & copy)",
  "Previous school records / transcripts",
  "Passport-size photographs (4 copies)",
  "Medical fitness certificate",
  "Parent/Guardian ID proof",
  "Transfer certificate (if applicable)",
];

const Admissions = () => (
  <div className="min-h-screen pt-24">
    <section className="container mx-auto px-4 py-16">
      <SectionTitle title="Admissions" subtitle="Join the ABC International family — Applications open for 2026-27" />
    </section>

    {/* Steps */}
    <section className="container mx-auto px-4 py-8">
      <h3 className="text-2xl font-heading font-bold text-center mb-8">Admission Process</h3>
      <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-4 max-w-6xl mx-auto">
        {steps.map((s) => (
          <GlassCard key={s.step} className="p-6 text-center relative">
            <div className="w-10 h-10 rounded-full gradient-bg text-primary-foreground font-bold flex items-center justify-center mx-auto mb-3">
              {s.step}
            </div>
            <h4 className="font-heading font-semibold text-sm mb-1">{s.title}</h4>
            <p className="text-xs text-muted-foreground">{s.desc}</p>
          </GlassCard>
        ))}
      </div>
    </section>

    {/* Requirements */}
    <section className="container mx-auto px-4 py-16">
      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h3 className="text-2xl font-heading font-bold mb-6">Requirements</h3>
          <GlassCard className="p-6" hover={false}>
            <div className="space-y-3">
              {requirements.map((r) => (
                <div key={r} className="flex items-center gap-3">
                  <CheckCircle className="w-4 h-4 text-primary shrink-0" />
                  <span className="text-sm">{r}</span>
                </div>
              ))}
            </div>
          </GlassCard>
        </div>
        <div>
          <h3 className="text-2xl font-heading font-bold mb-6">Quick Actions</h3>
          <div className="space-y-4">
            <GlassCard className="p-6 flex items-center justify-between">
              <div>
                <h4 className="font-semibold">Download Admission Form</h4>
                <p className="text-sm text-muted-foreground">PDF format, 2 pages</p>
              </div>
              <Download className="w-5 h-5 text-primary" />
            </GlassCard>
            <Link to="/contact">
              <GlassCard className="p-6 flex items-center justify-between gradient-bg border-none">
                <div className="text-primary-foreground">
                  <h4 className="font-semibold">Apply Now</h4>
                  <p className="text-sm opacity-80">Start your application online</p>
                </div>
                <ArrowRight className="w-5 h-5 text-primary-foreground" />
              </GlassCard>
            </Link>
          </div>
        </div>
      </div>
    </section>

    {/* Fee Structure */}
    <section className="container mx-auto px-4 py-16">
      <SectionTitle title="Fee Structure" subtitle="Annual tuition and fees for the 2026-27 academic year" />
      <GlassCard className="overflow-hidden max-w-4xl mx-auto" hover={false}>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="gradient-bg text-primary-foreground">
                <th className="px-6 py-4 text-left font-semibold">Level</th>
                <th className="px-6 py-4 text-left font-semibold">Tuition</th>
                <th className="px-6 py-4 text-left font-semibold">Activities</th>
                <th className="px-6 py-4 text-left font-semibold">Technology</th>
                <th className="px-6 py-4 text-left font-semibold">Total</th>
              </tr>
            </thead>
            <tbody>
              {feeStructure.map((row, i) => (
                <tr key={row.level} className={`${i % 2 === 0 ? "bg-secondary/30" : ""} border-b border-border/50`}>
                  <td className="px-6 py-4 font-medium">{row.level}</td>
                  <td className="px-6 py-4">{row.tuition}</td>
                  <td className="px-6 py-4">{row.activities}</td>
                  <td className="px-6 py-4">{row.technology}</td>
                  <td className="px-6 py-4 font-bold gradient-text">{row.total}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </GlassCard>
    </section>
  </div>
);

export default Admissions;
