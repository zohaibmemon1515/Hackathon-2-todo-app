import { useState } from "react";
import { Task } from "@/types/task";
import {
  Save,
  AlertCircle,
  Type,
  AlignLeft,
  Flag,
  Calendar as CalendarIcon,
} from "lucide-react";

interface TaskEditFormProps {
  task: Task;
  onTaskUpdated: (updatedTask: Task) => void;
  onClose: () => void;
}

export default function TaskEditForm({
  task,
  onTaskUpdated,
  onClose,
}: TaskEditFormProps) {
  const [formData, setFormData] = useState({
    title: task.title,
    description: task.description || "",
    priority: task.priority,
    due_date: task.due_date
      ? new Date(task.due_date).toISOString().split("T")[0]
      : "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // TypeScript error fix karne ke liye formatting
      const updatedTaskData: Task = {
        ...task,
        title: formData.title,
        description: formData.description,
        priority: formData.priority,
        // Agar date khali hai toh 'undefined' bhej rahe hain 'null' ki jagah
        due_date: formData.due_date
          ? new Date(formData.due_date).toISOString()
          : undefined,
      };

      // Save call
      await onTaskUpdated(updatedTaskData);

      // Modal band karna
      onClose();
    } catch (err: any) {
      console.error("Update Error:", err);
      setError(err.message || "Update failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && (
        <div className="flex items-center gap-2 p-3 bg-rose-50 text-rose-600 rounded-xl text-xs font-bold">
          <AlertCircle size={16} /> {error}
        </div>
      )}

      <div className="space-y-1.5">
        <label className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">
          <Type size={12} className="text-indigo-500" /> Title
        </label>
        <input
          name="title"
          value={formData.title}
          onChange={handleChange}
          required
          className="w-full bg-slate-50 border-2 border-transparent focus:border-indigo-500/20 focus:bg-white rounded-xl px-4 py-3 outline-none transition-all font-bold text-slate-800"
        />
      </div>

      <div className="space-y-1.5">
        <label className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">
          <AlignLeft size={12} className="text-indigo-500" /> Description
        </label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={3}
          className="w-full bg-slate-50 border-2 border-transparent focus:border-indigo-500/20 focus:bg-white rounded-xl px-4 py-3 outline-none transition-all text-slate-600 resize-none"
        />
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1.5">
          <label className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">
            <Flag size={12} className="text-indigo-500" /> Priority
          </label>
          <select
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            className="w-full bg-slate-50 border-2 border-transparent focus:border-indigo-500/20 rounded-xl px-3 py-3 outline-none font-bold text-slate-700 appearance-none cursor-pointer"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="space-y-1.5">
          <label className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">
            <CalendarIcon size={12} className="text-indigo-500" /> Due Date
          </label>
          <input
            type="date"
            name="due_date"
            value={formData.due_date}
            onChange={handleChange}
            className="w-full bg-slate-50 border-2 border-transparent focus:border-indigo-500/20 rounded-xl px-3 py-3 outline-none font-bold text-slate-700 cursor-pointer"
          />
        </div>
      </div>

      <div className="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={loading}
          className="flex-1 bg-slate-900 text-white h-12 rounded-xl font-bold uppercase tracking-widest text-[10px] flex items-center justify-center gap-2 hover:bg-indigo-600 transition-all disabled:opacity-50 active:scale-95"
        >
          <Save size={14} /> {loading ? "Saving..." : "Save Changes"}
        </button>
        <button
          type="button"
          onClick={onClose}
          className="px-5 h-12 rounded-xl font-bold uppercase tracking-widest text-[10px] text-slate-400 bg-slate-50 hover:bg-slate-100 transition-all"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
