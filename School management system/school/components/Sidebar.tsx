"use client";
import { LayoutDashboard, Users, GraduationCap, Wallet, LogOut } from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="w-64 bg-[#1e1b2e] text-white p-6 flex flex-col items-center">
      {/* Profile Section */}
      <div className="mt-4 flex flex-col items-center border-b border-gray-700 pb-6 w-full text-center">
        <div className="h-16 w-16 rounded-full border-2 border-pink-500 overflow-hidden bg-gray-400">
           {/* <img src="/user.jpg" alt="Admin" /> */}
        </div>
        <h3 className="mt-3 font-bold text-sm">مدیر نورالله نوری</h3>
        <p className="text-[10px] text-gray-400">سیستم مدیریت مکتب</p>
      </div>

      {/* Menu Links */}
      <nav className="mt-8 w-full space-y-2">
        <div className="flex items-center gap-3 rounded-lg bg-pink-500/20 p-3 text-pink-400 cursor-pointer">
          <LayoutDashboard size={20} /> <span>داشبورد</span>
        </div>
        <div className="flex items-center gap-3 rounded-lg p-3 hover:bg-white/10 cursor-pointer transition">
          <Users size={20} /> <span>دانش‌آموزان</span>
        </div>
        <div className="flex items-center gap-3 rounded-lg p-3 hover:bg-white/10 cursor-pointer transition">
          <GraduationCap size={20} /> <span>معلمان</span>
        </div>
        <div className="flex items-center gap-3 rounded-lg p-3 hover:bg-white/10 cursor-pointer transition">
          <Wallet size={20} /> <span>خزانه</span>
        </div>
      </nav>

      <button className="mt-auto flex w-full items-center gap-3 rounded-lg p-3 text-red-400 hover:bg-red-500/10 transition">
        <LogOut size={20} /> <span>خروج</span>
      </button>
    </aside>
  );
}
