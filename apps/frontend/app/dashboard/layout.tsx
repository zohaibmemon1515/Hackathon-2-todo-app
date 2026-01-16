"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";
import {
  LayoutDashboard,
  LogOut,
  Menu,
  Bell,
  Zap,
  ChevronRight,
  UserCircle,
  CalendarDays,
  Activity,
  MessageSquare
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const { loading, isAuthenticated, logout, user } = useAuth();
  const [isSidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, loading, router]);

  if (loading) return <LoadingScreen />;
  if (!isAuthenticated) return null;

  const navItems = [
    { name: "Overview", icon: LayoutDashboard, href: "/dashboard" },
    { name: "Chat", icon: MessageSquare, href: "/chat" },
  ];

  return (
    <div className="flex h-screen bg-[#FDFDFD] dark:bg-[#0B0E14] overflow-hidden font-sans">
      {/* --- SIDEBAR --- */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 w-72 bg-white dark:bg-[#11141D] border-r border-slate-100 dark:border-slate-800/50 transition-all duration-300 lg:relative lg:translate-x-0",
          !isSidebarOpen && "-translate-x-full"
        )}
      >
        <div className="flex flex-col h-full p-6">
          {/* BRANDING LOGO */}
          <div className="flex items-center gap-3 px-2 mb-10 group cursor-default">
            <div className="h-10 w-10 bg-linear-to-tr from-indigo-600 to-violet-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-100 dark:shadow-none transform group-hover:rotate-6 transition-transform duration-300">
              <Zap size={20} className="text-white fill-current" />
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-black tracking-tighter text-slate-800 dark:text-white leading-none italic">
                TASK<span className="text-indigo-600">MASTER</span>
              </span>
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">Control Center</span>
            </div>
          </div>

          {/* NAVIGATION LINKS */}
          <nav className="flex-1 space-y-2">
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] px-3 mb-4">Workspace</p>
            {navItems.map((item) => (
              <a
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center justify-between px-4 py-3.5 rounded-2xl text-sm font-bold transition-all duration-300 group",
                  pathname === item.href
                    ? "bg-slate-900 text-white shadow-xl shadow-slate-200 dark:shadow-none"
                    : "text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900"
                )}
              >
                <div className="flex items-center gap-3">
                  <item.icon className={cn("h-5 w-5", pathname === item.href ? "text-indigo-400" : "group-hover:text-indigo-600")} />
                  {item.name}
                </div>
                {pathname === item.href && <ChevronRight size={14} className="text-indigo-400 animate-pulse" />}
              </a>
            ))}
          </nav>

          {/* LOGOUT BUTTON */}
          <button
            onClick={logout}
            className="group mt-auto flex items-center justify-between w-full p-4 rounded-[1.8rem] bg-rose-50/30 dark:bg-rose-950/10 border border-transparent hover:border-rose-100 transition-all duration-300 active:scale-95"
          >
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-white dark:bg-slate-800 shadow-sm group-hover:bg-rose-500 group-hover:text-white transition-all duration-500">
                <LogOut className="h-4 w-4" />
              </div>
              <div className="text-left">
                <p className="text-xs font-black text-slate-800 dark:text-slate-200 group-hover:text-rose-600">Sign Out</p>
                <p className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter italic">End Session</p>
              </div>
            </div>
          </button>
        </div>
      </aside>

      {/* --- MAIN CONTENT --- */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* ADVANCED HEADER */}
        <header className="h-24 flex items-center justify-between px-8 bg-white/60 dark:bg-[#0B0E14]/60 backdrop-blur-xl border-b border-slate-50 dark:border-slate-800/50 sticky top-0 z-40">
          <div className="flex items-center gap-6">
            <button
              onClick={() => setSidebarOpen(!isSidebarOpen)}
              className="lg:hidden p-3 rounded-2xl bg-slate-100 text-slate-600 hover:bg-indigo-600 hover:text-white transition-all shadow-sm"
            >
              <Menu className="h-6 w-6" />
            </button>
            
            {/* GREETING WIDGET */}
            <div className="hidden md:flex flex-col">
              <h1 className="text-xl font-black text-slate-900 dark:text-white tracking-tight italic">
                Hi, {user?.first_name || "Champ"}! 👋
              </h1>
              <div className="flex items-center gap-2 mt-1.5">
                <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] flex items-center gap-1.5">
                  <Activity size={10} className="text-emerald-500" /> System Active
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* LIVE DATE CAPSULE */}
            <div className="hidden lg:flex items-center gap-3 bg-slate-50 dark:bg-slate-900/50 px-5 py-2.5 rounded-2xl border border-slate-100 dark:border-slate-800/50 mr-2">
              <CalendarDays size={16} className="text-indigo-500" />
              <div className="text-left">
                <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest leading-none mb-0.5 italic">Today</p>
                <p className="text-xs font-black text-slate-700 dark:text-slate-300">
                  {new Date().toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'short' })}
                </p>
              </div>
            </div>

            {/* NOTIFICATION */}
            <button className="relative p-3.5 rounded-2xl bg-white dark:bg-slate-900 text-slate-400 hover:text-indigo-600 shadow-sm border border-slate-100 dark:border-slate-800 transition-all active:scale-90 group">
              <Bell className="h-5 w-5 group-hover:rotate-12 transition-transform" />
              <span className="absolute top-3.5 right-4 w-2 h-2 bg-indigo-600 rounded-full ring-4 ring-white dark:ring-slate-900 animate-bounce"></span>
            </button>
            
            <div className="h-10 w-px bg-slate-100 dark:bg-slate-800 mx-1" />

            {/* USER AVATAR */}
            <div className="flex items-center gap-3 pl-2 group">
              <div className="h-12 w-12 rounded-2xl bg-linear-to-tr from-indigo-500 via-purple-500 to-pink-500 p-0.5 shadow-lg shadow-indigo-100 dark:shadow-none transition-all group-hover:scale-105 group-hover:rotate-3">
                <div className="h-full w-full rounded-[0.9rem] bg-white dark:bg-slate-900 flex items-center justify-center overflow-hidden">
                  <UserCircle size={28} className="text-slate-300 group-hover:text-indigo-600 transition-colors" />
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* MAIN SCROLL AREA */}
        <main className="flex-1 overflow-y-auto p-6 lg:p-10 bg-[#F8FAFC]/50 dark:bg-[#0B0E14] custom-scrollbar">
          <div className="max-w-7xl mx-auto pb-10">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

function LoadingScreen() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white dark:bg-[#0B0E14]">
      <div className="relative flex items-center justify-center">
        <div className="h-24 w-24 border-[6px] border-slate-50 dark:border-slate-800 rounded-[2.5rem] rotate-45"></div>
        <div className="absolute h-24 w-24 border-[6px] border-indigo-600 border-t-transparent rounded-[2.5rem] rotate-45 animate-spin"></div>
        <Zap size={32} className="absolute text-indigo-600 animate-pulse fill-current" />
      </div>
      <div className="mt-10 text-center space-y-3">
        <h2 className="text-2xl font-black text-slate-800 dark:text-white tracking-tighter italic uppercase">
          TASK<span className="text-indigo-600">MASTER</span>
        </h2>
        <div className="flex items-center justify-center gap-2">
          <div className="h-1 w-1 bg-indigo-600 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
          <div className="h-1 w-1 bg-indigo-600 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
          <div className="h-1 w-1 bg-indigo-600 rounded-full animate-bounce"></div>
        </div>
      </div>
    </div>
  );
}