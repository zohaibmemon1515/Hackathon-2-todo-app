"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/auth-context";
import { LogOut, LayoutDashboard, User, Zap } from "lucide-react";

export default function Navigation() {
  const pathname = usePathname();
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header className="sticky top-0 z-50 w-full px-4 py-4">
      <nav className="max-w-7xl mx-auto bg-white/70 backdrop-blur-xl border border-white/20 shadow-[0_8px_32px_0_rgba(31,38,135,0.07)] rounded-4xl px-6 py-3 transition-all duration-300">
        <div className="flex items-center justify-between">
          
          {/* LOGO SECTION */}
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="relative">
              <div className="w-10 h-10 bg-linear-to-tr from-indigo-600 to-violet-600 rounded-xl shadow-lg shadow-indigo-200 flex items-center justify-center transform group-hover:rotate-12 transition-transform duration-300">
                <Zap size={20} className="text-white fill-current" />
              </div>
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 border-2 border-white rounded-full"></div>
            </div>
            <span className="text-xl font-black tracking-tighter text-slate-800 italic">
              TASK<span className="text-indigo-600">MASTER</span>
            </span>
          </Link>

          {/* MAIN LINKS */}
          <div className="hidden md:flex items-center bg-slate-100/50 p-1 rounded-2xl border border-slate-200/50">
            <Link
              href="/"
              className={`px-6 py-2 text-xs font-black uppercase tracking-widest rounded-xl transition-all ${
                pathname === "/"
                  ? "bg-white text-indigo-600 shadow-sm"
                  : "text-slate-500 hover:text-slate-900"
              }`}
            >
              Home
            </Link>
            
            {isAuthenticated ? (
              <Link
                href="/dashboard"
                className={`px-6 py-2 text-xs font-black uppercase tracking-widest rounded-xl transition-all ${
                  pathname.includes("/dashboard")
                    ? "bg-white text-indigo-600 shadow-sm"
                    : "text-slate-500 hover:text-slate-900"
                }`}
              >
                Dashboard
              </Link>
            ) : (
              <div className="flex">
                {/* Sirf Features rakha hai, Pricing hata diya */}
                {["Features"].map((item) => (
                  <Link
                    key={item}
                    href={`#${item.toLowerCase()}`}
                    className="px-6 py-2 text-xs font-black uppercase tracking-widest text-slate-500 hover:text-slate-900 rounded-xl transition-all"
                  >
                    {item}
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* AUTH SECTION */}
          <div className="flex items-center space-x-3">
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <div className="hidden sm:flex flex-col items-end mr-2">
                  <span className="text-[10px] font-black text-indigo-600 uppercase tracking-tighter leading-none">Pro Member</span>
                  <span className="text-sm font-bold text-slate-700 capitalize">
                    {user?.first_name || user?.email?.split('@')[0]}
                  </span>
                </div>
                
                <div className="h-10 w-10 rounded-full bg-slate-100 border-2 border-white shadow-sm flex items-center justify-center text-indigo-600 overflow-hidden">
                   <User size={20} />
                </div>

                <button
                  onClick={logout}
                  className="p-2.5 rounded-xl bg-rose-50 text-rose-500 hover:bg-rose-500 hover:text-white transition-all duration-300 group"
                  title="Logout"
                >
                  <LogOut size={18} className="group-hover:-translate-x-0.5 transition-transform" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link href="/auth/login">
                  <Button variant="ghost" className="text-xs font-black uppercase tracking-widest text-slate-600 hover:bg-slate-50 rounded-xl">
                    Sign In
                  </Button>
                </Link>
                <Link href="/auth/register">
                  <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-100 px-6 py-5 text-xs font-black uppercase tracking-widest rounded-xl transition-all active:scale-95">
                    Get Started
                  </Button>
                </Link>
              </div>
            )}
          </div>

        </div>
      </nav>
    </header>
  );
}