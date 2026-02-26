"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import Sidebar from "@/components/layout/Sidebar";
import Navbar from "@/components/layout/Navbar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get("auth/me/");
        setUser(res.data);
      } catch (err) {
        router.push("/login");
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  if (loading) return <div className="p-10">Loading...</div>;

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar role={user.role} />
      <div className="flex-1 flex flex-col">
        <Navbar user={user} />
        <main className="p-6 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}