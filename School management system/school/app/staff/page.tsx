"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

interface Teacher {
  id: number;
  name: string;
  position: string;
  image: string;
}

export default function StaffPage() {
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTeachers = async () => {
      try {
        const response = await api.get("teachers/");

        // 🔥 FIX HERE
        const data = Array.isArray(response.data)
          ? response.data
          : response.data.results;

        setTeachers(data || []);
      } catch (error) {
        console.error("Staff fetch error:", error);
        setTeachers([]); // prevent crash
      } finally {
        setLoading(false);
      }
    };

    fetchTeachers();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-center mb-10">Our Teachers</h1>

      <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-8">
        {teachers.length > 0 ? (
          teachers.map((teacher) => (
            <div
              key={teacher.id}
              className="bg-white shadow-lg rounded-xl p-6 text-center"
            >
              <img
                src={teacher.image}
                alt={teacher.name}
                className="w-32 h-32 object-cover rounded-full mx-auto mb-4"
              />
              <h2 className="text-xl font-semibold">{teacher.name}</h2>
              <p className="text-gray-500">{teacher.position}</p>
            </div>
          ))
        ) : (
          <p>No teachers found.</p>
        )}
      </div>
    </div>
  );
}