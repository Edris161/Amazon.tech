import Link from 'next/link';


const Navbar = () => {
  return (
    <nav className="fixed top-0 w-full z-50 px-8 py-4 flex items-center justify-between bg-black/20 backdrop-blur-sm">
      {/* Logo Section */}
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-orange-600 rounded-sm flex flex-col items-center justify-center">
          <div className="w-4 h-0.5 bg-white mb-0.5"></div>
          <div className="w-4 h-0.5 bg-white mb-0.5"></div>
          <div className="w-4 h-0.5 bg-white"></div>
        </div>
        <div className="text-white font-bold leading-tight text-sm uppercase tracking-tighter">
          <div>Fortis</div>
          <div>Construction</div>
        </div>
      </div>

      {/* Navigation Links */}
      <div className="hidden md:flex items-center gap-8 text-white/90 text-sm font-medium">
        <Link href="/about" className="hover:text-orange-500 transition">About Us</Link>
        <Link href="/services" className="hover:text-orange-500 transition">Our Services</Link>
        <Link href="/team" className="hover:text-orange-500 transition">Our Team</Link>
        <Link href="/contact" className="hover:text-orange-500 transition">Contact</Link>
      </div>

      {/* CTA Button */}
      <Link 
        href="/estimate" 
        className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-2 rounded text-sm font-bold uppercase transition"
      >
        Request Free Survey
      </Link>
    </nav>
  );
};

export default Navbar;
