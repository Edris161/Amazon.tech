export default function Footer() {
  return (
    <footer className="bg-primary text-white py-8 mt-12">
      <div className="container mx-auto text-center">
        <p>&copy; {new Date().getFullYear()} ABC International School. All rights reserved.</p>
      </div>
    </footer>
  );
}