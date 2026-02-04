"use client";

import { useState, useEffect } from "react";
import { Task } from "@/types/task";
import TaskCard from "@/components/tasks/task-card";
import {
  LayoutGrid,
  CheckCircle2,
  Clock3,
  BarChart3,
  Filter,
  Search,
} from "lucide-react";
import { motion } from "framer-motion";

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: (id: string, updates: Partial<Task>) => void;
  onTaskDeleted: (id: string) => void;
}

export default function TaskList({
  tasks,
  onTaskUpdated,
  onTaskDeleted,
}: TaskListProps) {
  const [filter, setFilter] = useState<"all" | "completed" | "pending">("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [sortOption, setSortOption] = useState<
    "created_at" | "due_date" | "priority" | "title"
  >("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);

  // Apply filters
  let filteredTasks = tasks.filter((task) => {
    if (filter === "completed") return task.is_completed;
    if (filter === "pending") return !task.is_completed;
    return true;
  });

  if (searchQuery) {
    const q = searchQuery.toLowerCase();
    filteredTasks = filteredTasks.filter(
      (task) =>
        task.title.toLowerCase().includes(q) ||
        (task.description && task.description.toLowerCase().includes(q)),
    );
  }

  // Sorting
  filteredTasks.sort((a, b) => {
    let aValue: any, bValue: any;
    switch (sortOption) {
      case "title":
        aValue = a.title.toLowerCase();
        bValue = b.title.toLowerCase();
        break;
      case "priority":
        const order = { high: 3, medium: 2, low: 1 };
        aValue = order[a.priority];
        bValue = order[b.priority];
        break;
      case "due_date":
        aValue = a.due_date ? new Date(a.due_date) : new Date(0);
        bValue = b.due_date ? new Date(b.due_date) : new Date(0);
        break;
      case "created_at":
      default:
        aValue = a.created_at ? new Date(a.created_at) : new Date(0);
        bValue = b.created_at ? new Date(b.created_at) : new Date(0);
        break;
    }
    return sortOrder === "asc"
      ? aValue > bValue
        ? 1
        : -1
      : aValue < bValue
        ? 1
        : -1;
  });

  const totalPages = Math.ceil(filteredTasks.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedTasks = filteredTasks.slice(
    startIndex,
    startIndex + itemsPerPage,
  );

  useEffect(
    () => setCurrentPage(1),
    [filter, searchQuery, sortOption, sortOrder],
  );

  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((t) => t.is_completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const completionRate = totalTasks
    ? Math.round((completedTasks / totalTasks) * 100)
    : 0;

  if (!tasks.length) {
    return (
      <div className="bg-white shadow-lg sm:rounded-2xl p-12 text-center border-2 border-dashed border-slate-200">
        <LayoutGrid className="mx-auto h-12 w-12 text-slate-300 animate-pulse" />
        <h3 className="mt-4 text-sm font-bold text-slate-900">
          No tasks created
        </h3>
        <p className="mt-1 text-sm text-slate-500">
          Get started by creating a new task.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* --- STATS --- */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          {
            label: "Total",
            val: totalTasks,
            icon: LayoutGrid,
            color: "text-indigo-600",
            bg: "bg-indigo-50",
          },
          {
            label: "Done",
            val: completedTasks,
            icon: CheckCircle2,
            color: "text-emerald-600",
            bg: "bg-emerald-50",
          },
          {
            label: "Pending",
            val: pendingTasks,
            icon: Clock3,
            color: "text-amber-600",
            bg: "bg-amber-50",
          },
          {
            label: "Rate",
            val: `${completionRate}%`,
            icon: BarChart3,
            color: "text-blue-600",
            bg: "bg-blue-50",
          },
        ].map((stat, i) => (
          <motion.div
            key={i}
            whileHover={{ scale: 1.03 }}
            className="bg-white p-4 rounded-3xl border border-slate-100 shadow-sm flex items-center gap-4 transition-all"
          >
            <div
              className={`shrink-0 ${stat.bg} ${stat.color} p-3 rounded-2xl flex items-center justify-center`}
            >
              <stat.icon size={20} />
            </div>
            <div>
              <p className="text-[10px] font-black uppercase tracking-wider text-slate-400">
                {stat.label}
              </p>
              <p className="text-xl font-black text-slate-900">{stat.val}</p>
            </div>
          </motion.div>
        ))}
      </div>

      {/* --- MAIN FILTERS --- */}
      <div className="bg-white p-4 rounded-3xl border border-slate-100 shadow-sm flex flex-wrap gap-4 items-center justify-between">
        <div className="flex-1 relative min-w-37.5">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-4 w-4 text-slate-400" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search tasks..."
            className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>

        <div className="flex gap-2 flex-wrap">
          {(["all", "pending", "completed"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 text-xs font-bold uppercase rounded-xl transition-all ${
                filter === f
                  ? "bg-indigo-600 text-white shadow-md"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {/* --- TASK CARDS --- */}
      <div className="p-6 bg-white rounded-3xl border border-slate-100 space-y-6">
        <div className="mb-2 px-4 text-sm font-bold text-slate-600">
          {filteredTasks.length} of {tasks.length} tasks shown
        </div>
        {paginatedTasks.length ? (
          <motion.div
            layout
            className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3"
          >
            {paginatedTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onTaskUpdated={(updatedTask:any) =>
                  onTaskUpdated(updatedTask.id, updatedTask)
                }
                onTaskDeleted={onTaskDeleted}
              />
            ))}
          </motion.div>
        ) : (
          <div className="text-center py-12">
            <Filter className="mx-auto h-12 w-12 text-slate-200 animate-pulse" />
            <h3 className="mt-2 text-sm font-semibold text-slate-900">
              No tasks found
            </h3>
            <p className="mt-1 text-sm text-slate-500">
              Try adjusting your filters or create a new task.
            </p>
          </div>
        )}
      </div>

      {/* --- PAGINATION --- */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between px-4 mt-2">
          <button
            onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="text-xs font-bold uppercase tracking-widest text-slate-400 disabled:opacity-30 hover:text-slate-600 transition-all"
          >
            &larr; Prev
          </button>
          <div className="flex gap-2">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
              <button
                key={p}
                onClick={() => setCurrentPage(p)}
                className={`w-8 h-8 rounded-lg text-xs font-bold transition-all ${currentPage === p ? "bg-indigo-600 text-white shadow-md" : "bg-slate-100 text-slate-500 hover:bg-slate-200"}`}
              >
                {p}
              </button>
            ))}
          </div>
          <button
            onClick={() =>
              setCurrentPage((prev) => Math.min(prev + 1, totalPages))
            }
            disabled={currentPage === totalPages}
            className="text-xs font-bold uppercase tracking-widest text-slate-400 disabled:opacity-30 hover:text-slate-600 transition-all"
          >
            Next &rarr;
          </button>
        </div>
      )}
    </div>
  );
}
