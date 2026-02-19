"use client";

import { motion } from "framer-motion";
import { ArrowLeft, Sparkles } from "lucide-react";
import Link from "next/link";
import Image from "next/image";

function AvatarIcon() {
  return (
    <motion.div
      className="relative"
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: "spring", stiffness: 200, delay: 0.1 }}
    >
      {/* Glow effect */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-blue-500/50 to-violet-500/50 blur-md" />
      
      {/* Main container */}
      <div className="relative w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 via-violet-500 to-cyan-500 p-[1.5px] shadow-lg shadow-blue-500/30 overflow-hidden">
        <div className="w-full h-full rounded-xl overflow-hidden">
          <Image
            src="/qasim-avatar.png"
            alt="Qasim Sheikh"
            width={40}
            height={40}
            className="w-full h-full object-cover object-[center_15%] scale-[1.2]"
          />
        </div>
      </div>
      
      {/* Online indicator */}
      <motion.div
        className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full border-2 border-[#06080d] shadow-sm shadow-green-500/50"
        animate={{ scale: [1, 1.2, 1] }}
        transition={{ duration: 2, repeat: Infinity }}
      />
    </motion.div>
  );
}

export function ChatHeader() {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="sticky top-0 z-50 glass border-b border-white/5 shadow-lg shadow-black/20"
    >
      <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/">
            <motion.button
              whileHover={{ scale: 1.05, x: -2 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 rounded-xl hover:bg-white/5 transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-slate-400" />
            </motion.button>
          </Link>

          <div className="flex items-center gap-3">
            <AvatarIcon />

            <div>
              <h1 className="font-semibold text-white flex items-center gap-2">
                Qasim&apos;s Digital Me
                <Sparkles className="w-4 h-4 text-blue-400" />
              </h1>
              <p className="text-xs text-slate-500">Always here to help</p>
            </div>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-blue-500/10 to-violet-500/10 border border-blue-500/20 shadow-inner"
        >
          <div className="w-2 h-2 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 animate-pulse shadow-sm shadow-green-500/50" />
          <span className="text-xs text-blue-400 font-medium">Online</span>
        </motion.div>
      </div>
    </motion.header>
  );
}
