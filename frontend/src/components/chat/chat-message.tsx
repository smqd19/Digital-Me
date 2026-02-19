"use client";

import { motion } from "framer-motion";
import { User } from "lucide-react";
import { cn } from "@/lib/utils";
import Image from "next/image";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  isLoading?: boolean;
}

function cleanContent(text: string): string {
  return text
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/__([^_]+)__/g, '$1')
    .replace(/_([^_]+)_/g, '$1')
    .replace(/###\s*/g, '')
    .replace(/##\s*/g, '')
    .replace(/#\s*/g, '')
    .replace(/^\s*[-•]\s*/gm, '• ')
    .replace(/^\s*\d+\.\s*/gm, (match) => match.trim() + ' ')
    .trim();
}

function AssistantAvatar() {
  return (
    <div className="relative w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 via-violet-500 to-cyan-500 p-[1.5px] shadow-md shadow-blue-500/20 overflow-hidden">
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
  );
}

export function ChatMessage({ role, content, isLoading }: ChatMessageProps) {
  const isUser = role === "user";
  const displayContent = isUser ? content : cleanContent(content);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={cn(
        "flex gap-3 max-w-4xl",
        isUser ? "ml-auto flex-row-reverse" : "mr-auto"
      )}
    >
      {/* Avatar */}
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.1, type: "spring", stiffness: 200 }}
        className="flex-shrink-0"
      >
        {isUser ? (
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-violet-500 flex items-center justify-center shadow-md shadow-blue-500/20">
            <User className="w-5 h-5 text-white" />
          </div>
        ) : (
          <AssistantAvatar />
        )}
      </motion.div>

      {/* Message Bubble */}
      <motion.div
        initial={{ opacity: 0, x: isUser ? 20 : -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.15, duration: 0.3 }}
        className={cn(
          "relative px-5 py-3 rounded-2xl max-w-[80%]",
          isUser
            ? "message-user rounded-tr-sm"
            : "message-assistant rounded-tl-sm"
        )}
      >
        {isLoading ? (
          <div className="flex items-center gap-1.5 py-1">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-2 h-2 rounded-full bg-blue-400"
                animate={{
                  scale: [1, 1.3, 1],
                  opacity: [0.5, 1, 0.5],
                }}
                transition={{
                  duration: 0.8,
                  repeat: Infinity,
                  delay: i * 0.15,
                }}
              />
            ))}
          </div>
        ) : isUser ? (
          <p className="text-sm md:text-base leading-relaxed text-white">
            {content}
          </p>
        ) : (
          <div className="text-sm md:text-base leading-relaxed text-slate-200 space-y-2">
            {displayContent.split('\n').map((line, index) => (
              <p key={index} className={line.startsWith('•') ? 'pl-2' : ''}>
                {line || '\u00A0'}
              </p>
            ))}
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}
