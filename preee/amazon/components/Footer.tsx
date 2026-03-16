import Link from 'next/link';
import Image from 'next/image';

const Footer = () => {
  return (
    <footer className="bg-[#1a1a1a] text-white py-12 px-6 border-t border-gray-800">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-5 gap-8">
        
        {/* Logo and Tagline Section */}
        <div className="col-span-1 md:col-span-2">
          <div className="flex items-center gap-3 mb-4">
            {/* Replace with your actual logo path */}
            <div className="w-10 h-10 bg-orange-600 rounded flex items-center justify-center">
              <span className="font-bold text-xl">F</span>
            </div>
            <div>
              <h2 className="text-xl font-bold leading-tight uppercase tracking-wider">Fortis</h2>
              <h2 className="text-xl font-bold leading-tight uppercase tracking-wider">Construction</h2>
            </div>
          </div>
          <p className="text-gray-400 text-sm italic">
            Building Excellence, One Stake At A Time.
          </p>
        </div>

        {/* Links Columns */}
        <div>
          <h3 className="text-gray-500 font-semibold mb-4 text-xs uppercase tracking-widest">Navigation</h3>
          <ul className="space-y-2 text-sm">
            <li><Link href="/team" className="hover:text-orange-500 transition">Our Team</Link></li>
          </ul>
        </div>

        <div>
          <h3 className="text-gray-500 font-semibold mb-4 text-xs uppercase tracking-widest">Company</h3>
          <ul className="space-y-2 text-sm">
            <li><Link href="/about" className="hover:text-orange-500 transition">About Us</Link></li>
          </ul>
        </div>

        <div>
          <h3 className="text-gray-500 font-semibold mb-4 text-xs uppercase tracking-widest">Resources</h3>
          <ul className="space-y-2 text-sm">
            <li><Link href="/privacy" className="hover:text-orange-500 transition">Privacy Policy</Link></li>
          </ul>
        </div>

        <div>
          <h3 className="text-gray-500 font-semibold mb-4 text-xs uppercase tracking-widest">Services</h3>
          <ul className="space-y-2 text-sm">
            <li><Link href="/quote" className="hover:text-orange-500 transition">Get Your Quote</Link></li>
          </ul>
        </div>

      </div>
    </footer>
  );
};

export default Footer;
