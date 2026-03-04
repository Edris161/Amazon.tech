import { Link } from "react-router-dom";
import { GraduationCap, Mail, Phone, MapPin, Facebook, Twitter, Instagram, Youtube } from "lucide-react";

const Footer = () => (
  <footer className="relative mt-20">
    <div className="absolute inset-0 gradient-bg opacity-95" />
    <div className="relative z-10 container mx-auto px-4 py-16 text-primary-foreground">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
        <div>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-xl bg-primary-foreground/20 backdrop-blur flex items-center justify-center">
              <GraduationCap className="w-6 h-6" />
            </div>
            <span className="font-heading font-bold text-lg">ABC International</span>
          </div>
          <p className="text-primary-foreground/80 text-sm leading-relaxed">
            Nurturing minds, shaping futures. Providing world-class education since 1995.
          </p>
        </div>
        <div>
          <h4 className="font-heading font-semibold mb-4">Quick Links</h4>
          <div className="space-y-2">
            {["About", "Academics", "Admissions", "Contact"].map((link) => (
              <Link key={link} to={`/${link.toLowerCase()}`} className="block text-sm text-primary-foreground/80 hover:text-primary-foreground transition-colors">
                {link}
              </Link>
            ))}
          </div>
        </div>
        <div>
          <h4 className="font-heading font-semibold mb-4">Contact Info</h4>
          <div className="space-y-3 text-sm text-primary-foreground/80">
            <div className="flex items-center gap-2"><MapPin className="w-4 h-4 shrink-0" /> 123 Education Lane, Knowledge City</div>
            <div className="flex items-center gap-2"><Phone className="w-4 h-4 shrink-0" /> +1 (555) 123-4567</div>
            <div className="flex items-center gap-2"><Mail className="w-4 h-4 shrink-0" /> info@abcschool.edu</div>
          </div>
        </div>
        <div>
          <h4 className="font-heading font-semibold mb-4">Follow Us</h4>
          <div className="flex gap-3">
            {[Facebook, Twitter, Instagram, Youtube].map((Icon, i) => (
              <a key={i} href="#" className="w-10 h-10 rounded-xl bg-primary-foreground/10 backdrop-blur flex items-center justify-center hover:bg-primary-foreground/20 transition-colors">
                <Icon className="w-4 h-4" />
              </a>
            ))}
          </div>
        </div>
      </div>
      <div className="border-t border-primary-foreground/20 mt-10 pt-6 text-center text-sm text-primary-foreground/60">
        © 2026 ABC International School. All rights reserved.
      </div>
    </div>
  </footer>
);

export default Footer;
