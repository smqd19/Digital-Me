"use client";

import { useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Trash2 } from "lucide-react";
import { ChatHeader } from "@/components/chat/chat-header";
import { ChatMessage } from "@/components/chat/chat-message";
import { ChatInput } from "@/components/chat/chat-input";
import { SuggestedQuestions } from "@/components/chat/suggested-questions";
import { Particles } from "@/components/ui/particles";
import { useChat } from "@/hooks/use-chat";
import Image from "next/image";

function WelcomeAvatar() {
  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: "spring", stiffness: 200 }}
      className="relative mb-6"
    >
      {/* Outer glow */}
      <motion.div
        className="absolute inset-0 rounded-3xl bg-gradient-to-br from-blue-500/40 to-violet-500/40 blur-2xl"
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.4, 0.6, 0.4],
        }}
        transition={{ duration: 3, repeat: Infinity }}
      />
      
      {/* Main avatar */}
      <div className="relative w-24 h-24 rounded-3xl bg-gradient-to-br from-blue-500 via-violet-500 to-cyan-500 p-[3px] shadow-2xl shadow-blue-500/30 overflow-hidden">
        <div className="w-full h-full rounded-3xl overflow-hidden">
          <Image
            src="/qasim-avatar.png"
            alt="Qasim Sheikh"
            width={96}
            height={96}
            className="w-full h-full object-cover object-[center_15%] scale-[1.2]"
          />
        </div>
      </div>
      
      {/* Animated ring */}
      <motion.div
        className="absolute -inset-2 rounded-3xl border-2 border-blue-500/30"
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.3, 0.1, 0.3],
        }}
        transition={{ duration: 2, repeat: Infinity }}
      />
    </motion.div>
  );
}

export default function ChatPage() {
  const { messages, isLoading, sendMessage, clearMessages } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = (message: string) => {
    sendMessage(message);
  };

  return (
    <div className="h-screen flex flex-col gradient-bg overflow-hidden">
      {/* Background Effects */}
      <Particles className="fixed inset-0 z-0" quantity={30} color="59, 130, 246" />
      <div className="fixed inset-0 z-0 pointer-events-none">
        <motion.div 
          className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-gradient-to-br from-blue-600/15 to-transparent rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.2, 0.3, 0.2],
          }}
          transition={{ duration: 8, repeat: Infinity }}
        />
        <motion.div 
          className="absolute bottom-0 right-1/4 w-[400px] h-[400px] bg-gradient-to-tl from-violet-500/15 to-transparent rounded-full blur-3xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.2, 0.3, 0.2],
          }}
          transition={{ duration: 10, repeat: Infinity }}
        />
      </div>

      {/* Header */}
      <ChatHeader />

      {/* Main Chat Area - Fixed Layout */}
      <div className="flex-1 relative z-10 flex flex-col min-h-0">
        <div className="flex-1 max-w-4xl w-full mx-auto px-4 flex flex-col min-h-0">
          
          {/* Messages Container - Scrollable (hidden scrollbar) */}
          <div className="flex-1 overflow-y-auto py-6 space-y-6">
            <AnimatePresence mode="popLayout">
              {messages.length === 0 ? (
                <motion.div
                  key="welcome"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="flex flex-col items-center justify-center py-8"
                >
                  {/* Welcome Avatar */}
                  <WelcomeAvatar />

                  <motion.h2
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="text-2xl font-bold text-white mb-2 text-shadow-md"
                  >
                    Welcome! I&apos;m Qasim&apos;s Digital Me
                  </motion.h2>

                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                    className="text-slate-400 text-center max-w-md mb-8"
                  >
                    I can tell you about Qasim&apos;s experience, projects, skills, and
                    help you understand if he&apos;s the right fit for your team.
                  </motion.p>

                  <SuggestedQuestions onSelect={handleSend} />
                </motion.div>
              ) : (
                <>
                  {messages.map((message) => (
                    <ChatMessage
                      key={message.id}
                      role={message.role}
                      content={message.content}
                    />
                  ))}

                  {isLoading && (
                    <ChatMessage
                      role="assistant"
                      content=""
                      isLoading={true}
                    />
                  )}
                </>
              )}
            </AnimatePresence>
            <div ref={messagesEndRef} />
          </div>

          {/* Clear Chat Button */}
          {messages.length > 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-center py-2"
            >
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={clearMessages}
                className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm text-slate-500 hover:text-slate-300 hover:bg-white/5 transition-colors"
              >
                <Trash2 className="w-4 h-4" />
                Clear conversation
              </motion.button>
            </motion.div>
          )}

          {/* Input Area - Fixed at Bottom */}
          <div className="py-4 flex-shrink-0">
            <ChatInput onSend={handleSend} isLoading={isLoading} />
          </div>
        </div>
      </div>
    </div>
  );
}
