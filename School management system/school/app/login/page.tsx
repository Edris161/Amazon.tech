"use client";

import { useState } from "react";
import api from "@/lib/api";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const res = await api.post("auth/login/", { email, password });

    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);

    const user = await api.get("auth/me/");
    const role = user.data.role;

    if (role === "admin") router.push("/admin");
    if (role === "teacher") router.push("/teacher");
    if (role === "student") router.push("/student");
  };

  return (
    <div className="flex h-screen items-center justify-center">
      <div className="p-6 bg-white shadow rounded-xl w-96">
        <h2 className="text-2xl mb-4">Login</h2>
        <input
          className="w-full border p-2 mb-3"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          className="w-full border p-2 mb-3"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 text-white p-2 rounded"
        >
          Login
        </button>
      </div>
    </div>
  );
}