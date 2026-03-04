import GlassCard from "@/components/GlassCard";
import SectionTitle from "@/components/SectionTitle";
import { staffMembers } from "@/lib/data";

const Staff = () => (
  <div className="min-h-screen pt-24">
    <section className="container mx-auto px-4 py-16">
      <SectionTitle title="Our Faculty" subtitle="Meet the dedicated educators shaping the next generation" />
    </section>

    <section className="container mx-auto px-4 pb-20">
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {staffMembers.map((member) => (
          <GlassCard key={member.id} className="overflow-hidden group">
            <div className="h-56 overflow-hidden">
              <img src={member.image} alt={member.name} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
            </div>
            <div className="p-5">
              <h3 className="font-heading font-semibold">{member.name}</h3>
              <span className="text-xs font-medium gradient-text">{member.subject}</span>
              <p className="text-sm text-muted-foreground mt-2">{member.bio}</p>
            </div>
          </GlassCard>
        ))}
      </div>
    </section>
  </div>
);

export default Staff;
