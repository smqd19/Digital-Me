"use client";

import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import { ArrowRight, Brain, Zap, Mic } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Particles } from "@/components/ui/particles";
import Link from "next/link";
import { useEffect, useState } from "react";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" as const },
  },
};

const floatVariants = {
  initial: { y: 0 },
  animate: {
    y: [-5, 5, -5],
    transition: {
      duration: 4,
      repeat: Infinity,
      ease: "easeInOut" as const,
    },
  },
};

const skills = [
  { icon: Brain, label: "GenAI & LLMs", color: "from-blue-500 to-indigo-600" },
  { icon: Mic, label: "Voice AI", color: "from-violet-500 to-purple-600" },
  { icon: Zap, label: "RAG Systems", color: "from-cyan-500 to-blue-600" },
];

interface AnimatedCounterProps {
  value: number;
  suffix?: string;
  duration?: number;
}

function AnimatedCounter({ value, suffix = "", duration = 2 }: AnimatedCounterProps) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => Math.round(latest));
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    const controls = animate(count, value, { duration });
    const unsubscribe = rounded.on("change", (v) => setDisplayValue(v));
    return () => {
      controls.stop();
      unsubscribe();
    };
  }, [count, rounded, value, duration]);

  return (
    <span>
      {displayValue}{suffix}
    </span>
  );
}

interface RadialProgressProps {
  value: number;
  max: number;
  label: string;
  suffix?: string;
  color: string;
  delay?: number;
}

function RadialProgress({ value, max, label, suffix = "", color, delay = 0 }: RadialProgressProps) {
  const [isVisible, setIsVisible] = useState(false);
  const percentage = (value / max) * 100;
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);

  return (
    <motion.div
      className="relative group"
      whileHover={{ scale: 1.05, y: -8 }}
      transition={{ type: "spring", stiffness: 300 }}
    >
      <div className="relative w-32 h-32 mx-auto">
        {/* Glow effect */}
        <div className={`absolute inset-0 rounded-full blur-xl opacity-30 group-hover:opacity-50 transition-opacity ${color === 'blue' ? 'bg-blue-500' : color === 'violet' ? 'bg-violet-500' : color === 'cyan' ? 'bg-cyan-500' : 'bg-indigo-500'}`} />
        
        {/* Background ring */}
        <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="rgba(255,255,255,0.05)"
            strokeWidth="6"
          />
          {/* Progress ring */}
          <motion.circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke={`url(#gradient-${color})`}
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: isVisible ? strokeDashoffset : circumference }}
            transition={{ duration: 1.5, ease: "easeOut", delay: 0.3 }}
          />
          <defs>
            <linearGradient id={`gradient-${color}`} x1="0%" y1="0%" x2="100%" y2="100%">
              {color === 'blue' && (
                <>
                  <stop offset="0%" stopColor="#3b82f6" />
                  <stop offset="100%" stopColor="#6366f1" />
                </>
              )}
              {color === 'violet' && (
                <>
                  <stop offset="0%" stopColor="#8b5cf6" />
                  <stop offset="100%" stopColor="#a855f7" />
                </>
              )}
              {color === 'cyan' && (
                <>
                  <stop offset="0%" stopColor="#06b6d4" />
                  <stop offset="100%" stopColor="#3b82f6" />
                </>
              )}
              {color === 'indigo' && (
                <>
                  <stop offset="0%" stopColor="#6366f1" />
                  <stop offset="100%" stopColor="#8b5cf6" />
                </>
              )}
            </linearGradient>
          </defs>
        </svg>

        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-bold text-white">
            {isVisible ? <AnimatedCounter value={value} suffix={suffix} /> : `0${suffix}`}
          </span>
        </div>
      </div>
      <p className="mt-3 text-sm text-slate-400 text-center font-medium">{label}</p>
    </motion.div>
  );
}

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden gradient-bg">
      {/* Particles Background - Blue */}
      <Particles className="absolute inset-0 z-0" quantity={60} color="59, 130, 246" />

      {/* Enhanced Gradient Orbs - Neon Blue */}
      <motion.div
        className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-gradient-to-br from-blue-600/20 via-violet-500/15 to-transparent rounded-full blur-3xl"
        animate={{
          scale: [1, 1.3, 1],
          opacity: [0.3, 0.5, 0.3],
          rotate: [0, 180, 360],
        }}
        transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
      />
      <motion.div
        className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-gradient-to-tl from-violet-500/20 via-cyan-500/15 to-transparent rounded-full blur-3xl"
        animate={{
          scale: [1.2, 1, 1.2],
          opacity: [0.3, 0.5, 0.3],
          rotate: [360, 180, 0],
        }}
        transition={{ duration: 12, repeat: Infinity, ease: "linear" }}
      />
      <motion.div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-radial from-blue-500/10 via-transparent to-transparent rounded-full"
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.2, 0.4, 0.2],
        }}
        transition={{ duration: 8, repeat: Infinity }}
      />

      {/* Content */}
      <motion.div
        className="relative z-10 max-w-5xl mx-auto px-6 text-center"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Main Heading */}
        <motion.h1
          variants={itemVariants}
          className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
        >
          <span className="text-white drop-shadow-lg">Hi, I&apos;m </span>
          <span className="gradient-text drop-shadow-2xl">Qasim Sheikh</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          variants={itemVariants}
          className="text-xl md:text-2xl text-slate-400 mb-4 font-light"
        >
          Senior AI Engineer & Data Scientist
        </motion.p>

        <motion.p
          variants={itemVariants}
          className="text-lg text-slate-500 mb-8 max-w-2xl mx-auto"
        >
          7+ years crafting intelligent systems. Specializing in{" "}
          <span className="text-blue-400 font-medium">Generative AI</span>,{" "}
          <span className="text-violet-400 font-medium">LLMs</span>, and{" "}
          <span className="text-cyan-400 font-medium">Voice AI</span>.
        </motion.p>

        {/* Skills Pills */}
        <motion.div
          variants={itemVariants}
          className="flex flex-wrap justify-center gap-3 mb-10"
        >
          {skills.map((skill, index) => (
            <motion.div
              key={skill.label}
              variants={floatVariants}
              initial="initial"
              animate="animate"
              style={{ animationDelay: `${index * 0.5}s` }}
              className="flex items-center gap-2 px-4 py-2 rounded-full glass-light shadow-lg shadow-black/20 border border-white/10"
            >
              <div className={`p-1.5 rounded-lg bg-gradient-to-br ${skill.color} shadow-md`}>
                <skill.icon className="w-4 h-4 text-white" />
              </div>
              <span className="text-sm text-slate-300">{skill.label}</span>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA Button - Centered */}
        <motion.div
          variants={itemVariants}
          className="flex justify-center"
        >
          <Link href="/chat">
            <Button size="lg" className="group pulse-glow shadow-2xl shadow-blue-500/30">
              Talk to the Digital Me
              <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
            </Button>
          </Link>
        </motion.div>

        {/* Interactive Stats with Radial Progress */}
        <motion.div
          variants={itemVariants}
          className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8"
        >
          <RadialProgress
            value={7}
            max={10}
            label="Years Experience"
            suffix="+"
            color="blue"
            delay={200}
          />
          <RadialProgress
            value={15}
            max={20}
            label="AI Projects"
            suffix="+"
            color="violet"
            delay={400}
          />
          <RadialProgress
            value={85}
            max={100}
            label="Automation Accuracy"
            suffix="%"
            color="cyan"
            delay={600}
          />
          <RadialProgress
            value={10}
            max={15}
            label="Team Members Led"
            suffix="+"
            color="indigo"
            delay={800}
          />
        </motion.div>
      </motion.div>

      {/* Scroll Indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.5, duration: 0.5 }}
      >
        <motion.div
          className="w-6 h-10 rounded-full border-2 border-slate-600/50 flex justify-center pt-2 shadow-inner"
          animate={{ y: [0, 5, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          <motion.div className="w-1.5 h-1.5 rounded-full bg-gradient-to-b from-blue-400 to-violet-500" />
        </motion.div>
      </motion.div>
    </section>
  );
}
