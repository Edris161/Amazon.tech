"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import StatCard from "@/components/dashboard/StatCard";
import {
  Users,
  UserSquare2,
  BookOpen,
  GraduationCap,
  Calculator,
  Loader2,
} from "lucide-react";

export default function DashboardHome() {
  const { data: summary, isLoading, error } = useQuery({
    queryKey: ["dashboard-summary"],
    queryFn: async () => {
      const response = await api.get("/dashboard/summary/");
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (error)
    return (
      <div className="p-4 bg-red-50 text-red-500 rounded-xl">
        Connection Error: Ensure backend is running.
      </div>
    );

  // ✅ FIXED: statsList is now properly defined
  const statsList = [
    {
      title: "Students",
      value: summary?.students ?? 0,
      icon: Users,
      color: "text-blue-600",
      bg: "bg-blue-100",
    },
    {
      title: "Teachers",
      value: summary?.teachers ?? 0,
      icon: UserSquare2,
      color: "text-green-600",
      bg: "bg-green-100",
    },
    {
      title: "Courses",
      value: summary?.courses ?? 0,
      icon: BookOpen,
      color: "text-purple-600",
      bg: "bg-purple-100",
    },
    {
      title: "Classes",
      value: summary?.classes ?? 0,
      icon: GraduationCap,
      color: "text-yellow-600",
      bg: "bg-yellow-100",
    },
    {
      title: "Exams",
      value: summary?.exams ?? 0,
      icon: Calculator,
      color: "text-red-600",
      bg: "bg-red-100",
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Dashboard Overview
        </h1>
        <p className="text-gray-500 font-light">
          Real-time school statistics
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
        {statsList.map((stat, index) => (
          <StatCard
            key={index}
            title={stat.title}
            value={stat.value}
            icon={stat.icon}
            color={stat.color}
            bgColor={stat.bg}
          />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="h-64 bg-white rounded-2xl border border-dashed border-gray-200 flex items-center justify-center text-gray-400">
          Chart Area
        </div>
        <div className="h-64 bg-white rounded-2xl border border-dashed border-gray-200 flex items-center justify-center text-gray-400">
          Recent Activity
        </div>
      </div>
    </div>
  );
}