"use client";

import { useState, useRef, useEffect } from "react";
import { SendHorizontal, Zap, Plus, Bot, UserCircle, Terminal } from "lucide-react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import { sendMessage, getUserConversations } from "../services/api";
import { ConversationList } from "./ConversationList";

export const ChatWindow = ({ userId, isSidebarOpen, setSidebarOpen }: any) => {
  const [messages, setMessages] = useState<any[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState([]);
  const [currentId, setCurrentId] = useState<string | undefined>(undefined);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => { scrollRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);
  useEffect(() => { loadConvos(); }, []);

  const loadConvos = async () => {
    try {
      const data = await getUserConversations(userId);
      setConversations(data);
    } catch (err) { console.error(err); }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMsg = { id: Date.now().toString(), role: "user", content: inputValue, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInputValue("");
    setIsLoading(true);

    try {
      const res = await sendMessage(userId, inputValue, currentId);
      if (res.conversation_id && !currentId) {
        setCurrentId(res.conversation_id);
        loadConvos();
      }
      setMessages(prev => [...prev, { id: `ai-${Date.now()}`, role: "assistant", content: res.response, timestamp: new Date() }]);
    } catch (err) { console.error(err); } finally { setIsLoading(false); }
  };

  return (
    <div className="flex h-full w-full bg-[#FDFDFD] dark:bg-[#0B0E14] overflow-hidden relative">
      
      {/* MOBILE OVERLAY */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[70] lg:hidden" 
          onClick={() => setSidebarOpen(false)} 
        />
      )}

      {/* SIDEBAR */}
      <aside className={cn(
        "fixed inset-y-0 left-0 z-[80] w-80 lg:relative lg:translate-x-0 transition-all duration-300 transform border-r border-slate-100 dark:border-slate-800/50 shadow-2xl lg:shadow-none",
        isSidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex flex-col h-full bg-white dark:bg-[#11141D]">
          <div className="p-4 border-b border-slate-50 dark:border-slate-800/50">
            <button 
              onClick={() => { setMessages([]); setCurrentId(undefined); if(window.innerWidth < 1024) setSidebarOpen(false); }}
              className="w-full flex items-center justify-center gap-2 bg-slate-900 dark:bg-indigo-600 text-white py-4 rounded-2xl font-black text-[10px] uppercase tracking-[0.2em] shadow-lg hover:scale-[1.02] active:scale-95 transition-all italic"
            >
              <Plus size={16} strokeWidth={3} /> New session
            </button>
          </div>
          <div className="flex-1 overflow-hidden">
            <ConversationList 
              conversations={conversations} 
              currentId={currentId} 
              onSelect={(id: any) => setCurrentId(id.toString())}
              onMobileSelect={() => setSidebarOpen(false)}
            />
          </div>
        </div>
      </aside>

      {/* CHAT MAIN */}
      <div className="flex-1 flex flex-col min-w-0 bg-[#F8FAFC]/50 dark:bg-[#0B0E14] relative">
        <div className="flex-1 overflow-y-auto p-4 md:p-10 custom-scrollbar">
          <div className="max-w-4xl mx-auto w-full">
            {messages.length === 0 ? (
              <div className="h-[60vh] flex flex-col items-center justify-center space-y-6">
                <div className="h-24 w-24 bg-linear-to-tr from-indigo-600 to-violet-600 rounded-[2.5rem] flex items-center justify-center shadow-2xl rotate-6 animate-in zoom-in duration-500">
                  <Zap size={40} className="text-white fill-current" />
                </div>
                <div className="text-center">
                  <h3 className="text-3xl font-black text-slate-900 dark:text-white italic tracking-tighter uppercase leading-none">
                    TASK<span className="text-indigo-600">MASTER</span> CORE
                  </h3>
                  <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.4em] mt-3 animate-pulse italic">Awaiting neural link protocol...</p>
                </div>
              </div>
            ) : (
              messages.map((m) => <Message key={m.id} {...m} />)
            )}
            <div ref={scrollRef} />
          </div>
        </div>

        {/* INPUT BOX */}
        <div className="p-4 md:p-10 bg-linear-to-t from-white dark:from-[#0B0E14] via-white/90 dark:via-[#0B0E14]/90 to-transparent">
          <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative group">
            <div className="relative flex items-center transition-all duration-500">
              <div className="absolute left-6 text-slate-400 group-focus-within:text-indigo-600 hidden xs:block">
                <Terminal size={18} />
              </div>
              <input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="ENTER COMMAND..."
                className="w-full h-16 md:h-20 bg-white dark:bg-[#11141D] border-2 border-slate-100 dark:border-slate-800 rounded-[1.8rem] md:rounded-[2.2rem] pl-6 xs:pl-16 pr-20 md:pr-24 text-xs md:text-sm font-black tracking-widest focus:outline-none focus:border-indigo-600 focus:ring-8 focus:ring-indigo-600/5 transition-all shadow-2xl dark:shadow-none uppercase italic text-slate-800 dark:text-white"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                className="absolute right-2 md:right-3 h-12 md:h-14 px-4 md:px-10 bg-slate-900 dark:bg-indigo-600 text-white rounded-[1.4rem] md:rounded-[1.8rem] transition-all flex items-center gap-2 shadow-lg disabled:opacity-50"
              >
                {isLoading ? (
                  <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <SendHorizontal size={18} />
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

const Message = ({ role, content, timestamp }: any) => {
  const isUser = role === "user";
  return (
    <div className={cn("flex w-full mb-8 group animate-in fade-in slide-in-from-bottom-2", isUser ? "justify-end" : "justify-start")}>
      <div className={cn("flex gap-4 max-w-[95%] md:max-w-[75%]", isUser ? "flex-row-reverse" : "flex-row")}>
        <div className={cn("h-10 w-10 shrink-0 rounded-xl flex items-center justify-center border shadow-lg transform transition-transform group-hover:rotate-6", isUser ? "bg-slate-900 text-white" : "bg-white dark:bg-slate-800 text-indigo-600")}>
          {isUser ? <UserCircle size={20} /> : <Bot size={20} />}
        </div>
        <div className={cn("flex flex-col gap-2", isUser ? "items-end" : "items-start")}>
          <div className={cn("p-4 md:p-5 rounded-[1.6rem] md:rounded-[1.8rem] border-b-[6px] shadow-md", isUser ? "bg-slate-900 dark:bg-indigo-600 text-white rounded-tr-none border-slate-800 dark:border-indigo-700 shadow-slate-200 dark:shadow-none" : "bg-white dark:bg-[#11141D] text-slate-800 dark:text-slate-200 rounded-tl-none border-slate-100 dark:border-slate-800")}>
            <p className="text-[13px] md:text-[14px] font-bold tracking-tight leading-relaxed">{content}</p>
          </div>
          <span className="text-[8px] font-black opacity-40 uppercase tracking-widest px-2 italic">{format(new Date(timestamp), "HH:mm:ss")}</span>
        </div>
      </div>
    </div>
  );
};