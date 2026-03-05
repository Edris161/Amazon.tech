import { useState, useEffect } from "react";
import { Mail, Phone, MapPin, Send, Facebook, Twitter, Instagram, Youtube } from "lucide-react";
import GlassCard from "@/components/GlassCard";
import SectionTitle from "@/components/SectionTitle";
import { z } from "zod";
import { toast } from "sonner";

const contactSchema = z.object({
  name: z.string().trim().min(1, "Name is required").max(100),
  email: z.string().trim().email("Invalid email address").max(255),
  message: z.string().trim().min(1, "Message is required").max(1000),
});

const Contact = () => {

  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [errors, setErrors] = useState({});
  const [contactInfo, setContactInfo] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/contact-info/")
      .then(res => res.json())
      .then(data => setContactInfo(data))
      .catch(err => console.log(err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const result = contactSchema.safeParse(form);

    if (!result.success) {
      const fieldErrors = {};
      result.error.errors.forEach((err) => {
        if (err.path[0]) fieldErrors[err.path[0]] = err.message;
      });
      setErrors(fieldErrors);
      return;
    }

    setErrors({});

    try {
      const res = await fetch("http://localhost:8000/api/contact-messages/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
      });

      if (res.ok) {
        toast.success("Message sent successfully! We'll get back to you soon.");
        setForm({ name: "", email: "", message: "" });
      } else {
        toast.error("Something went wrong.");
      }

    } catch (error) {
      console.log(error);
    }

  };

  return (
    <div className="min-h-screen pt-24">

      <section className="container mx-auto px-4 py-16">
        <SectionTitle
          title="Contact Us"
          subtitle="We'd love to hear from you. Reach out anytime."
        />
      </section>

      <section className="container mx-auto px-4 pb-20">

        <div className="grid lg:grid-cols-2 gap-8 max-w-5xl mx-auto">

          {/* FORM */}

          <GlassCard className="p-8" hover={false}>

            <h3 className="text-xl font-heading font-bold mb-6">Send a Message</h3>

            <form onSubmit={handleSubmit} className="space-y-4">

              <div>
                <label className="text-sm font-medium mb-1 block">Name</label>

                <input
                  type="text"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className="w-full px-4 py-3 rounded-xl bg-secondary/50 border border-border focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
                  placeholder="Your full name"
                />

                {errors.name && (
                  <p className="text-destructive text-xs mt-1">{errors.name}</p>
                )}

              </div>

              <div>
                <label className="text-sm font-medium mb-1 block">Email</label>

                <input
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  className="w-full px-4 py-3 rounded-xl bg-secondary/50 border border-border focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all"
                  placeholder="your@email.com"
                />

                {errors.email && (
                  <p className="text-destructive text-xs mt-1">{errors.email}</p>
                )}

              </div>

              <div>

                <label className="text-sm font-medium mb-1 block">Message</label>

                <textarea
                  value={form.message}
                  onChange={(e) => setForm({ ...form, message: e.target.value })}
                  rows={5}
                  className="w-full px-4 py-3 rounded-xl bg-secondary/50 border border-border focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all resize-none"
                  placeholder="Your message..."
                />

                {errors.message && (
                  <p className="text-destructive text-xs mt-1">{errors.message}</p>
                )}

              </div>

              <button
                type="submit"
                className="w-full gradient-bg text-primary-foreground py-3 rounded-xl font-semibold hover:opacity-90 transition-opacity flex items-center justify-center gap-2"
              >
                <Send className="w-4 h-4" /> Send Message
              </button>

            </form>

          </GlassCard>


          {/* CONTACT INFO */}

          <div className="space-y-4">

            {contactInfo && (
              <>
                <GlassCard className="p-6 flex items-start gap-4">
                  <div className="w-10 h-10 rounded-xl gradient-bg flex items-center justify-center shrink-0">
                    <MapPin className="w-5 h-5 text-primary-foreground" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Address</h4>
                    <p className="text-sm text-muted-foreground">{contactInfo.address}</p>
                  </div>
                </GlassCard>

                <GlassCard className="p-6 flex items-start gap-4">
                  <div className="w-10 h-10 rounded-xl gradient-bg flex items-center justify-center shrink-0">
                    <Phone className="w-5 h-5 text-primary-foreground" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Phone</h4>
                    <p className="text-sm text-muted-foreground">{contactInfo.phone}</p>
                  </div>
                </GlassCard>

                <GlassCard className="p-6 flex items-start gap-4">
                  <div className="w-10 h-10 rounded-xl gradient-bg flex items-center justify-center shrink-0">
                    <Mail className="w-5 h-5 text-primary-foreground" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-sm">Email</h4>
                    <p className="text-sm text-muted-foreground">{contactInfo.email}</p>
                  </div>
                </GlassCard>
              </>
            )}

          </div>

        </div>

      </section>

    </div>
  );
};

export default Contact;