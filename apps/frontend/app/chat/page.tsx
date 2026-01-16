'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ChatWindow } from '@/components/ChatWindow';
import { useAuth } from '@/contexts/auth-context';
import { Zap, Activity, UserCircle, Bell } from 'lucide-react';

export default function ChatPage() {
  const router = useRouter();
  const { user, loading, isAuthenticated } = useAuth();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-white dark:bg-[#0B0E14]">
        <div className="relative flex items-center justify-center">
          <div className="h-24 w-24 border-[6px] border-slate-50 dark:border-slate-800 rounded-[2.5rem] rotate-45"></div>
          <div className="absolute h-24 w-24 border-[6px] border-indigo-600 border-t-transparent rounded-[2.5rem] rotate-45 animate-spin"></div>
          <Zap size={32} className="absolute text-indigo-600 animate-pulse fill-current" />
        </div>
        <p className="mt-10 text-sm font-black text-slate-500 uppercase tracking-[0.3em] animate-pulse italic">
          Verifying Neural Identity...
        </p>
      </div>
    );
  }

  if (!isAuthenticated) return null;

  const userId = user?.id?.toString() || '';

  return (
    <div className="flex flex-col h-screen bg-[#FDFDFD] dark:bg-[#0B0E14] overflow-hidden">
      {/* ADVANCED HEADER: Dashboard Style */}
      <header className="h-24 flex items-center justify-between px-8 bg-white/60 dark:bg-[#0B0E14]/60 backdrop-blur-xl border-b border-slate-50 dark:border-slate-800/50 sticky top-0 z-40">
        
        {/* LOGO SECTION - Identical to Dashboard */}
        <div className="flex items-center gap-3 group cursor-default">
          <div className="h-10 w-10 bg-linear-to-tr from-indigo-600 to-violet-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-100 dark:shadow-none transform group-hover:rotate-6 transition-transform duration-300">
            <Zap size={20} className="text-white fill-current" />
          </div>
          <div className="flex flex-col">
            <h1 className="text-xl font-black tracking-tighter text-slate-800 dark:text-white leading-none italic uppercase">
              TASK<span className="text-indigo-600">MASTER</span> <span className="text-[10px] ml-1 bg-slate-900 text-white px-2 py-0.5 rounded-sm not-italic">AI</span>
            </h1>
            <div className="flex items-center gap-1.5 mt-1">
              <span className="flex h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest italic flex items-center gap-1">
                <Activity size={10} className="text-emerald-500" /> Core Engine Active
              </span>
            </div>
          </div>
        </div>

        {/* RIGHT ACTIONS: Notifications & User Avatar */}
        <div className="flex items-center gap-4">
          <div className="hidden md:flex flex-col items-end mr-2">
            <p className="text-xs font-black text-slate-800 dark:text-slate-200 tracking-tight uppercase italic">
              {user?.first_name || 'Operator'}
            </p>
            <p className="text-[9px] font-bold text-emerald-500 uppercase tracking-tighter">SECURE_LINK_STABLE</p>
          </div>

          <button className="relative p-3 rounded-2xl bg-white dark:bg-slate-900 text-slate-400 border border-slate-100 dark:border-slate-800 shadow-sm transition-all active:scale-90">
            <Bell size={18} />
            <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-indigo-600 rounded-full ring-4 ring-white dark:ring-slate-900 animate-bounce"></span>
          </button>

          <div className="h-12 w-12 rounded-2xl bg-linear-to-tr from-indigo-500 via-purple-500 to-pink-500 p-0.5 shadow-lg shadow-indigo-100 dark:shadow-none transition-all hover:scale-105">
            <div className="h-full w-full rounded-[0.9rem] bg-white dark:bg-slate-900 flex items-center justify-center overflow-hidden">
              <UserCircle size={28} className="text-slate-300" />
            </div>
          </div>
        </div>
      </header>

      {/* CHAT AREA: Full height layout */}
      <main className="flex-1 overflow-hidden bg-[#F8FAFC]/50 dark:bg-[#0B0E14] relative">
        <ChatWindow userId={userId} />
      </main>

      {/* BOTTOM STATUS BAR: Pro Look */}
      <footer className="h-7 bg-slate-950 text-white flex items-center px-8 justify-between border-t border-white/5">
        <div className="flex items-center gap-6">
          <span className="text-[8px] font-black uppercase tracking-[0.3em] text-emerald-400 flex items-center gap-2">
            <span className="h-1 w-1 bg-emerald-400 rounded-full shadow-[0_0_5px_#34d399]" /> 
            Protocol: Encrypted
          </span>
          <span className="text-[8px] font-black uppercase tracking-[0.3em] opacity-40 italic hidden sm:block">
            Buffer: Optimized (0.02ms)
          </span>
        </div>
        <div className="text-[8px] font-black uppercase tracking-[0.3em] opacity-30">
          © 2026 TaskMaster Neural Network
        </div>
      </footer>
    </div>
  );
}