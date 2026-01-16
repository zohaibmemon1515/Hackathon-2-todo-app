'use client';

import { format } from 'date-fns';
import { UserCircle, Bot } from "lucide-react";

export const Message = ({ role, content, timestamp }: any) => {
  const isUser = role === 'user';
  
  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-8 group`}>
      <div className={`flex gap-3 max-w-[85%] md:max-w-[70%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        
        {/* Avatar matching Dashboard Style */}
        <div className={`h-10 w-10 shrink-0 rounded-xl flex items-center justify-center border transition-transform group-hover:rotate-3 ${
          isUser ? 'bg-slate-900 border-slate-800' : 'bg-white dark:bg-slate-800 border-slate-100 dark:border-slate-700 shadow-sm'
        }`}>
          {isUser ? <UserCircle size={20} className="text-white" /> : <Bot size={20} className="text-indigo-600" />}
        </div>

        {/* Bubble */}
        <div className={`flex flex-col gap-1.5 ${isUser ? 'items-end' : 'items-start'}`}>
          <div className={`p-5 rounded-[1.8rem] transition-all border-b-4 ${
            isUser 
              ? 'bg-slate-900 dark:bg-indigo-600 text-white rounded-tr-none border-slate-800 dark:border-indigo-700 shadow-xl' 
              : 'bg-white dark:bg-[#11141D] text-slate-800 dark:text-slate-200 rounded-tl-none border-slate-100 dark:border-slate-800 shadow-sm'
          }`}>
            <p className="text-sm font-bold tracking-tight leading-relaxed italic-none">
              {content}
            </p>
          </div>
          
          <div className="flex items-center gap-2 px-2">
            <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest italic">
              {format(new Date(timestamp), 'HH:mm')}
            </span>
            <div className={`h-1 w-1 rounded-full ${isUser ? 'bg-indigo-500' : 'bg-emerald-500 animate-pulse'}`} />
          </div>
        </div>
      </div>
    </div>
  );
};