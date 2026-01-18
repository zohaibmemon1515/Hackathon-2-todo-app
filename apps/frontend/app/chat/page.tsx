'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ChatWindow } from '@/components/ChatWindow';
import { useAuth } from '@/contexts/auth-context';
import { Zap, Activity, UserCircle, Bell, Menu } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function ChatPage() {
  const router = useRouter();
  const { user, loading, isAuthenticated } = useAuth();
  const [isSidebarOpen, setSidebarOpen] = useState(false);

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
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <div className="flex flex-col h-screen bg-[#FDFDFD] dark:bg-[#0B0E14] overflow-hidden">
      {/* HEADER */}
      <header className="h-20 lg:h-24 flex items-center justify-between px-4 lg:px-8 bg-white/60 dark:bg-[#0B0E14]/60 backdrop-blur-xl border-b border-slate-50 dark:border-slate-800/50 sticky top-0 z-[60]">
        <div className="flex items-center gap-3">
          <button 
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden p-2.5 rounded-xl bg-slate-900 text-white dark:bg-indigo-600 active:scale-90 transition-all shadow-lg"
          >
            <Menu size={20} />
          </button>

          <div className="flex items-center gap-2 lg:gap-3 group">
            <div className="h-10 w-10 bg-linear-to-tr from-indigo-600 to-violet-600 rounded-xl flex items-center justify-center shadow-lg transform group-hover:rotate-6 transition-all duration-300">
              <Zap size={20} className="text-white fill-current" />
            </div>
            <div className="flex flex-col">
              <h1 className="text-base lg:text-xl font-black tracking-tighter text-slate-800 dark:text-white leading-none italic uppercase">
                TASK<span className="text-indigo-600">MASTER</span> <span className="hidden xs:inline-block text-[10px] ml-1 bg-slate-900 text-white px-1.5 py-0.5 rounded-sm not-italic">AI</span>
              </h1>
              <div className="flex items-center gap-1.5 mt-1">
                <span className="flex h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest italic flex items-center gap-1">
                  <Activity size={8} className="text-emerald-500" /> Engine Active
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3 lg:gap-4">
          <button className="relative p-3 rounded-2xl bg-white dark:bg-slate-900 text-slate-400 border border-slate-100 dark:border-slate-800 shadow-sm">
            <Bell size={18} />
            <span className="absolute top-2 right-2 w-2 h-2 bg-indigo-600 rounded-full ring-4 ring-white dark:ring-slate-900"></span>
          </button>
          <div className="h-10 w-10 lg:h-12 lg:w-12 rounded-xl lg:rounded-2xl bg-linear-to-tr from-indigo-500 to-pink-500 p-0.5 shadow-lg">
            <div className="h-full w-full rounded-[0.7rem] lg:rounded-[0.9rem] bg-white dark:bg-slate-900 flex items-center justify-center">
              <UserCircle size={24} className="text-slate-300" />
            </div>
          </div>
        </div>
      </header>

      {/* CHAT AREA CONTAINER */}
      <main className="flex-1 flex overflow-hidden relative">
        <ChatWindow 
          userId={user?.id?.toString() || ''} 
          isSidebarOpen={isSidebarOpen} 
          setSidebarOpen={setSidebarOpen} 
        />
      </main>

      {/* FOOTER */}
      <footer className="h-8 bg-slate-950 text-white flex items-center px-8 justify-between border-t border-white/5">
        <span className="text-[8px] font-black uppercase tracking-[0.3em] text-emerald-400 flex items-center gap-2">
          <span className="h-1 w-1 bg-emerald-400 rounded-full shadow-[0_0_5px_#34d399]" /> Encrypted Connection
        </span>
        <div className="text-[8px] font-black uppercase tracking-[0.3em] opacity-30">© 2026 TASKMASTER</div>
      </footer>
    </div>
  );
}