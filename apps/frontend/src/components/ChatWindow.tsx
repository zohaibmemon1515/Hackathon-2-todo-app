"use client";

import { useState, useRef, useEffect } from "react";
import {
  SendHorizontal,
  Zap,
  Plus,
  Menu,
  Activity,
  UserCircle,
  Bot,
  Terminal,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import { sendMessage, getUserConversations } from "../services/api";

// --- MESSAGE COMPONENT ---
const Message = ({ role, content, timestamp }: any) => {
  const isUser = role === "user";
  return (
    <div
      className={cn(
        "flex w-full mb-8 group animate-in fade-in slide-in-from-bottom-2",
        isUser ? "justify-end" : "justify-start",
      )}
    >
      <div
        className={cn(
          "flex gap-4 max-w-[85%] md:max-w-[75%]",
          isUser ? "flex-row-reverse" : "flex-row",
        )}
      >
        {/* Avatar matching Dashboard Style */}
        <div
          className={cn(
            "h-10 w-10 shrink-0 rounded-xl flex items-center justify-center border transition-all duration-500 group-hover:rotate-6 shadow-lg",
            isUser
              ? "bg-slate-900 border-slate-800 text-white"
              : "bg-white dark:bg-slate-800 border-slate-100 dark:border-slate-700 text-indigo-600",
          )}
        >
          {isUser ? <UserCircle size={20} /> : <Bot size={20} />}
        </div>

        {/* Bubble */}
        <div
          className={cn(
            "flex flex-col gap-2",
            isUser ? "items-end" : "items-start",
          )}
        >
          <div
            className={cn(
              "p-5 rounded-[1.8rem] border-b-[6px] transition-all",
              isUser
                ? "bg-slate-900 dark:bg-indigo-600 text-white rounded-tr-none border-slate-800 dark:border-indigo-700 shadow-xl shadow-slate-200 dark:shadow-none"
                : "bg-white dark:bg-[#11141D] text-slate-800 dark:text-slate-200 rounded-tl-none border-slate-100 dark:border-slate-800 shadow-sm",
            )}
          >
            <p className="text-[14px] font-bold tracking-tight leading-relaxed whitespace-pre-wrap">
              {content}
            </p>
          </div>
          <div className="flex items-center gap-2 px-2 opacity-50">
            <span className="text-[8px] font-black uppercase tracking-[0.2em] italic">
              {format(new Date(timestamp), "HH:mm:ss")}
            </span>
            <div
              className={cn(
                "h-1 w-1 rounded-full",
                isUser ? "bg-indigo-400" : "bg-emerald-500 animate-pulse",
              )}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

// --- CONVERSATION LIST COMPONENT ---
const ConversationList = ({ conversations, currentId, onSelect }: any) => {
  const arr = Array.isArray(conversations)
    ? conversations
    : conversations?.conversations || [];
  return (
    <div className="px-4 py-6 space-y-2">
      <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.3em] px-4 mb-4 italic">
        Neural Sessions
      </p>
      {arr.map((conv: any) => {
        const isActive = currentId === conv.id.toString();
        return (
          <button
            key={conv.id}
            onClick={() => onSelect(conv.id)}
            className={cn(
              "w-full flex items-center justify-between px-5 py-4 rounded-2xl transition-all duration-300 group border text-left",
              isActive
                ? "bg-slate-900 dark:bg-indigo-600 border-slate-800 dark:border-indigo-500 text-white shadow-xl scale-[1.02]"
                : "bg-white dark:bg-slate-900/50 border-slate-50 dark:border-slate-800/50 text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900",
            )}
          >
            <div className="flex flex-col gap-1 overflow-hidden">
              <span className="text-[12px] font-black uppercase tracking-tighter truncate italic">
                {conv.title || `SESSION_ID_${conv.id}`}
              </span>
              <div className="flex items-center gap-1.5 opacity-60">
                <Activity
                  size={10}
                  className={isActive ? "text-indigo-400" : "text-emerald-500"}
                />
                <span className="text-[8px] font-bold uppercase tracking-widest">
                  Active Link
                </span>
              </div>
            </div>
            {isActive && (
              <Zap
                size={12}
                className="text-indigo-400 fill-current animate-pulse"
              />
            )}
          </button>
        );
      })}
    </div>
  );
};

// --- MAIN CHAT WINDOW ---
export const ChatWindow = ({ userId }: { userId: string }) => {
  const [messages, setMessages] = useState<any[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState([]);
  const [currentId, setCurrentId] = useState<string | null>(null);
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
  useEffect(() => {
    loadConvos();
  }, []);

  const loadConvos = async () => {
    try {
      const data = await getUserConversations(userId);
      setConversations(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMsg = {
      id: Date.now().toString(),
      role: "user",
      content: inputValue,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputValue("");
    setIsLoading(true);

    try {
      const res = await sendMessage(userId, inputValue, currentId ?? undefined);
      if (res.conversation_id && !currentId) {
        setCurrentId(res.conversation_id);
        loadConvos();
      }
      setMessages((prev) => [
        ...prev,
        {
          id: `ai-${Date.now()}`,
          role: "assistant",
          content: res.response,
          timestamp: new Date(),
        },
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-full w-full bg-[#FDFDFD] dark:bg-[#0B0E14] overflow-hidden">
      {/* INTERNAL CHAT SIDEBAR */}
      <aside
        className={cn(
          "fixed lg:relative inset-y-0 left-0 z-30 bg-white dark:bg-[#11141D] border-r border-slate-100 dark:border-slate-800/50 transition-all duration-300 flex flex-col shadow-2xl lg:shadow-none",
          isSidebarOpen
            ? "w-80 translate-x-0"
            : "w-0 -translate-x-full lg:translate-x-0 lg:w-0",
        )}
      >
        <div className="p-6 border-b border-slate-50 dark:border-slate-800/50 flex justify-between items-center min-w-[320px]">
          <div className="flex items-center gap-2">
            <Terminal size={18} className="text-indigo-600" />
            <h2 className="font-black text-slate-900 dark:text-white text-sm uppercase tracking-widest italic">
              History
            </h2>
          </div>
          <button
            onClick={() => {
              setMessages([]);
              setCurrentId(null);
            }}
            className="p-2 bg-slate-900 dark:bg-indigo-600 text-white rounded-xl hover:scale-105 active:scale-95 transition-all shadow-lg"
          >
            <Plus size={16} strokeWidth={3} />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto custom-scrollbar min-w-[320px]">
          <ConversationList
            conversations={conversations}
            currentId={currentId}
            onSelect={(id: any) => {
              setCurrentId(id.toString());
              if (window.innerWidth < 1024) setSidebarOpen(false);
            }}
          />
        </div>
      </aside>

      {/* CHAT MAIN CONTENT */}
      <div className="flex-1 flex flex-col min-w-0 bg-[#F8FAFC]/50 dark:bg-[#0B0E14] relative">
        {/* Toggle button for mobile */}
        <button
          onClick={() => setSidebarOpen(!isSidebarOpen)}
          className="lg:hidden absolute top-4 left-4 z-20 p-3 bg-white dark:bg-slate-800 rounded-2xl shadow-md border border-slate-100 dark:border-slate-700"
        >
          <Menu size={20} className="text-slate-600 dark:text-slate-300" />
        </button>

        {/* MESSAGES AREA */}
        <div className="flex-1 overflow-y-auto p-6 md:p-10 custom-scrollbar">
          <div className="max-w-4xl mx-auto w-full">
            {messages.length === 0 ? (
              <div className="h-[60vh] flex flex-col items-center justify-center space-y-6">
                <div className="h-20 w-20 bg-linear-to-tr from-indigo-600 to-violet-600 rounded-[2rem] flex items-center justify-center shadow-2xl shadow-indigo-200 dark:shadow-none rotate-6">
                  <Zap size={36} className="text-white fill-current" />
                </div>
                <div className="text-center">
                  <h3 className="text-3xl font-black text-slate-900 dark:text-white italic tracking-tighter uppercase leading-none">
                    TASK<span className="text-indigo-600">MASTER</span> CORE
                  </h3>
                  <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.4em] mt-3 animate-pulse">
                    Awaiting Input Protocol
                  </p>
                </div>
              </div>
            ) : (
              messages.map((m) => <Message key={m.id} {...m} />)
            )}
            <div ref={scrollRef} />
          </div>
        </div>

        {/* INPUT BOX - THE "CONTROL CAPSULE" */}
        <div className="p-6 md:p-10 bg-linear-to-t from-[#FDFDFD] dark:from-[#0B0E14] via-[#FDFDFD]/90 dark:via-[#0B0E14]/90 to-transparent">
          <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative">
            <div className="group relative flex items-center transition-all duration-500">
              <div className="absolute left-6 text-slate-400 group-focus-within:text-indigo-600 transition-colors">
                <Terminal size={18} />
              </div>
              <input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="ENTER COMMAND OR QUERY..."
                className="w-full h-16 md:h-20 bg-white dark:bg-[#11141D] border-2 border-slate-100 dark:border-slate-800 rounded-[2.2rem] pl-16 pr-24 text-sm font-black tracking-widest focus:outline-none focus:border-indigo-600 focus:ring-8 focus:ring-indigo-600/5 transition-all shadow-2xl shadow-slate-200/50 dark:shadow-none uppercase italic text-slate-800 dark:text-white placeholder:text-slate-300"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                className="absolute right-3 h-12 md:h-14 px-6 md:px-10 bg-slate-900 dark:bg-indigo-600 text-white rounded-[1.8rem] hover:bg-indigo-700 active:scale-95 transition-all flex items-center gap-2 shadow-lg disabled:opacity-50"
              >
                {isLoading ? (
                  <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <>
                    <span className="hidden md:inline text-[10px] font-black uppercase tracking-widest italic">
                      Execute
                    </span>
                    <SendHorizontal size={18} />
                  </>
                )}
              </button>
            </div>
          </form>
          <div className="mt-4 flex justify-center gap-8 opacity-40">
            <div className="flex items-center gap-2 text-[8px] font-black uppercase tracking-[0.2em] text-slate-500">
              <div className="h-1 w-1 bg-emerald-500 rounded-full animate-pulse" />{" "}
              Neural Link: Online
            </div>
            <div className="flex items-center gap-2 text-[8px] font-black uppercase tracking-[0.2em] text-slate-500">
              <div className="h-1 w-1 bg-indigo-500 rounded-full" /> Encryption:
              AES-256
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
