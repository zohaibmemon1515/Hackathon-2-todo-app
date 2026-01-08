"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import Navigation from "@/components/layout/navigation";
import { 
  Zap, 
  ShieldCheck, 
  BarChart3, 
  Users2, 
  ArrowRight, 
  CheckCircle2,
  Sparkles
} from "lucide-react";

export default function LandingPage() {
  const [isHovered, setIsHovered] = useState<number | null>(null);

  const features = [
    {
      title: "Smart Management",
      description: "Organize tasks with AI-driven categorization and dynamic priority settings.",
      icon: <Zap className="text-indigo-600" size={28} />,
      gradient: "from-indigo-500/10 to-blue-500/10"
    },
    {
      title: "Team Sync",
      description: "Collaborate in real-time with your team with zero latency synchronization.",
      icon: <Users2 className="text-emerald-600" size={28} />,
      gradient: "from-emerald-500/10 to-teal-500/10"
    },
    {
      title: "Visual Insights",
      description: "Deep-dive into your productivity with interactive performance metrics.",
      icon: <BarChart3 className="text-amber-600" size={28} />,
      gradient: "from-amber-500/10 to-orange-500/10"
    },
    {
      title: "Bank-Grade Security",
      description: "Your data is protected by AES-256 encryption and multi-layer safety.",
      icon: <ShieldCheck className="text-rose-600" size={28} />,
      gradient: "from-rose-500/10 to-pink-500/10"
    },
  ];

  return (
    <div className="min-h-screen bg-[#FDFDFD] overflow-hidden selection:bg-indigo-100 selection:text-indigo-900">
      {/* Background Decorative Elements */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-150 bg-[radial-gradient(circle_at_center,var(--tw-gradient-stops))] from-indigo-50/50 via-transparent to-transparent -z-10" />
      
      <Navigation />

      {/* --- HERO SECTION --- */}
      <section className="relative pt-20 pb-32 px-4 max-w-7xl mx-auto">
        <div className="text-center space-y-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-slate-200 shadow-sm transition-all hover:border-indigo-200"
          >
            <Sparkles size={14} className="text-indigo-600 animate-pulse" />
            <span className="text-xs font-black uppercase tracking-[0.15em] text-slate-600">The Future of Work is Here</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="text-6xl md:text-8xl font-black text-slate-900 tracking-tighter italic leading-[0.9]"
          >
            Simplify Your <br />
            <span className="text-transparent bg-clip-text bg-linear-to-r from-indigo-600 via-violet-600 to-purple-600">
              Productivity
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-lg md:text-xl text-slate-500 max-w-2xl mx-auto font-medium leading-relaxed"
          >
            The all-in-one task management solution built for modern teams who want to achieve 10x more with zero stress.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4"
          >
            <Link href="/auth/register">
              <Button size="lg" className="h-16 px-10 bg-slate-900 hover:bg-black text-white rounded-2xl text-lg font-bold shadow-2xl shadow-slate-200 transition-all active:scale-95 group">
                Get Started Free
                <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="h-16 px-10 border-slate-200 rounded-2xl text-lg font-bold hover:bg-slate-50 transition-all">
              Watch Demo
            </Button>
          </motion.div>
        </div>
      </section>

      {/* --- FEATURES GRID --- */}
      <section id="features" className="py-24 bg-slate-50/50 border-y border-slate-100 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20 space-y-4">
            <h2 className="text-[10px] font-black uppercase tracking-[0.3em] text-indigo-600">Core Capabilities</h2>
            <h3 className="text-4xl md:text-5xl font-black text-slate-900 tracking-tight italic">Engineered for Excellence</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                onMouseEnter={() => setIsHovered(index)}
                onMouseLeave={() => setIsHovered(null)}
                className="group relative bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-sm hover:shadow-2xl hover:shadow-indigo-100 transition-all duration-500 hover:-translate-y-2 cursor-default"
              >
                <div className={`w-16 h-16 rounded-2xl bg-lanier-to-br ${feature.gradient} flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform`}>
                  {feature.icon}
                </div>
                <h4 className="text-xl font-black text-slate-900 mb-3 tracking-tight italic">{feature.title}</h4>
                <p className="text-sm text-slate-500 font-medium leading-relaxed">
                  {feature.description}
                </p>
                <div className="mt-6 flex items-center text-xs font-black text-indigo-600 uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity">
                  Learn More <ArrowRight size={14} className="ml-1" />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* --- CTA SECTION --- */}
      <section className="py-32 px-4 relative overflow-hidden">
        <div className="max-w-5xl mx-auto bg-slate-900 rounded-[3rem] p-12 md:p-20 relative overflow-hidden text-center shadow-[0_40px_80px_-15px_rgba(0,0,0,0.3)]">
          {/* Decorative shapes for CTA */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-600/20 rounded-full blur-3xl -mr-32 -mt-32" />
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-purple-600/10 rounded-full blur-3xl -ml-32 -mb-32" />

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative z-10 space-y-8"
          >
            <h2 className="text-4xl md:text-6xl font-black text-white tracking-tighter italic">
              Ready to reclaim <br /> your focus?
            </h2>
            <p className="text-slate-400 text-lg max-w-xl mx-auto font-medium">
              Join 50,000+ high-performers who have already switched to TaskMaster. No credit card required.
            </p>
            <div className="flex flex-col items-center gap-6 pt-4">
              <Link href="/auth/register">
                <Button size="lg" className="h-16 px-12 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl text-xl font-bold transition-all shadow-xl shadow-indigo-500/20 active:scale-95">
                  Get Started Now
                </Button>
              </Link>
              <div className="flex items-center gap-6">
                {['No CC required', 'Free forever tier', '24/7 Support'].map((item) => (
                  <div key={item} className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">
                    <CheckCircle2 size={12} className="text-indigo-500" />
                    {item}
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* --- FOOTER --- */}
      <footer className="py-12 border-t border-slate-100">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <Zap size={20} className="text-indigo-600 fill-current" />
            <span className="text-sm font-black tracking-tighter italic">TASKMASTER</span>
          </div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">
            © 2026 TASKMASTER INC. DESIGNED FOR PERFORMANCE.
          </p>
          <div className="flex gap-8">
            {['Privacy', 'Terms', 'Contact'].map(item => (
              <Link key={item} href="#" className="text-xs font-black uppercase tracking-widest text-slate-400 hover:text-indigo-600 transition-colors">
                {item}
              </Link>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
}