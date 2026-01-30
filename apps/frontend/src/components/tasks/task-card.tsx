"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Pencil, Trash2, Check, Clock, Tag, Sparkles } from "lucide-react";
import { Task } from "@/types/task";
import TaskEditForm from "./task-edit-form";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

export default function TaskCard({
  task,
  onTaskUpdated,
  onTaskDeleted,
}: {
  task: Task;
  onTaskUpdated: any;
  onTaskDeleted: any;
}) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Priority themes
  const themes = {
    high: {
      card: "border-l-rose-500 bg-gradient-to-br from-rose-50/20 to-rose-50/10",
      glow: "group-hover:shadow-[0_12px_25px_-5px_rgba(239,68,68,0.4)]",
      gradient: "bg-gradient-to-r from-rose-400 via-pink-400 to-rose-500",
    },
    medium: {
      card: "border-l-amber-500 bg-gradient-to-br from-amber-50/20 to-amber-50/10",
      glow: "group-hover:shadow-[0_12px_25px_-5px_rgba(251,191,36,0.4)]",
      gradient: "bg-gradient-to-r from-amber-400 via-yellow-400 to-amber-500",
    },
    low: {
      card: "border-l-emerald-500 bg-gradient-to-br from-emerald-50/20 to-emerald-50/10",
      glow: "group-hover:shadow-[0_12px_25px_-5px_rgba(34,197,94,0.4)]",
      gradient:
        "bg-gradient-to-r from-emerald-400 via-green-400 to-emerald-500",
    },
  };

  const style =
    themes[task.priority?.toLowerCase() as keyof typeof themes] || themes.low;
  const priorityInitial = task.priority?.charAt(0).toUpperCase() || "L";

  return (
    <>
      <motion.div
        layout
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        whileHover={{ scale: 1.04 }}
        className={`relative group bg-white/30 backdrop-blur-xl rounded-3xl border border-slate-100 border-l-[6px] ${style.card} transition-all duration-300 hover:shadow-2xl ${style.glow} overflow-hidden`}
      >
        {/* High Priority Sparkle */}
        {task.priority?.toLowerCase() === "high" && (
          <motion.div
            className="absolute top-2 right-2"
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <Sparkles size={18} className="text-rose-400/70" />
          </motion.div>
        )}

        {/* Card Content */}
        <div
          className={`p-5 flex flex-col gap-4 ${task.is_completed ? "opacity-80" : ""}`}
        >
          {/* TOP: Priority & Actions */}
          <div className="flex items-center justify-between">
            <div
              title={task.priority}
              className="w-7 h-7 rounded-lg flex items-center justify-center font-black text-[11px] shrink-0 shadow-md"
            >
              <motion.div
                className={`text-transparent bg-clip-text font-extrabold ${style.gradient}`}
                animate={{ backgroundPositionX: [0, 100] }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  repeatType: "mirror",
                }}
              >
                {priorityInitial}
              </motion.div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <button
                onClick={() => setIsModalOpen(true)}
                className="w-9 h-9 rounded-lg flex items-center justify-center text-indigo-500 hover:bg-indigo-100 transition-all"
              >
                <Pencil size={16} />
              </button>
              <button
                onClick={() => onTaskDeleted(task.id)}
                className="w-9 h-9 rounded-lg flex items-center justify-center text-rose-500 hover:bg-rose-100 transition-all"
              >
                <Trash2 size={16} />
              </button>
            </div>
          </div>

          {/* MAIN CONTENT WRAPPER */}
          <div className="flex flex-col w-full gap-4">
            {/* UPPER PART: Title + Description & Status Toggle */}
            <div className="flex items-start gap-4">
              {/* 1. Title & Description (Ziada Area) */}
              <div className="min-w-0 flex-1 space-y-1">
                <h3
                  className={`text-base md:text-lg font-bold leading-tight transition-all duration-300 ${
                    task.is_completed
                      ? "text-slate-400 line-through"
                      : "text-slate-900"
                  }`}
                >
                  {task.title}
                </h3>

                {task.description && (
                  <p className="text-sm text-slate-500 line-clamp-1 group-hover:line-clamp-none transition-all duration-500 ease-in-out">
                    {task.description}
                  </p>
                )}
              </div>

              {/* 2. Toggle Switch (Kam Area - Fixed Width) */}
              <div className="shrink-0 pt-1">
                <button
  onClick={() => onTaskUpdated({ ...task, is_completed: !task.is_completed })}
  className="relative mt-0.5 shrink-0 group/toggle block"
>
  {/* Track: Width reduced to w-10 (40px) or w-9 (36px) */}
  <div
    className={`
      w-10 h-5.5 rounded-full transition-all duration-500 flex items-center px-0.5
      ${
        task.is_completed
          ? "bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.3)]"
          : "bg-slate-200 shadow-inner group-hover/toggle:bg-slate-300"
      }
    `}
  >
    {/* Animated Thumb: Size slightly smaller to fit w-10 */}
    <motion.div
      layout
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 20,
      }}
      animate={{
        x: task.is_completed ? 18 : 0, // Distance adjusted for smaller width
        rotate: task.is_completed ? 360 : 0,
      }}
      className="w-4 h-4 bg-white rounded-full shadow-sm flex items-center justify-center"
    >
      <AnimatePresence mode="wait">
        {task.is_completed ? (
          <motion.div
            key="check"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
          >
            <Check
              size={9}
              strokeWidth={5}
              className="text-emerald-600"
            />
          </motion.div>
        ) : (
          <div className="w-1 h-1 rounded-full bg-slate-300" />
        )}
      </AnimatePresence>
    </motion.div>
  </div>

  <span className="sr-only">Toggle Complete</span>
</button>
              </div>
            </div>

            {/* LOWER PART: Full Width Tags */}
            {task.tags && task.tags.length > 0 && (
              <div className="w-full pt-3 border-t border-slate-50">
                <div className="flex gap-2">
                  {task.tags.map((tag, i) => (
                    <motion.span
                      key={i}
                      whileHover={{ scale: 1.05, backgroundColor: "#EEF2FF" }}
                      className="inline-flex items-center gap-1.5 bg-slate-50 text-slate-600 border border-slate-100 text-[11px] font-semibold px-3 py-1 rounded-lg cursor-pointer transition-colors"
                    >
                      <Tag size={10} className="text-indigo-500" />
                      {tag}
                    </motion.span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* FOOTER */}
          <div className="flex flex-wrap items-center justify-between pt-3 border-t border-slate-100 gap-2">
            <div className="flex items-center gap-3 text-slate-400 flex-wrap text-[11px] font-bold uppercase tracking-tight">
              {task.due_date && (
                <div className="flex items-center gap-1">
                  <Clock size={12} />
                  {new Date(task.due_date).toLocaleDateString("en-GB", {
                    day: "2-digit",
                    month: "short",
                  })}
                </div>
              )}
            </div>

            {/* Animated Dot */}
            <motion.div
              className="h-2 w-2 rounded-full"
              animate={{
                scale: [1, 1.6, 1],
                backgroundColor: ["#34D399", "#3B82F6", "#FBBF24", "#34D399"],
              }}
              transition={{ duration: 1.5, repeat: Infinity }}
            />
          </div>
        </div>
      </motion.div>

      {/* EDIT MODAL */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="w-[95%] sm:max-w-[650px] p-0 border-none bg-transparent shadow-none overflow-visible">
          <DialogHeader className="sr-only">
            <DialogTitle>Update Task</DialogTitle>
            <DialogDescription>Edit the details of your task</DialogDescription>
          </DialogHeader>

          {/* Premium blurred gradient background */}
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-400/20 via-pink-300/20 to-rose-400/20 blur-[120px] animate-pulse -z-10" />

          {isModalOpen && task && (
            <TaskEditForm
              task={task}
              onClose={() => setIsModalOpen(false)}
              onTaskUpdated={async (updatedData) => {
                await onTaskUpdated(updatedData);
                setIsModalOpen(false);
              }}
            />
          )}
        </DialogContent>
      </Dialog>
    </>
  );
}
