'use client';

import { Activity, Zap, X, Terminal } from "lucide-react";
import { cn } from "@/lib/utils";

export const ConversationList = ({ conversations, currentId, onSelect, onMobileSelect }: any) => {
  const arr = Array.isArray(conversations) ? conversations : (conversations?.conversations || []);

  return (
    <div className="flex flex-col h-full bg-white dark:bg-[#11141D]">
      {/* Sidebar Header with Close Button */}
      <div className="p-6 border-b border-slate-50 dark:border-slate-800/50 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Terminal size={18} className="text-indigo-600" />
          <h2 className="font-black text-slate-900 dark:text-white text-sm uppercase tracking-widest italic">History</h2>
        </div>
        <button 
          onClick={onMobileSelect}
          className="lg:hidden p-2 rounded-lg bg-slate-50 dark:bg-slate-800 text-slate-500"
        >
          <X size={20} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-2 custom-scrollbar">
        <p className="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.3em] px-4 mb-4 italic">
          Neural Sessions
        </p>
        
        {arr.length === 0 ? (
          <div className="px-4 py-8 text-center border-2 border-dashed border-slate-100 dark:border-slate-800 rounded-3xl">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">No Active Links</p>
          </div>
        ) : (
          arr.map((conv: any) => {
            const isActive = currentId === conv.id.toString();
            return (
              <button
                key={conv.id}
                onClick={() => {
                  onSelect(conv.id);
                  if (onMobileSelect) onMobileSelect();
                }}
                className={cn(
                  "w-full flex items-center justify-between px-5 py-4 rounded-2xl transition-all duration-300 group border text-left active:scale-[0.98]",
                  isActive
                    ? "bg-slate-900 dark:bg-indigo-600 border-slate-800 dark:border-indigo-500 text-white shadow-xl scale-[1.02]"
                    : "bg-white dark:bg-slate-900/50 border-slate-50 dark:border-slate-800/50 text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900"
                )}
              >
                <div className="flex flex-col gap-1 overflow-hidden">
                  <span className="text-[12px] font-black uppercase tracking-tighter truncate italic">
                    {conv.title || `LINK_0${conv.id}`}
                  </span>
                  <div className="flex items-center gap-1.5 opacity-60">
                    <Activity size={10} className={isActive ? "text-indigo-400" : "text-emerald-500"} />
                    <span className="text-[8px] font-bold uppercase tracking-widest">Synced</span>
                  </div>
                </div>
                {isActive && <Zap size={12} className="text-indigo-400 fill-current animate-pulse" />}
              </button>
            );
          })
        )}
      </div>
    </div>
  );
};