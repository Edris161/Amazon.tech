import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  color: string; // Tailwind color class e.g., 'text-blue-600'
  bgColor: string; // Tailwind bg color class e.g., 'bg-blue-50'
}

export default function StatCard({ title, value, icon: Icon, color, bgColor }: StatCardProps) {
  return (
    <div className="group bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500 mb-1">{title}</p>
          <h3 className="text-2xl font-bold text-gray-900">{value}</h3>
        </div>
        <div className={`p-3 ${bgColor} rounded-xl group-hover:scale-110 transition-transform duration-300`}>
          <Icon className={`w-6 h-6 ${color}`} />
        </div>
      </div>
      <div className="mt-4 flex items-center text-xs">
        <span className="text-green-500 font-medium mr-1">↑ 12%</span>
        <span className="text-gray-400 font-light text-[10px]">than last month</span>
      </div>
    </div>
  );
}
