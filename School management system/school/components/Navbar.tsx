import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-primary text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="font-bold text-xl">
          ABC International School
        </Link>
        <div className="space-x-4">
          <Link href="/">Home</Link>
          <Link href="/about">About</Link>
          <Link href="/academics">Academics</Link>
          <Link href="/staff">Staff</Link>
          <Link href="/admissions">Admissions</Link>
          <Link href="/gallery">Gallery</Link>
          <Link href="/news">News</Link>
          <Link href="/contact">Contact</Link>
        </div>
      </div>
    </nav>
  );
}