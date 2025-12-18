"use client";

import { motion } from "framer-motion";
import { ArrowRight, TrendingUp, DollarSign } from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface DealCardProps {
    title: string;
    description: string;
    price: string;
    revenue: string;
    type: "github_zombie" | "chrome_ghost";
    onAnalyze: () => void;
}

export function DealCard({ title, description, price, revenue, type, onAnalyze }: DealCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ y: -2 }}
            className={cn(
                "group relative overflow-hidden rounded-xl",
                "bg-white/5 backdrop-blur-xl border border-white/10",
                "shadow-2xl shadow-black/50",
                "transition-all duration-300",
                "hover:border-white/20 hover:shadow-indigo-500/10"
            )}
        >
            <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                    <Badge
                        variant="outline"
                        className={cn(
                            "border-transparent bg-white/5 text-xs font-mono tracking-wider uppercase",
                            type === "github_zombie" ? "text-orange-400" : "text-emerald-400"
                        )}
                    >
                        {type === "github_zombie" ? "Zombie Code" : "Ghost API"}
                    </Badge>
                    <div className="flex items-center text-zinc-400 text-xs font-medium">
                        <span className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse" />
                        Active Opportunity
                    </div>
                </div>

                <h3 className="text-xl font-medium text-white mb-2 tracking-tight group-hover:text-indigo-400 transition-colors">
                    {title}
                </h3>

                <p className="text-zinc-400 text-sm mb-6 line-clamp-2 h-10">
                    {description}
                </p>

                <div className="flex items-center justify-between mt-auto pt-4 border-t border-white/5">
                    <div className="flex flex-col">
                        <span className="text-zinc-500 text-xs uppercase tracking-wider mb-1">Est. Value</span>
                        <span className="text-white font-mono text-lg">{price}</span>
                    </div>

                    <div className="flex flex-col items-end">
                        <div className="bg-green-500/10 text-green-400 px-2 py-1 rounded-full text-xs font-mono mb-1 flex items-center">
                            <TrendingUp className="w-3 h-3 mr-1" />
                            {revenue}
                        </div>
                    </div>
                </div>

                <div className="mt-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 absolute bottom-6 right-6">
                    <Button
                        onClick={onAnalyze}
                        size="sm"
                        className="bg-indigo-500 hover:bg-indigo-600 text-white border-0"
                    >
                        Analyze <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                </div>
            </div>
        </motion.div>
    );
}
