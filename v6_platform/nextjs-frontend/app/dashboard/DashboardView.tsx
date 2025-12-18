"use client";

import { useState } from "react";
import { DealTicker } from "@/components/DealTicker";
import { DealCard } from "@/components/DealCard";
import { ValuationDrawer } from "@/components/ValuationDrawer";
import { Button } from "@/components/ui/button";
import { Scan, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

export function DashboardView() {
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);
    const [selectedAsset, setSelectedAsset] = useState<any>(null);
    const [assets, setAssets] = useState<any[]>([]);
    const [isScanning, setIsScanning] = useState(false);

    const handleScan = async () => {
        setIsScanning(true);
        // Simulate scan delay
        setTimeout(() => {
            setAssets([
                {
                    id: "1",
                    title: "Legacy Github: core-v1-archive",
                    description: "Found abandoned branch with critical auth logic not present in v2.",
                    price: "$15,000 - $25,000",
                    revenue: "High Potential",
                    type: "github_zombie",
                    details: "Codebase contains trade-secret logic for legacy auth flow. Re-monetization possible via licensing to legacy users."
                },
                {
                    id: "2",
                    title: "Shadow API: /v1/internal/admin",
                    description: "Undocumented admin endpoint accessible via specific header injection.",
                    price: "$50,000+",
                    revenue: "Critical Vulnerability",
                    type: "chrome_ghost",
                    details: "Direct access to admin table detected. Bounty program applicable or immediate patch required."
                },
                {
                    id: "3",
                    title: "Deprecated Service: ImageOptimizer",
                    description: "Service running on AWS instance labeled 'do-not-delete' but unlinked.",
                    price: "$200/mo cost",
                    revenue: "Cost Saver",
                    type: "github_zombie",
                    details: "Zombie infrastructure. Shutting down saves $2400/yr immediately."
                }
            ]);
            setIsScanning(false);
        }, 2000);
    };

    const handleAnalyze = (asset: any) => {
        setSelectedAsset({
            title: asset.title,
            valuation: asset.price,
            reasoning: asset.description, // Mock reasoning mapping
            details: asset.details
        });
        setIsDrawerOpen(true);
    };

    return (
        <div className="min-h-screen bg-transparent text-foreground relative font-sans selection:bg-indigo-500/30">

            {/* Ticker */}
            <DealTicker />

            <main className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <header className="mb-12 flex justify-between items-end">
                    <div>
                        <h1 className="text-4xl font-medium tracking-tighter text-white mb-2">
                            Asset Hunter <span className="text-indigo-500">V6.0</span>
                        </h1>
                        <p className="text-zinc-400">
                            Identify, Analyze, and Valuate Digital Ghosts & Zombies.
                        </p>
                    </div>

                    <Button
                        onClick={handleScan}
                        disabled={isScanning}
                        size="lg"
                        className="bg-white text-black hover:bg-zinc-200 border-0 font-medium tracking-tight rounded-full px-8 shadow-xl shadow-white/10"
                    >
                        {isScanning ? (
                            <Sparkles className="w-5 h-5 mr-2 animate-spin text-indigo-500" />
                        ) : (
                            <Scan className="w-5 h-5 mr-2" />
                        )}
                        {isScanning ? "Scanning Ecosystem..." : "Initiate System Scan"}
                    </Button>
                </header>

                {/* Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {assets.length === 0 && !isScanning && (
                        <div className="col-span-full py-20 text-center border border-dashed border-white/10 rounded-3xl bg-white/5">
                            <p className="text-zinc-500">System Ready. Initiate scan to reveal hidden assets.</p>
                        </div>
                    )}

                    {assets.map((asset, i) => (
                        <motion.div
                            key={asset.id}
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: i * 0.1 }}
                        >
                            <DealCard
                                title={asset.title}
                                description={asset.description}
                                price={asset.price}
                                revenue={asset.revenue}
                                type={asset.type}
                                onAnalyze={() => handleAnalyze(asset)}
                            />
                        </motion.div>
                    ))}
                </div>

            </main>

            <ValuationDrawer
                isOpen={isDrawerOpen}
                onClose={() => setIsDrawerOpen(false)}
                data={selectedAsset}
            />
        </div>
    );
}
