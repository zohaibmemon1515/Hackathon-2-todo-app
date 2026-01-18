"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/auth-context";
import { 
  LogOut, 
  User, 
  Zap, 
  Menu, 
  X, 
  ChevronRight 
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function Navigation() {
  const pathname = usePathname();
  const { user, isAuthenticated, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Close menu when route changes
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [pathname]);

  const NavLink = ({ href, children, mobile = false }: any) => {
    const isActive = pathname === href || (href !== "/" && pathname.includes(href));
    
    return (
      <Link
        href={href}
        className={cn(
          "transition-all duration-300 uppercase font-black tracking-widest italic",
          mobile 
            ? "flex items-center justify-between p-4 text-xl border-b border-slate-50 text-slate-800" 
            : "px-6 py-2 text-xs rounded-xl",
          isActive 
            ? (mobile ? "text-indigo-600 bg-indigo-50/30" : "bg-white text-indigo-600 shadow-sm")
            : "text-slate-500 hover:text-slate-900"
        )}
      >
        {children}
        {mobile && <ChevronRight size={18} className={isActive ? "text-indigo-600" : "text-slate-300"} />}
      </Link>
    );
  };

  return (
    <header className="sticky top-0 z-[100] w-full px-4 py-4">
      <nav className="max-w-7xl mx-auto bg-white/70 backdrop-blur-xl border border-white/20 shadow-[0_8px_32px_0_rgba(31,38,135,0.07)] rounded-[2rem] md:rounded-4xl px-4 md:px-6 py-3 transition-all duration-300">
        <div className="flex items-center justify-between">
          
          {/* LOGO SECTION */}
          <Link href="/" className="flex items-center space-x-3 group shrink-0">
            <div className="relative">
              <div className="w-9 h-9 md:w-10 md:h-10 bg-linear-to-tr from-indigo-600 to-violet-600 rounded-xl shadow-lg flex items-center justify-center transform group-hover:rotate-12 transition-transform duration-300">
                <Zap size={18} className="text-white fill-current" />
              </div>
              <div className="absolute -bottom-1 -right-1 w-3.5 h-3.5 bg-emerald-500 border-2 border-white rounded-full"></div>
            </div>
            <span className="text-lg md:text-xl font-black tracking-tighter text-slate-800 italic">
              TASK<span className="text-indigo-600">MASTER</span>
            </span>
          </Link>

          {/* DESKTOP MAIN LINKS */}
          <div className="hidden md:flex items-center bg-slate-100/50 p-1 rounded-2xl border border-slate-200/50">
            <NavLink href="/">Home</NavLink>
            {isAuthenticated ? (
              <>
                <NavLink href="/dashboard">Dashboard</NavLink>
                <NavLink href="/chat">Chat</NavLink>
              </>
            ) : (
              <NavLink href="#features">Features</NavLink>
            )}
          </div>

          {/* AUTH & MOBILE TOGGLE */}
          <div className="flex items-center space-x-2 md:space-x-3">
            {isAuthenticated ? (
              <div className="flex items-center gap-2 md:gap-3">
                <div className="hidden sm:flex flex-col items-end mr-1">
                  <span className="text-[9px] font-black text-indigo-600 uppercase tracking-tighter leading-none">Pro Member</span>
                  <span className="text-xs font-bold text-slate-700 capitalize">
                    {user?.first_name || 'User'}
                  </span>
                </div>
                
                <div className="h-9 w-9 md:h-10 md:w-10 rounded-full bg-slate-100 border-2 border-white shadow-sm flex items-center justify-center text-indigo-600">
                   <User size={18} />
                </div>

                <button
                  onClick={logout}
                  className="p-2 md:p-2.5 rounded-xl bg-rose-50 text-rose-500 hover:bg-rose-500 hover:text-white transition-all group"
                  title="Logout"
                >
                  <LogOut size={16} className="group-hover:-translate-x-0.5 transition-transform" />
                </button>
              </div>
            ) : (
              <div className="hidden md:flex items-center gap-2">
                <Link href="/auth/login">
                  <Button variant="ghost" className="text-[10px] font-black uppercase tracking-widest text-slate-600 rounded-xl">
                    Sign In
                  </Button>
                </Link>
                <Link href="/auth/register">
                  <Button className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg px-5 py-4 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all active:scale-95">
                    Get Started
                  </Button>
                </Link>
              </div>
            )}

            {/* MOBILE MENU BUTTON */}
            <button 
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden p-2.5 rounded-xl bg-slate-900 text-white active:scale-90 transition-all"
            >
              {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>

        {/* MOBILE MENU DROPDOWN */}
        <div className={cn(
          "md:hidden overflow-hidden transition-all duration-300 ease-in-out",
          isMobileMenuOpen ? "max-h-[400px] opacity-100 mt-4 pb-4" : "max-h-0 opacity-0"
        )}>
          <div className="flex flex-col space-y-1">
            <NavLink href="/" mobile>Home</NavLink>
            {isAuthenticated ? (
              <>
                <NavLink href="/dashboard" mobile>Dashboard</NavLink>
                <NavLink href="/chat" mobile>Chat</NavLink>
              </>
            ) : (
              <>
                <NavLink href="#features" mobile>Features</NavLink>
                <div className="grid grid-cols-2 gap-3 p-4 pt-6">
                  <Link href="/auth/login" className="w-full">
                    <Button variant="outline" className="w-full h-12 rounded-xl font-black uppercase tracking-widest text-[10px] italic">
                      Sign In
                    </Button>
                  </Link>
                  <Link href="/auth/register" className="w-full">
                    <Button className="w-full h-12 bg-indigo-600 text-white rounded-xl font-black uppercase tracking-widest text-[10px] italic">
                      Register
                    </Button>
                  </Link>
                </div>
              </>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}