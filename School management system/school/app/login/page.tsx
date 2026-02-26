"use client";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import axios from "@/lib/api";
import { useRouter } from "next/navigation";
import { Loader2, GraduationCap, Globe } from "lucide-react";
import { toast } from "sonner";

const loginSchema = z.object({
  username: z.string().min(3, "Username is required"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormValues) => {
    setIsLoading(true);
    try {
      // Adjusted to match your Django /token/ endpoint
      const response = await axios.post("/token/", {
        username: data.username,
        password: data.password
      });
      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);
      toast.success("Welcome back!");
      router.push("/dashboard");
    } catch (error: any) {
      toast.error("Invalid username or password");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#f0f2f5] p-4 font-sans">
      {/* Main Card */}
      <div className="w-full max-w-[950px] min-h-[550px] bg-white rounded-[30px] shadow-2xl flex overflow-hidden">
        
        {/* Left Side: Form */}
        <div className="w-full lg:w-1/2 p-12 flex flex-col justify-center relative">
          {/* Language Picker Placeholder */}
          <div className="absolute top-8 left-8 flex items-center gap-2 text-gray-400 text-sm cursor-pointer">
            <Globe className="w-4 h-4" />
            <span>English</span>
          </div>

          <div className="mb-10 text-center lg:text-left">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">Welcome Back!</h1>
            <p className="text-gray-500">Please enter your details to log in.</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <div className="space-y-1">
              <input
                {...register("username")}
                type="text"
                placeholder="Username"
                className="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl focus:ring-2 focus:ring-pink-500 outline-none transition-all text-gray-700"
              />
              {errors.username && <p className="text-red-500 text-xs pl-2">{errors.username.message}</p>}
            </div>

            <div className="space-y-1">
              <input
                {...register("password")}
                type="password"
                placeholder="Password"
                className="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl focus:ring-2 focus:ring-pink-500 outline-none transition-all text-gray-700"
              />
              {errors.password && <p className="text-red-500 text-xs pl-2">{errors.password.message}</p>}
            </div>

            <div className="flex items-center justify-between text-sm px-2">
              <label className="flex items-center gap-2 text-gray-500 cursor-pointer">
                <input type="checkbox" className="rounded border-gray-300 text-pink-500 focus:ring-pink-500" />
                Remember me
              </label>
              <a href="#" className="text-pink-500 hover:underline font-medium">Forgot password?</a>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 text-white font-bold py-4 rounded-2xl shadow-lg shadow-rose-200 flex items-center justify-center transition-all transform hover:scale-[1.01]"
            >
              {isLoading ? <Loader2 className="w-6 h-6 animate-spin" /> : "LOG IN"}
            </button>
          </form>
        </div>

        {/* Right Side: Branding/Gradient */}
        <div className="hidden lg:flex w-1/2 bg-gradient-to-br from-[#1e1b4b] via-[#312e81] to-[#881337] flex-col items-center justify-center p-12 text-white relative">
          {/* Decorative Pattern Background (Optional) */}
          <div className="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com')]"></div>
          
          <div className="relative z-10 text-center">
            <div className="w-20 h-20 bg-white/10 backdrop-blur-md rounded-3xl flex items-center justify-center mx-auto mb-6 border border-white/20">
              <GraduationCap className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-3xl font-extrabold mb-4">Payam Muslim</h2>
            <p className="text-indigo-200 font-light tracking-wide">
              School Management System <br /> 
              Designed for Excellence.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
