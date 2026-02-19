"use client";

import { motion } from "framer-motion";
import { Sparkles, Briefcase, Code, Award, MessageSquare } from "lucide-react";

interface SuggestedQuestionsProps {
  onSelect: (question: string) => void;
}

const suggestions = [
  {
    icon: Sparkles,
    text: "Tell me about yourself",
    color: "from-blue-500 to-indigo-600",
  },
  {
    icon: Briefcase,
    text: "What's your LLM experience?",
    color: "from-violet-500 to-purple-600",
  },
  {
    icon: Code,
    text: "Show me your Voice AI projects",
    color: "from-cyan-500 to-blue-600",
  },
  {
    icon: Award,
    text: "What are your key achievements?",
    color: "from-indigo-500 to-violet-600",
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20, scale: 0.9 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.4, ease: "easeOut" as const },
  },
};

export function SuggestedQuestions({ onSelect }: SuggestedQuestionsProps) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-3"
    >
      <motion.div
        variants={itemVariants}
        className="flex items-center gap-2 text-sm text-slate-500 mb-4"
      >
        <MessageSquare className="w-4 h-4" />
        <span>Suggested questions</span>
      </motion.div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {suggestions.map((suggestion) => (
          <motion.button
            key={suggestion.text}
            variants={itemVariants}
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onSelect(suggestion.text)}
            className="group flex items-center gap-3 p-4 rounded-xl glass-light border border-white/5 hover:border-blue-500/30 transition-all duration-300 text-left"
          >
            <div
              className={`p-2 rounded-lg bg-gradient-to-br ${suggestion.color} opacity-80 group-hover:opacity-100 transition-opacity shadow-md`}
            >
              <suggestion.icon className="w-4 h-4 text-white" />
            </div>
            <span className="text-sm text-slate-300 group-hover:text-white transition-colors">
              {suggestion.text}
            </span>
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
}
