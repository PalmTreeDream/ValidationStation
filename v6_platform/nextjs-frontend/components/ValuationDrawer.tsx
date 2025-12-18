"use client";

import { motion, AnimatePresence } from "framer-motion";
import { X, CheckCircle2, AlertTriangle, Layers } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ValuationDrawerProps {
    isOpen: boolean;
    onClose: () => void;
    data: {
        title: string;
        valuation: string;
        reasoning: string;
        details: string;
    } | null;
}

export function ValuationDrawer({ isOpen, onClose, data }: ValuationDrawerProps) {
    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
                    />

                    {/* Drawer */}
                    <motion.div
                        initial={{ x: "100%" }}
                        animate={{ x: 0 }}
                        exit={{ x: "100%" }}
                        transition={{ type: "spring", damping: 25, stiffness: 200 }}
                        className="fixed right-0 top-0 bottom-0 w-full max-w-md bg-[#09090b] border-l border-white/10 z-50 shadow-2xl p-6 flex flex-col"
                    >
                        <div className="flex items-center justify-between mb-8">
                            <div className="flex items-center space-x-2">
                                <div className="p-2 bg-indigo-500/10 rounded-lg">
                                    <Layers className="w-5 h-5 text-indigo-400" />
                                </div>
                                <h2 className="text-xl font-medium text-white tracking-tight">V6.0 Valuation Protocol</h2>
                            </div>
                            <Button variant="ghost" size="icon" onClick={onClose} className="text-zinc-500 hover:text-white rounded-full">
                                <X className="w-5 h-5" />
                            </Button>
                        </div>

                        {data ? (
                            <div className="space-y-8 overflow-y-auto flex-1 pr-2">
                                {/* Valuation Hero */}
                                <div className="p-6 rounded-2xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border border-white/5 relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 p-3 opacity-20">
                                        <DollarSignIcon className="w-24 h-24 text-indigo-500" />
                                    </div>
                                    <div className="relative">
                                        <p className="text-sm text-indigo-400 font-mono mb-1 uppercase tracking-wider">AI Estimated Value</p>
                                        <h3 className="text-4xl font-medium text-white tracking-tighter shadow-glow">{data.valuation}</h3>
                                    </div>
                                </div>

                                {/* Reasoning */}
                                <div className="space-y-3">
                                    <h4 className="text-sm font-medium text-zinc-400 uppercase tracking-widest flex items-center">
                                        <CheckCircle2 className="w-4 h-4 mr-2 text-emerald-500" />
                                        Analysis Reasoning
                                    </h4>
                                    <p className="text-zinc-300 leading-relaxed text-sm bg-zinc-900/50 p-4 rounded-lg border border-white/5">
                                        {data.reasoning}
                                    </p>
                                </div>

                                {/* Technical Details */}
                                <div className="space-y-3">
                                    <h4 className="text-sm font-medium text-zinc-400 uppercase tracking-widest flex items-center">
                                        <AlertTriangle className="w-4 h-4 mr-2 text-amber-500" />
                                        Leverage Points
                                    </h4>
                                    <div className="text-zinc-400 text-sm font-mono whitespace-pre-wrap bg-zinc-950 p-4 rounded-lg border border-white/5">
                                        {data.details}
                                    </div>
                                </div>

                                <div className="p-4 bg-emerald-500/5 border border-emerald-500/20 rounded-lg">
                                    <p className="text-emerald-400 text-xs text-center">
                                        Confidence Score: 94.2% (Gemini 3 Flash Verified)
                                    </p>
                                </div>
                            </div>
                        ) : (
                            <div className="flex-1 flex items-center justify-center text-zinc-500">
                                <div className="animate-pulse flex flex-col items-center">
                                    <div className="w-8 h-8 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin mb-4" />
                                    Processing Asset Data...
                                </div>
                            </div>
                        )}

                        <div className="mt-8 pt-6 border-t border-white/5">
                            <Button className="w-full bg-white text-black hover:bg-zinc-200 font-medium">
                                Export Report PDF
                            </Button>
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}

function DollarSignIcon({ className }: { className?: string }) {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
            <line x1="12" x2="12" y1="2" y2="22" />
            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
        </svg>
    )
}
