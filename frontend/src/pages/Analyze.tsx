import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { 
  Search, Zap, Loader2, Globe, Store, ArrowRight, Sparkles,
  TrendingUp, AlertTriangle, XCircle, CheckCircle, Eye
} from 'lucide-react';
import { cn } from '@/lib/utils';

const markets = [
  { code: 'US', flag: '🇺🇸', name: 'United States' },
  { code: 'UK', flag: '🇬🇧', name: 'United Kingdom' },
  { code: 'CA', flag: '🇨🇦', name: 'Canada' },
  { code: 'AU', flag: '🇦🇺', name: 'Australia' },
  { code: 'DE', flag: '🇩🇪', name: 'Germany' },
  { code: 'FR', flag: '🇫🇷', name: 'France' },
  { code: 'IN', flag: '🇮🇳', name: 'India' },
  { code: 'BD', flag: '🇧🇩', name: 'Bangladesh' },
];

const platforms = [
  { id: 'amazon', name: 'Amazon FBA', color: '#FF9900' },
  { id: 'shopify', name: 'Shopify', color: '#96BF48' },
  { id: 'ebay', name: 'eBay', color: '#E53238' },
  { id: 'etsy', name: 'Etsy', color: '#F16521' },
];

function AnalysisStep({ step, label, active, completed }: { step: number; label: string; active: boolean; completed: boolean }) {
  return (
    <div className="flex items-center gap-3">
      <div className={cn(
        "w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300",
        completed && "bg-emerald-400/20 text-emerald-400 border border-emerald-400/30",
        active && !completed && "bg-cyan-400/20 text-cyan-400 border border-cyan-400/30 animate-pulse-glow",
        !active && !completed && "bg-white/5 text-white/30 border border-white/10"
      )}>
        {completed ? <CheckCircle className="w-4 h-4" /> : step}
      </div>
      <span className={cn(
        "text-sm font-medium transition-colors",
        active && "text-white",
        !active && "text-white/40"
      )}>
        {label}
      </span>
    </div>
  );
}

export default function Analyze() {
  const navigate = useNavigate();
  const [productName, setProductName] = useState('');
  const [selectedMarket, setSelectedMarket] = useState('US');
  const [selectedPlatform, setSelectedPlatform] = useState('amazon');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<any>(null);

  const steps = [
    { label: 'Facebook Ads', duration: 2000 },
    { label: 'Alibaba Pricing', duration: 2000 },
    { label: 'Amazon Reviews', duration: 2000 },
    { label: 'AI Analysis', duration: 3000 },
  ];

  const startAnalysis = async () => {
    if (!productName.trim()) return;
    
    setIsAnalyzing(true);
    setCurrentStep(0);
    setProgress(0);
    setResult(null);

    // Simulate step-by-step progress
    for (let i = 0; i < steps.length; i++) {
      setCurrentStep(i);
      const stepProgress = (i / steps.length) * 100;
      
      // Animate progress within step
      for (let p = 0; p <= 25; p += 2) {
        setProgress(stepProgress + p);
        await new Promise(r => setTimeout(r, steps[i].duration / 15));
      }
    }

    setCurrentStep(4);
    setProgress(100);

    // Mock result
    const mockResult = {
      verdict: Math.random() > 0.4 ? 'pursue' : Math.random() > 0.5 ? 'risky' : 'skip',
      score: Math.floor(Math.random() * 40) + 55,
      confidence: Math.floor(Math.random() * 20) + 75,
    };

    await new Promise(r => setTimeout(r, 800));
    setResult(mockResult);
    setIsAnalyzing(false);
  };

  const verdictConfig = {
    pursue: {
      color: '#00ff88',
      bg: 'rgba(0,255,136,0.1)',
      border: 'rgba(0,255,136,0.25)',
      icon: TrendingUp,
      label: 'PURSUE',
      desc: 'Strong signals across all channels',
    },
    risky: {
      color: '#ffd700',
      bg: 'rgba(255,215,0,0.1)',
      border: 'rgba(255,215,0,0.25)',
      icon: AlertTriangle,
      label: 'RISKY',
      desc: 'Mixed signals, proceed with caution',
    },
    skip: {
      color: '#ff0040',
      bg: 'rgba(255,0,64,0.1)',
      border: 'rgba(255,0,64,0.25)',
      icon: XCircle,
      label: 'SKIP',
      desc: 'Weak demand or oversaturated market',
    },
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-400/10 border border-cyan-400/20 text-cyan-400 text-xs font-semibold uppercase tracking-wider">
          <Sparkles className="w-3.5 h-3.5" />
          AI-Powered Analysis
        </div>
        <h1 className="text-4xl font-bold text-white tracking-tight">
          Analyze a <span className="text-gradient-cyan">Product</span>
        </h1>
        <p className="text-white/40 max-w-lg mx-auto">
          Enter a product name and we'll scrape Facebook Ads, Alibaba, Amazon, and Google Trends to give you a verdict in under 90 seconds.
        </p>
      </div>

      {/* Input Card */}
      <div className="glass-strong rounded-2xl p-6 lg:p-8 space-y-6">
        {/* Product Name Input */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-white/70">Product Name or Keyword</label>
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
            <input
              type="text"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              placeholder="e.g. Portable LED Ring Light"
              className="w-full pl-12 pr-4 py-4 bg-white/[0.04] border border-white/[0.08] rounded-xl text-white placeholder:text-white/20 focus:outline-none focus:border-cyan-400/40 focus:ring-1 focus:ring-cyan-400/20 transition-all text-lg"
              onKeyDown={(e) => e.key === 'Enter' && startAnalysis()}
              disabled={isAnalyzing}
            />
          </div>
        </div>

        {/* Market Selection */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-white/70 flex items-center gap-2">
            <Globe className="w-4 h-4" /> Target Market
          </label>
          <div className="flex flex-wrap gap-2">
            {markets.map((m) => (
              <button
                key={m.code}
                onClick={() => setSelectedMarket(m.code)}
                disabled={isAnalyzing}
                className={cn(
                  "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200",
                  selectedMarket === m.code
                    ? "bg-cyan-400/10 text-cyan-400 border border-cyan-400/30"
                    : "bg-white/[0.03] text-white/50 border border-white/[0.06] hover:bg-white/[0.06] hover:text-white/70"
                )}
              >
                <span>{m.flag}</span>
                <span className="hidden sm:inline">{m.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Platform Selection */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-white/70 flex items-center gap-2">
            <Store className="w-4 h-4" /> Selling Platform
          </label>
          <div className="flex flex-wrap gap-2">
            {platforms.map((p) => (
              <button
                key={p.id}
                onClick={() => setSelectedPlatform(p.id)}
                disabled={isAnalyzing}
                className={cn(
                  "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200",
                  selectedPlatform === p.id
                    ? "text-white border"
                    : "bg-white/[0.03] text-white/50 border border-white/[0.06] hover:bg-white/[0.06]"
                )}
                style={selectedPlatform === p.id ? { borderColor: p.color + '40', background: p.color + '15' } : {}}
              >
                <span className="w-2 h-2 rounded-full" style={{ background: p.color }} />
                {p.name}
              </button>
            ))}
          </div>
        </div>

        {/* Analyze Button */}
        <button
          onClick={startAnalysis}
          disabled={isAnalyzing || !productName.trim()}
          className={cn(
            "w-full py-4 rounded-xl font-bold text-lg flex items-center justify-center gap-3 transition-all duration-300",
            isAnalyzing
              ? "bg-white/5 text-white/40 cursor-not-allowed"
              : "bg-gradient-to-r from-cyan-400 to-blue-500 text-white hover:shadow-lg hover:shadow-cyan-500/30 hover:scale-[1.02] active:scale-[0.98]"
          )}
        >
          {isAnalyzing ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <Zap className="w-5 h-5" />
              Start Analysis
            </>
          )}
        </button>
      </div>

      {/* Progress */}
      {isAnalyzing && (
        <div className="glass rounded-2xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-white">Analysis Progress</h3>
            <span className="text-2xl font-bold text-cyan-400">{progress}%</span>
          </div>
          
          <div className="w-full h-2 bg-white/[0.06] rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {steps.map((s, i) => (
              <AnalysisStep
                key={s.label}
                step={i + 1}
                label={s.label}
                active={currentStep === i}
                completed={currentStep > i}
              />
            ))}
          </div>
        </div>
      )}

      {/* Result Card */}
      {result && (
        <div 
          className="glass-strong rounded-2xl p-8 space-y-6 animate-float"
          style={{ 
            borderColor: verdictConfig[result.verdict as keyof typeof verdictConfig].border,
            boxShadow: `0 0 40px ${verdictConfig[result.verdict as keyof typeof verdictConfig].color}15`
          }}
        >
          <div className="flex flex-col sm:flex-row items-center gap-6">
            <div 
              className="w-24 h-24 rounded-2xl flex items-center justify-center"
              style={{ 
                background: verdictConfig[result.verdict as keyof typeof verdictConfig].bg,
                border: `2px solid ${verdictConfig[result.verdict as keyof typeof verdictConfig].border}`
              }}
            >
              {React.createElement(verdictConfig[result.verdict as keyof typeof verdictConfig].icon, { 
                className: "w-12 h-12",
                style: { color: verdictConfig[result.verdict as keyof typeof verdictConfig].color }
              })}
            </div>
            
            <div className="flex-1 text-center sm:text-left">
              <div 
                className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-bold uppercase tracking-wider mb-2"
                style={{ 
                  background: verdictConfig[result.verdict as keyof typeof verdictConfig].bg,
                  color: verdictConfig[result.verdict as keyof typeof verdictConfig].color,
                  border: `1px solid ${verdictConfig[result.verdict as keyof typeof verdictConfig].border}`
                }}
              >
                {verdictConfig[result.verdict as keyof typeof verdictConfig].label}
              </div>
              <h2 className="text-2xl font-bold text-white">{productName}</h2>
              <p className="text-white/50 mt-1">
                {verdictConfig[result.verdict as keyof typeof verdictConfig].desc}
              </p>
            </div>
            
            <div className="text-center">
              <div className="text-5xl font-bold" style={{ color: verdictConfig[result.verdict as keyof typeof verdictConfig].color }}>
                {result.score}
              </div>
              <div className="text-xs text-white/40 uppercase tracking-wider mt-1">Product Score</div>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-white/[0.06]">
            <div className="text-center p-4 rounded-xl bg-white/[0.02]">
              <div className="text-xl font-bold text-cyan-400">{Math.floor(Math.random() * 20 + 15)}%</div>
              <div className="text-xs text-white/40 mt-1">Est. Margin</div>
            </div>
            <div className="text-center p-4 rounded-xl bg-white/[0.02]">
              <div className="text-xl font-bold text-fuchsia-400">${Math.floor(Math.random() * 30 + 15)}</div>
              <div className="text-xs text-white/40 mt-1">Ali Price</div>
            </div>
            <div className="text-center p-4 rounded-xl bg-white/[0.02]">
              <div className="text-xl font-bold text-emerald-400">{Math.floor(Math.random() * 100 + 50)}</div>
              <div className="text-xs text-white/40 mt-1">Active Ads</div>
            </div>
            <div className="text-center p-4 rounded-xl bg-white/[0.02]">
              <div className="text-xl font-bold text-amber-400">{result.confidence}%</div>
              <div className="text-xs text-white/40 mt-1">Confidence</div>
            </div>
          </div>

          <div className="flex gap-3">
            <button className="flex-1 py-3 rounded-xl bg-white/[0.05] text-white font-semibold hover:bg-white/[0.08] transition-colors flex items-center justify-center gap-2">
              <Eye className="w-4 h-4" /> Add to Watchlist
            </button>
            <button 
              onClick={() => navigate(`/product/${Date.now()}`)}
              className="flex-1 py-3 rounded-xl bg-gradient-to-r from-cyan-400 to-blue-500 text-white font-semibold hover:shadow-lg hover:shadow-cyan-500/30 transition-all flex items-center justify-center gap-2"
            >
              View Full Report <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
