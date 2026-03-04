import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu, X, GraduationCap, Sun, Moon } from "lucide-react";

const navLinks = [
  { to: "/", label: "Home" },
  { to: "/about", label: "About" },
  { to: "/academics", label: "Academics" },
  { to: "/staff", label: "Staff" },
  { to: "/admissions", label: "Admissions" },
  { to: "/gallery", label: "Gallery" },
  { to: "/news", label: "News" },
  { to: "/contact", label: "Contact" },
];

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [isDark, setIsDark] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const toggleDark = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle("dark");
  };

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled
          ? "glass-strong py-2 shadow-glass-lg"
          : "bg-transparent py-4"
      }`}
    >
      <div className="container mx-auto px-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl gradient-bg flex items-center justify-center group-hover:scale-110 transition-transform">
            <GraduationCap className="w-6 h-6 text-primary-foreground" />
          </div>
          <span className="font-heading font-bold text-lg">ABC International</span>
        </Link>

        {/* Desktop nav */}
        <div className="hidden lg:flex items-center gap-1">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                location.pathname === link.to
                  ? "gradient-bg text-primary-foreground"
                  : "hover:bg-secondary"
              }`}
            >
              {link.label}
            </Link>
          ))}
          <button
            onClick={toggleDark}
            className="ml-2 p-2 rounded-lg hover:bg-secondary transition-colors"
            aria-label="Toggle dark mode"
          >
            {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
        </div>

        {/* Mobile */}
        <div className="lg:hidden flex items-center gap-2">
          <button onClick={toggleDark} className="p-2 rounded-lg hover:bg-secondary transition-colors">
            {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
          <button onClick={() => setIsOpen(!isOpen)} className="p-2 rounded-lg hover:bg-secondary transition-colors">
            {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="lg:hidden glass-strong mt-2 mx-4 rounded-2xl p-4 animate-scale-in">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              onClick={() => setIsOpen(false)}
              className={`block px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                location.pathname === link.to
                  ? "gradient-bg text-primary-foreground"
                  : "hover:bg-secondary"
              }`}
            >
              {link.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
