'use client';

import { Activity } from "lucide-react";

export const ConversationList = ({ conversations, currentConversationId, onSelectConversation }: any) => {
  const conversationsArray = Array.isArray(conversations) ? conversations : (conversations?.conversations || []);

  return (
    <div className="px-4 py-6 space-y-2">
      <p className="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] px-3 mb-4">
        Active Sessions
      </p>
      {conversationsArray.map((conv: any) => {
        const isActive = currentConversationId === conv.id.toString();
        return (
          <button
            key={conv.id}
            onClick={() => onSelectConversation?.(conv.id)}
            className={`w-full flex items-center justify-between px-4 py-4 rounded-2xl text-sm font-bold transition-all duration-300 group relative ${
              isActive
                ? "bg-slate-900 text-white shadow-xl dark:bg-indigo-600"
                : "text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-white"
            }`}
          >
            <div className="flex flex-col items-start gap-1 overflow-hidden">
              <span className="truncate w-full text-[13px] tracking-tight uppercase italic">
                {conv.title || `Session_${conv.id}`}
              </span>
              <div className="flex items-center gap-1.5 opacity-60">
                <Activity size={10} className={isActive ? "text-indigo-400" : "text-slate-400"} />
                <span className="text-[9px] font-black tracking-widest uppercase">Stable</span>
              </div>
            </div>
            {isActive && <div className="h-1.5 w-1.5 bg-indigo-400 rounded-full animate-pulse shadow-[0_0_8px_rgba(129,140,248,0.8)]" />}
          </button>
        );
      })}
    </div>
  );
};