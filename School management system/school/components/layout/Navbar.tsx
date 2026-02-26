"use client";

import { useRouter } from "next/navigation";

export default function Navbar({ user }: any) {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    router.push("/login");
  };

  return (
    <div className="bg-white shadow px-6 py-4 flex justify-between items-center">
      <h1 className="font-semibold">Welcome, {user.full_name}</h1>

      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-500">{user.role}</span>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-3 py-1 rounded"
        >
          Logout
        </button>
      </div>
    </div>
  );
}