"use client";

import { useState } from "react";
import SectionTitle from "../../components/SectionTitle";
import api from "../../lib/api";

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);

    try {
      await api.post("contact/", formData); // Ensure backend endpoint exists
      setSuccess(true);
      setFormData({ name: "", email: "", message: "" });
    } catch (err: any) {
      console.error(err);
      setError("Failed to send message. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12 space-y-12">

      <SectionTitle title="Contact Us" />

      <div className="grid md:grid-cols-2 gap-8">
        {/* Contact Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {success && <p className="text-green-600">Message sent successfully!</p>}
          {error && <p className="text-red-600">{error}</p>}

          <input
            type="text"
            name="name"
            placeholder="Your Name"
            value={formData.name}
            onChange={handleChange}
            required
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="email"
            name="email"
            placeholder="Your Email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <textarea
            name="message"
            placeholder="Your Message"
            value={formData.message}
            onChange={handleChange}
            required
            rows={5}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
          >
            {loading ? "Sending..." : "Send Message"}
          </button>
        </form>

        {/* Contact Info + Map */}
        <div className="space-y-6">
          <div>
            <h3 className="font-bold text-xl mb-2">School Address</h3>
            <p>123 Main Street, City Name, Country</p>
          </div>
          <div>
            <h3 className="font-bold text-xl mb-2">Phone & Email</h3>
            <p>Phone: +123 456 7890</p>
            <p>Email: info@abcschool.com</p>
          </div>
          <div>
            <h3 className="font-bold text-xl mb-2">Social Media</h3>
            <div className="flex space-x-4">
              <a href="#" className="text-blue-600 hover:text-blue-800">Facebook</a>
              <a href="#" className="text-blue-500 hover:text-blue-700">Twitter</a>
              <a href="#" className="text-pink-500 hover:text-pink-700">Instagram</a>
            </div>
          </div>
          <div className="w-full h-64 rounded-lg overflow-hidden shadow">
            <iframe
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d243646.12345!2d-74.005974!3d40.712776!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMzXCsDQyJzQ2LjAiTiA3NMKwMDAnMjkuMCJX!5e0!3m2!1sen!2sus!4v1699999999999!5m2!1sen!2sus"
              className="w-full h-full border-0"
              allowFullScreen
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
            ></iframe>
          </div>
        </div>
      </div>
    </div>
  );
}