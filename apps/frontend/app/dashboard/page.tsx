"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import { Task } from "@/types/task";
import { useTaskState } from "@/lib/task-state";
import TaskList from "@/components/tasks/task-list";
import TaskCreateForm from "@/components/tasks/task-create-form";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription,
} from "@/components/ui/dialog";
import {
  ClipboardList,
  CheckCircle,
  Clock,
  TrendingUp,
  PlusCircle,
  Activity,
  Zap,
  Filter,
  Calendar,
} from "lucide-react";

export default function DashboardPage() {
  const {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
  } = useTaskState();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const total = tasks.length;
  const completed = tasks.filter((t) => t.is_completed).length;
  const highPriority = tasks.filter(
    (t) => t.priority === "high" && !t.is_completed,
  ).length;
  const rate = total ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="space-y-6 lg:space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Header Section - Mobile Optimized */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 bg-white dark:bg-slate-900 p-5 lg:p-6 rounded-[2rem] shadow-sm border border-slate-100 dark:border-slate-800">
        <div>
          <h2 className="text-2xl lg:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">
            Workspace Overview
          </h2>
          <p className="text-slate-500 dark:text-slate-400 mt-1 flex items-center gap-2 text-sm lg:text-base">
            <Calendar className="h-4 w-4 text-indigo-500" />
            Everything looks good today.
          </p>
        </div>

        <Dialog open={isCreateModalOpen} onOpenChange={setIsCreateModalOpen}>
          <DialogTrigger asChild>
            <button className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3.5 rounded-2xl font-bold transition-all shadow-xl shadow-indigo-200 dark:shadow-none active:scale-95">
              <PlusCircle className="h-5 w-5" />
              New Task
            </button>
          </DialogTrigger>

          <DialogContent className="w-[95%] sm:max-w-[650px] p-0 border-none bg-transparent shadow-none gap-0 overflow-visible">
            <DialogHeader className="sr-only">
              <DialogTitle>Create New Task</DialogTitle>
              <DialogDescription>Fill in the details</DialogDescription>
            </DialogHeader>

            <div className="absolute inset-0 bg-indigo-500/5 blur-[100px] -z-10" />

            {/* ✅ FIX: Sirf tab render karein jab modal open ho aur (Edit ke case mein) task load ho chuka ho */}
            {isCreateModalOpen && (
              <TaskCreateForm
                onTaskCreated={async (data) => {
                  await createTask(data);
                  setIsCreateModalOpen(false);
                }}
              />
            )}
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats Cards Grid - 1 col on mobile, 2 on tablet, 4 on desktop */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
        <StatCard
          title="Total Tasks"
          value={total}
          icon={ClipboardList}
          color="text-blue-600"
          bg="bg-blue-50 dark:bg-blue-900/20"
        />
        <StatCard
          title="Completed"
          value={completed}
          icon={CheckCircle}
          color="text-emerald-600"
          bg="bg-emerald-50 dark:bg-emerald-900/20"
        />
        <StatCard
          title="Urgent"
          value={highPriority}
          icon={Clock}
          color="text-rose-600"
          bg="bg-rose-50 dark:bg-rose-900/20"
        />
        <StatCard
          title="Success Rate"
          value={`${rate}%`}
          icon={TrendingUp}
          color="text-amber-600"
          bg="bg-amber-50 dark:bg-amber-900/20"
        />
      </div>

      {/* Main Content Layout - Stack on mobile, side-by-side on XL */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 lg:gap-8">
        {/* Task List Section */}
        <div className="xl:col-span-2 space-y-6">
          <Card className="border-none shadow-sm bg-white dark:bg-slate-900 rounded-3xl overflow-hidden">
            <CardHeader className="flex flex-row items-center justify-between border-b border-slate-50 dark:border-slate-800 p-5 lg:p-8">
              <div className="flex items-center gap-3">
                <div className="p-2.5 bg-indigo-50 dark:bg-indigo-900/20 rounded-xl">
                  <Activity className="h-5 w-5 text-indigo-600" />
                </div>
                <div>
                  <CardTitle className="text-xl font-bold">
                    Recent Tasks
                  </CardTitle>
                  <CardDescription className="text-xs lg:text-sm">
                    Your latest activities
                  </CardDescription>
                </div>
              </div>
              <button className="p-2.5 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-colors">
                <Filter className="h-5 w-5 text-slate-400" />
              </button>
            </CardHeader>
            <CardContent className="p-4 lg:p-8 pt-4">
              <TaskList
                tasks={tasks}
                onTaskUpdated={updateTask}
                onTaskDeleted={deleteTask}
              />
            </CardContent>
          </Card>
        </div>

        {/* Sidebar Widgets */}
        <div className="space-y-6 lg:space-y-8">
          <Card className="border-none shadow-sm rounded-3xl bg-white dark:bg-slate-900 overflow-hidden">
            <CardHeader className="p-6 lg:p-8 pb-4">
              <CardTitle className="text-lg font-bold">
                Priority Breakdown
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6 lg:p-8 pt-0 space-y-5">
              <PriorityBar
                label="High"
                count={highPriority}
                total={total}
                color="bg-rose-500"
              />
              <PriorityBar
                label="Medium"
                count={tasks.filter((t) => t.priority === "medium").length}
                total={total}
                color="bg-amber-500"
              />
              <PriorityBar
                label="Low"
                count={tasks.filter((t) => t.priority === "low").length}
                total={total}
                color="bg-emerald-500"
              />
            </CardContent>
          </Card>

          {/* Upgrade Banner - Mobile UI Adjustment */}
          <Card className="bg-slate-900 text-white border-none shadow-2xl rounded-[2.5rem] relative overflow-hidden group">
            <CardContent className="p-6 lg:p-8 space-y-6 relative z-10">
              <div className="h-12 w-12 bg-white/10 backdrop-blur-md rounded-2xl flex items-center justify-center">
                <Zap className="h-6 w-6 text-indigo-400 fill-indigo-400" />
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-bold">Team Collaboration</h3>
                <p className="text-slate-400 text-sm leading-relaxed">
                  Invite your team to collaborate on projects and sync in
                  real-time.
                </p>
              </div>
              <button className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-4 rounded-2xl font-bold transition-all shadow-lg shadow-indigo-900/50 active:scale-95">
                Unlock Pro Features
              </button>
            </CardContent>
            {/* Design detail for flair */}
            <div className="absolute -right-4 -bottom-4 h-24 w-24 bg-indigo-600/20 rounded-full blur-3xl" />
          </Card>
        </div>
      </div>
    </div>
  );
}

// Updated StatCard: Mobile Friendly
function StatCard({ title, value, icon: Icon, color, bg }: any) {
  return (
    <Card className="border-none shadow-sm bg-white dark:bg-slate-900 rounded-[1.8rem] hover:shadow-xl transition-all duration-300 overflow-hidden">
      <CardContent className="p-5 lg:p-6">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <p className="text-[10px] lg:text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest">
              {title}
            </p>
            <p className="text-3xl lg:text-4xl font-black text-slate-900 dark:text-white tracking-tight">
              {value}
            </p>
          </div>
          <div className={cn("p-3.5 lg:p-4 rounded-2xl", bg)}>
            <Icon className={cn("h-6 w-6 lg:h-7 lg:w-7", color)} />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function PriorityBar({ label, count, total, color }: any) {
  const percentage = total > 0 ? (count / total) * 100 : 0;
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-[10px] font-black uppercase tracking-widest text-slate-400">
        <span>{label}</span>
        <span className="text-slate-900 dark:text-slate-100">
          {count} Tasks
        </span>
      </div>
      <div className="w-full bg-slate-100 dark:bg-slate-800 h-2.5 rounded-full overflow-hidden">
        <div
          className={cn(
            "h-full rounded-full transition-all duration-1000 ease-out",
            color,
          )}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
