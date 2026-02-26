import { 
  LayoutDashboard, Users, UserSquare2, BookOpen, 
  CalendarCheck, GraduationCap, Calculator, Settings, LogOut 
} from "lucide-react";

export const menuItems = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Students", href: "/dashboard/students", icon: GraduationCap },
  { name: "Teachers", href: "/dashboard/teachers", icon: UserSquare2 },
  { name: "Classes", href: "/dashboard/classes", icon: Users },
  { name: "Subjects", href: "/dashboard/subjects", icon: BookOpen },
  { name: "Attendance", href: "/dashboard/attendance", icon: CalendarCheck },
  { name: "Exams", href: "/dashboard/exams", icon: LayoutDashboard }, // You can swap icons as needed
  { name: "Finance", href: "/dashboard/finance", icon: Calculator },
  { name: "Settings", href: "/dashboard/settings", icon: Settings },
];
