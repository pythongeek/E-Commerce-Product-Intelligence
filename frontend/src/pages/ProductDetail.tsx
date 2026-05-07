import { Link } from 'react-router';
import { 
  ArrowLeft, TrendingUp, AlertTriangle, XCircle, DollarSign, 
  Package, Users, Clock, Target, Eye, Share2, Download
} from 'lucide-react';
import { cn } from '@/lib/utils';

function DetailCard({ title, children, className }: { title: string; children: React.ReactNode; className?: string }) {
  return (
    <div className={cn("glass rounded-2xl p-6 space-y-4", className)}>
      <h3 className="text-sm font-semibold text-white/70 uppercase tracking-wider">{title}</h3>
      {children}
    </div>
  );
}

function ScoreBar({ label, score, max, color }: { label: string; score: number; max: number; color: string }) {
  const pct = (score / max) * 100;
  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between text-sm">
        <span className="text-white/60">{label}</span>
        <span className="font-semibold" style={{ color }}>{score}/{max}</span>
      </div>
      <div className="w-full h-2 bg-white/[0.06] rounded-full overflow-hidden">
        <div 
          className="h-full rounded-full transition-all duration-1000"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
    </div>
  );
}

export default function ProductDetail() {
  // const { id } = useParams();
  
  // Mock data
  const product = {
    name: "Portable LED Ring Light",
    verdict: 'pursue' as const,
    score: 82,
    confidence: 88,
    margin: 58,
    ali_price: 4.50,
    amazon_price: 29.99,
    active_ads: 147,
    avg_duration: 38,
    advertisers: 23,
    rating: 4.2,
    reviews: 3847,
    sentiment_pos: 72,
    sentiment_neg: 18,
    payback: 21,
    ad_budget: 400,
    alternatives: ["LED Selfie Ring Light with Tripod", "Clip-on Phone Ring Light", "Dimmable Makeup Ring Light"],
    complaints: ["battery life", "cable too short", "dim on max setting"],
    summary: "Strong ad momentum with 38-day average ad duration confirms profitability. Negative reviews cluster around battery and cable — fixable product improvements that create a differentiation opportunity.",
    risk: "High competition — 147 active ads indicates market saturation risk. Differentiate with bundled accessories.",
  };

  const verdictConfig = {
    pursue: { color: '#00ff88', bg: 'rgba(0,255,136,0.1)', border: 'rgba(0,255,136,0.25)', icon: TrendingUp, label: 'PURSUE' },
    risky: { color: '#ffd700', bg: 'rgba(255,215,0,0.1)', border: 'rgba(255,215,0,0.25)', icon: AlertTriangle, label: 'RISKY' },
    skip: { color: '#ff0040', bg: 'rgba(255,0,64,0.1)', border: 'rgba(255,0,64,0.25)', icon: XCircle, label: 'SKIP' },
  };

  const v = verdictConfig[product.verdict];
  const Icon = v.icon;

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Breadcrumb */}
      <Link to="/" className="inline-flex items-center gap-2 text-sm text-white/40 hover:text-white/70 transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back to Dashboard
      </Link>

      {/* Hero Verdict Card */}
      <div 
        className="glass-strong rounded-2xl p-8 relative overflow-hidden"
        style={{ borderColor: v.border }}
      >
        <div 
          className="absolute top-0 right-0 w-96 h-96 rounded-full blur-3xl opacity-20 -translate-y-1/2 translate-x-1/3"
          style={{ background: v.color }}
        />
        
        <div className="relative flex flex-col lg:flex-row items-start lg:items-center gap-6">
          <div 
            className="w-20 h-20 rounded-2xl flex items-center justify-center shrink-0"
            style={{ background: v.bg, border: `2px solid ${v.border}` }}
          >
            <Icon className="w-10 h-10" style={{ color: v.color }} />
          </div>
          
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <span 
                className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider"
                style={{ background: v.bg, color: v.color, border: `1px solid ${v.border}` }}
              >
                {v.label}
              </span>
              <span className="text-xs text-white/30 flex items-center gap-1">
                <Clock className="w-3 h-3" /> Analyzed just now
              </span>
            </div>
            <h1 className="text-3xl font-bold text-white">{product.name}</h1>
            <p className="text-white/50 mt-2 max-w-2xl">{product.summary}</p>
          </div>
          
          <div className="flex items-center gap-8 shrink-0">
            <div className="text-center">
              <div className="text-6xl font-bold" style={{ color: v.color }}>{product.score}</div>
              <div className="text-xs text-white/40 uppercase tracking-wider mt-1">Product Score</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-white/80">{product.confidence}%</div>
              <div className="text-xs text-white/40 uppercase tracking-wider mt-1">Confidence</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Score Breakdown */}
        <DetailCard title="Score Breakdown" className="lg:col-span-1">
          <div className="space-y-4">
            <ScoreBar label="Profit Margin" score={24} max={30} color="#00f0ff" />
            <ScoreBar label="Ad Momentum" score={22} max={25} color="#ff00a0" />
            <ScoreBar label="Review Sentiment" score={14} max={20} color="#00ff88" />
            <ScoreBar label="Demand Trend" score={10} max={15} color="#ffd700" />
            <ScoreBar label="Competition" score={4} max={10} color="#ff0040" />
          </div>
          
          <div className="pt-4 border-t border-white/[0.06]">
            <div className="flex items-center gap-2 text-sm text-white/50">
              <Target className="w-4 h-4 text-red-400" />
              <span>Main Risk: <span className="text-white/70">{product.risk}</span></span>
            </div>
          </div>
        </DetailCard>

        {/* Financials */}
        <DetailCard title="Financial Overview" className="lg:col-span-1">
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-white/[0.02] text-center">
              <DollarSign className="w-5 h-5 text-cyan-400 mx-auto mb-2" />
              <div className="text-xl font-bold text-white">${product.ali_price}</div>
              <div className="text-xs text-white/40">Ali Cost</div>
            </div>
            <div className="p-4 rounded-xl bg-white/[0.02] text-center">
              <DollarSign className="w-5 h-5 text-fuchsia-400 mx-auto mb-2" />
              <div className="text-xl font-bold text-white">${product.amazon_price}</div>
              <div className="text-xs text-white/40">Amazon Price</div>
            </div>
            <div className="p-4 rounded-xl bg-white/[0.02] text-center">
              <TrendingUp className="w-5 h-5 text-emerald-400 mx-auto mb-2" />
              <div className="text-xl font-bold text-emerald-400">{product.margin}%</div>
              <div className="text-xs text-white/40">Est. Margin</div>
            </div>
            <div className="p-4 rounded-xl bg-white/[0.02] text-center">
              <Clock className="w-5 h-5 text-amber-400 mx-auto mb-2" />
              <div className="text-xl font-bold text-amber-400">{product.payback}d</div>
              <div className="text-xs text-white/40">Payback</div>
            </div>
          </div>
          
          <div className="p-4 rounded-xl bg-cyan-400/5 border border-cyan-400/10">
            <div className="flex items-center justify-between text-sm">
              <span className="text-white/60">Suggested Ad Budget</span>
              <span className="font-bold text-cyan-400">${product.ad_budget}/mo</span>
            </div>
          </div>
        </DetailCard>

        {/* Data Signals */}
        <DetailCard title="Raw Signals" className="lg:col-span-1">
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02]">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center">
                  <Users className="w-5 h-5 text-blue-400" />
                </div>
                <div>
                  <div className="text-sm font-medium text-white">Facebook Ads</div>
                  <div className="text-xs text-white/40">{product.active_ads} active ads</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-bold text-white">{product.advertisers}</div>
                <div className="text-xs text-white/40">advertisers</div>
              </div>
            </div>
            
            <div className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02]">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-orange-500/10 flex items-center justify-center">
                  <Package className="w-5 h-5 text-orange-400" />
                </div>
                <div>
                  <div className="text-sm font-medium text-white">Amazon Reviews</div>
                  <div className="text-xs text-white/40">{product.reviews.toLocaleString()} reviews</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-bold text-white">{product.rating}</div>
                <div className="text-xs text-white/40">avg rating</div>
              </div>
            </div>
            
            <div className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02]">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center">
                  <Clock className="w-5 h-5 text-purple-400" />
                </div>
                <div>
                  <div className="text-sm font-medium text-white">Ad Duration</div>
                  <div className="text-xs text-white/40">Avg lifetime</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-bold text-white">{product.avg_duration}d</div>
                <div className="text-xs text-white/40">strong signal</div>
              </div>
            </div>
          </div>
        </DetailCard>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DetailCard title="Top Complaints (Differentiation Opportunities)">
          <div className="space-y-2">
            {product.complaints.map((c, i) => (
              <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-red-400/5 border border-red-400/10">
                <XCircle className="w-5 h-5 text-red-400 shrink-0" />
                <span className="text-sm text-white/70">{c}</span>
                <span className="ml-auto text-xs text-red-400/60 font-medium">Fixable</span>
              </div>
            ))}
          </div>
        </DetailCard>

        <DetailCard title="Top 3 Alternatives">
          <div className="space-y-2">
            {product.alternatives.map((alt, i) => (
              <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-white/[0.02] hover:bg-white/[0.04] transition-colors cursor-pointer group">
                <div className="w-8 h-8 rounded-lg bg-cyan-400/10 flex items-center justify-center text-cyan-400 text-xs font-bold">
                  {i + 1}
                </div>
                <span className="text-sm text-white/70 group-hover:text-white transition-colors">{alt}</span>
                <ArrowLeft className="w-4 h-4 text-white/20 ml-auto rotate-180 group-hover:text-cyan-400 transition-colors" />
              </div>
            ))}
          </div>
        </DetailCard>
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-3">
        <button className="flex items-center gap-2 px-6 py-3 rounded-xl bg-white/[0.05] text-white font-semibold hover:bg-white/[0.08] transition-colors">
          <Eye className="w-4 h-4" /> Add to Watchlist
        </button>
        <button className="flex items-center gap-2 px-6 py-3 rounded-xl bg-white/[0.05] text-white font-semibold hover:bg-white/[0.08] transition-colors">
          <Share2 className="w-4 h-4" /> Share Report
        </button>
        <button className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-400 to-blue-500 text-white font-semibold hover:shadow-lg hover:shadow-cyan-500/30 transition-all">
          <Download className="w-4 h-4" /> Export PDF
        </button>
      </div>
    </div>
  );
}
