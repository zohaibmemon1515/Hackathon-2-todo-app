import { useState } from 'react';
import { TaskCreate } from '@/types/task';
import { api } from '@/lib/api';
import { Plus, Calendar, Flag, AlignLeft, Sparkles } from 'lucide-react';

export default function TaskCreateForm({ onTaskCreated }: { onTaskCreated: (task: any) => void }) {
  const [formData, setFormData] = useState<TaskCreate>({ title: '', description: '', priority: 'medium', due_date: undefined });
  const [loading, setLoading] = useState(false);

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: name === 'due_date' && value ? new Date(value).toISOString() : value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const newTask = await api.tasks.create(formData);
      onTaskCreated(newTask);
      setFormData({ title: '', description: '', priority: 'medium', due_date: undefined });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <form onSubmit={handleSubmit} className="bg-slate-50/50 p-1 rounded-4xl border border-slate-200 shadow-inner">
        <div className="bg-white p-6 sm:p-8 rounded-[1.8rem] shadow-xl space-y-6">
          
          {/* Header */}
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <h2 className="text-xl font-black text-slate-800 flex items-center gap-2 tracking-tight">
              <Sparkles className="w-5 h-5 text-indigo-500 fill-indigo-100" /> New Task
            </h2>
            <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 bg-slate-50 px-2 py-1 rounded">Quick Add</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Title - Full Width */}
            <div className="md:col-span-2">
              <div className="group relative">
                <input 
                  name="title" 
                  required 
                  value={formData.title} 
                  onChange={handleChange}
                  className="w-full text-lg font-medium px-0 py-2 border-b-2 border-slate-100 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-300" 
                  placeholder="What's on your mind?" 
                />
              </div>
            </div>

            {/* Description */}
            <div className="md:col-span-2 flex gap-3 items-start">
              <AlignLeft className="w-5 h-5 text-slate-400 mt-2 shrink-0" />
              <textarea 
                name="description" 
                rows={1} 
                value={formData.description || ''} 
                onChange={handleChange}
                className="w-full px-0 py-2 border-b border-slate-100 focus:border-indigo-400 outline-none transition-all resize-none text-slate-600 placeholder:text-slate-300" 
                placeholder="Add notes..." 
              />
            </div>

            {/* Priority Select */}
            <div className="flex items-center gap-3 bg-slate-50 p-3 rounded-2xl border border-slate-100 focus-within:ring-2 ring-indigo-100 transition-all">
              <Flag className={`w-4 h-4 ${formData.priority === 'high' ? 'text-red-500' : 'text-slate-400'}`} />
              <select 
                name="priority" 
                value={formData.priority} 
                onChange={handleChange}
                className="bg-transparent w-full outline-none text-sm font-semibold text-slate-700 cursor-pointer"
              >
                <option value="low">Low Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="high">High Priority</option>
              </select>
            </div>

            {/* Date Input */}
            <div className="flex items-center gap-3 bg-slate-50 p-3 rounded-2xl border border-slate-100 focus-within:ring-2 ring-indigo-100 transition-all">
              <Calendar className="w-4 h-4 text-slate-400" />
              <input 
                type="date" 
                name="due_date" 
                value={formData.due_date ? new Date(formData.due_date).toISOString().split('T')[0] : ''} 
                onChange={handleChange}
                className="bg-transparent w-full outline-none text-sm font-semibold text-slate-700 cursor-pointer" 
              />
            </div>
          </div>

          {/* Submit Button */}
          <button 
            disabled={loading} 
            className="w-full bg-slate-900 hover:bg-indigo-600 text-white font-bold py-4 rounded-2xl transition-all duration-300 flex items-center justify-center gap-2 shadow-lg shadow-slate-200 active:scale-95 disabled:opacity-50"
          >
            {loading ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" /> : <><Plus size={20} /> Create Task</>}
          </button>
        </div>
      </form>
    </div>
  );
}