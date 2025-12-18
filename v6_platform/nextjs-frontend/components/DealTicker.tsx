"use client";

import { motion } from "framer-motion";
import { Zap } from "lucide-react";

export function DealTicker() {
    const items = [
        "Github Zombie found: repo/legacy-core ($12k Est)",
        "Chrome Ghost detected: /api/v1/admin-hidden",
        "New Asset: user-db-snapshot.sql",
        "Scanning network specific nodes...",
        "Gemini 3 Flash: Valuation complete for Asset #492"
    ];

    return (
        <div className="w-full bg-black/40 border-y border-white/5 backdrop-blur-md h-10 flex items-center overflow-hidden relative">
            <div className="absolute left-0 top-0 bottom-0 w-20 bg-gradient-to-r from-zinc-950 to-transparent z-10" />
            <div className="absolute right-0 top-0 bottom-0 w-20 bg-gradient-to-l from-zinc-950 to-transparent z-10" />

            <div className="flex items-center space-x-2 px-4 z-20 bg-zinc-950/80 h-full border-r border-white/10">
                <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span className="text-xs font-mono text-zinc-400 font-bold uppercase tracking-widest">Live Feed</span>
            </div>

            <motion.div
                className="flex space-x-12 px-4 whitespace-nowrap"
                animate={{ x: [0, -1000] }}
                transition={{
                    repeat: Infinity,
                    ease: "linear",
                    duration: 30
                }}
            >
                {[...items, ...items].map((item, i) => (
                    <div key={i} className="flex items-center text-xs font-mono text-zinc-500">
                        <Zap className="w-3 h-3 text-indigo-500/50 mr-2" />
                        {item}
                    </div>
                ))}
            </motion.div>
        </div>
    );
}
