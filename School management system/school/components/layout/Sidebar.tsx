"use client";

import Link from "next/link";

export default function Sidebar({ role }: { role: string }) {
  const adminMenu = [
    { name: "Dashboard", href: "/admin" },
    { name: "Students", href: "/admin/students" },
    { name: "Teachers", href: "/admin/teachers" },
    { name: "Classes", href: "/admin/classes" },
    { name: "Subjects", href: "/admin/subjects" },
    { name: "Attendance", href: "/admin/attendance" },
    { name: "Exams", href: "/admin/exams" },
    { name: "Fees", href: "/admin/fees" },
  ];

  const teacherMenu = [
    { name: "Dashboard", href: "/teacher" },
    { name: "Attendance", href: "/teacher/attendance" },
    { name: "Exams", href: "/teacher/exams" },
  ];

  const studentMenu = [
    { name: "Dashboard", href: "/student" },
    { name: "My Attendance", href: "/student/attendance" },
    { name: "My Results", href: "/student/results" },
  ];

  const menu =
    role === "admin"
      ? adminMenu
      : role === "teacher"
      ? teacherMenu
      : studentMenu;

  return (
    <aside className="w-64 bg-white shadow-lg p-5">
      <h2 className="text-xl font-bold mb-6">School System</h2>
      <nav className="space-y-3">
        {menu.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="block p-2 rounded hover:bg-gray-100"
          >
            {item.name}
          </Link>
        ))}
      </nav>
    </aside>
  );
}