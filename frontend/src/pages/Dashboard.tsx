import { Link } from 'react-router';
import { 
  TrendingUp, Eye, Search, ArrowUpRight, ArrowDownRight, 
  Zap, Activity, BarChart3
} from 'lucide-react';
import { cn } from '@/lib/utils';

function StatCard({ 
  title, value, change, changeType, icon: Icon, color,
  delay = 0
}: {
  title: string;
  value: string;
  change: string;
  changeType: 'up' | 'down' | 'neutral';
  icon: React.ElementType;
  color: string;
  delay?: number;
}) {
  return (
    <div 
      className={cn(
        "glass rounded-2xl p-6 relative overflow-hidden group hover:scale-[1.02] transition-all duration-300",
        color === 'cyan' && "neon-border-cyan",
        color === 'magenta' && "neon-border-magenta",
        color === 'green' && "neon-border-green",
        color === 'yellow' && "neon-border-yellow",
      )}
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className={cn(
        "absolute top-0 right-0 w-32 h-32 opacity-10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2",
        color === 'cyan' && "bg-cyan-400",
        color === 'magenta' && "bg-fuchsia-500",
        color === 'green' && "bg-emerald-400",
        color === 'yellow' && "bg-amber-400",
      )} />
      
      <div className="flex items-start justify-between mb-4">
        <div className={cn(
          "p-3 rounded-xl",
          color === 'cyan' && "bg-cyan-400/10 text-cyan-400",
          color === 'magenta' && "bg-fuchsia-500/10 text-fuchsia-400",
          color === 'green' && "bg-emerald-400/10 text-emerald-400",
          color === 'yellow' && "bg-amber-400/10 text-amber-400",
        )}>
          <Icon className="w-5 h-5" />
        </div>
        <div className={cn(
          "flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-full",
          changeType === 'up' && "bg-emerald-500/10 text-emerald-400",
          changeType === 'down' && "bg-red-500/10 text-red-400",
          changeType === 'neutral' && "bg-white/5 text-white/50",
        )}>
          {changeType === 'up' && <ArrowUpRight className="w-3 h-3" />}
          {changeType === 'down' && <ArrowDownRight className="w-3 h-3" />}
          {change}
        </div>
      </div>
      
      <p className="text-white/40 text-sm font-medium mb-1">{title}</p>
      <p className="text-2xl font-bold text-white tracking-tight">{value}</p>
    </div>
  );
}

function RecentAnalysis({ 
  name, verdict, score, date, trend 
}: {
  name: string;
  verdict: 'pursue' | 'risky' | 'skip';
  score: number;
  date: string;
  trend: 'up' | 'down';
}) {
  const verdictConfig = {
    pursue: { color: '#00ff88', bg: 'rgba(0,255,136,0.1)', border: 'rgba(0,255,136,0.25)', icon: TrendingUp },
    risky: { color: '#ffd700', bg: 'rgba(255,215,0,0.1)', border: 'rgba(255,215,0,0.25)', icon: Activity },
    skip: { color: '#ff0040', bg: 'rgba(255,0,64,0.1)', border: 'rgba(255,0,64,0.25)', icon: ArrowDownRight },
  };
  
  const config = verdictConfig[verdict];
  const Icon = config.icon;

  return (
    <div 
      className="glass rounded-xl p-4 flex items-center gap-4 hover:scale-[1.01] transition-all duration-200 group cursor-pointer"
      style={{ borderColor: 'rgba(255,255,255,0.06)' }}
    >
      <div 
        className="w-12 h-12 rounded-xl flex items-center justify-center shrink-0"
        style={{ background: config.bg, border: `1px solid ${config.border}` }}
      >
        <Icon className="w-5 h-5" style={{ color: config.color }} />
      </div>
      
      <div className="flex-1 min-w-0">
        <h4 className="text-sm font-semibold text-white truncate">{name}</h4>
        <div className="flex items-center gap-2 mt-0.5">
          <span 
            className="text-xs font-medium px-2 py-0.5 rounded-full uppercase tracking-wider"
            style={{ background: config.bg, color: config.color, border: `1px solid ${config.border}` }}
          >
            {verdict}
          </span>
          <span className="text-xs text-white/30">{date}</span>
        </div>
      </div>
      
      <div className="text-right shrink-0">
        <div className="text-lg font-bold" style={{ color: config.color }}>{score}</div>
        <div className="text-xs text-white/30">score</div>
      </div>
      
      <div className="w-24 h-8 hidden sm:block">
        <svg viewBox="0 0 96 32" className="w-full h-full">
          <path
            d={trend === 'up' ? "M0 28 L24 20 L48 24 L72 8 L96 4" : "M0 8 L24 16 L48 12 L72 24 L96 28"}
            fill="none"
            stroke={config.color}
            strokeWidth="2"
            strokeLinecap="round"
            opacity="0.6"
          />
        </svg>
      </div>
    </div>
  );
}

function ScoreRing({ score, label, color }: { score: number; label: string; color: string }) {
  const circumference = 2 * Math.PI * 36;
  const offset = circumference - (score / 100) * circumference;
  
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative w-20 h-20">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 80 80">
          <circle cx="40" cy="40" r="36" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="6" />
          <circle 
            cx="40" 
            cy="40" 
            r="36" 
            fill="none" 
            stroke={color} 
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-sm font-bold text-white">{score}</span>
        </div>
      </div>
      <span className="text-xs text-white/50 font-medium">{label}</span>
    </div>
  );
}

export default function Dashboard() {
  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">
            Dashboard
          </h1>
          <p className="text-white/40 mt-1">Track your product intelligence at a glance</p>
        </div>
        <Link 
          to="/analyze"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-400 to-blue-500 text-white font-semibold text-sm hover:shadow-lg hover:shadow-cyan-500/25 transition-all duration-300 hover:scale-105"
        >
          <Zap className="w-4 h-4" />
          New Analysis
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Total Analyses" value="247" change="+12%" changeType="up" icon={BarChart3} color="cyan" delay={0} />
        <StatCard title="Winning Products" value="89" change="+8%" changeType="up" icon={TrendingUp} color="green" delay={100} />
        <StatCard title="Watchlist" value="34" change="+3" changeType="up" icon={Eye} color="magenta" delay={200} />
        <StatCard title="Avg. Score" value="72.4" change="-2.1" changeType="down" icon={Activity} color="yellow" delay={300} />
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Analyses */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Recent Analyses</h2>
            <Link to="/analyze" className="text-sm text-cyan-400 hover:text-cyan-300 transition-colors flex items-center gap-1">
              View All <ArrowUpRight className="w-4 h-4" />
            </Link>
          </div>
          
          <div className="space-y-3">
            <RecentAnalysis name="Portable LED Ring Light" verdict="pursue" score={82} date="2h ago" trend="up" />
            <RecentAnalysis name="Wireless Charging Pad" verdict="risky" score={54} date="5h ago" trend="down" />
            <RecentAnalysis name="Magnetic Phone Mount" verdict="pursue" score={76} date="1d ago" trend="up" />
            <RecentAnalysis name="Bluetooth Sleep Mask" verdict="skip" score={31} date="1d ago" trend="down" />
            <RecentAnalysis name="Car Phone Holder" verdict="pursue" score={88} date="2d ago" trend="up" />
          </div>
        </div>

        {/* Score Breakdown */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-white">Score Breakdown</h2>
          
          <div className="glass rounded-2xl p-6 space-y-6">
            <div className="text-center">
              <div className="relative w-40 h-40 mx-auto">
                <svg className="w-full h-full -rotate-90" viewBox="0 0 160 160">
                  <circle cx="80" cy="80" r="70" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="10" />
                  <circle 
                    cx="80" 
                    cy="80" 
                    r="70" 
                    fill="none" 
                    stroke="url(#scoreGradient)" 
                    strokeWidth="10"
                    strokeLinecap="round"
                    strokeDasharray={2 * Math.PI * 70}
                    strokeDashoffset={2 * Math.PI * 70 * (1 - 0.72)}
                    className="transition-all duration-1000"
                  />
                  <defs>
                    <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#00f0ff" />
                      <stop offset="100%" stopColor="#ff00a0" />
                    </linearGradient>
                  </defs>
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-4xl font-bold text-white">72</span>
                  <span className="text-xs text-white/40 uppercase tracking-wider">Avg Score</span>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <ScoreRing score={24} label="Profit Margin" color="#00f0ff" />
              <ScoreRing score={22} label="Ad Momentum" color="#ff00a0" />
              <ScoreRing score={14} label="Sentiment" color="#00ff88" />
              <ScoreRing score={10} label="Trend" color="#ffd700" />
            </div>
          </div>
          
          {/* Quick Actions */}
          <div className="glass rounded-2xl p-4 space-y-3">
            <h3 className="text-sm font-semibold text-white/70">Quick Actions</h3>
            <Link to="/analyze" className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/[0.04] transition-colors group">
              <div className="w-10 h-10 rounded-lg bg-cyan-400/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Search className="w-5 h-5 text-cyan-400" />
              </div>
              <div>
                <p className="text-sm font-medium text-white">New Analysis</p>
                <p className="text-xs text-white/40">Research a product idea</p>
              </div>
            </Link>
            <Link to="/watchlist" className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/[0.04] transition-colors group">
              <div className="w-10 h-10 rounded-lg bg-fuchsia-500/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Eye className="w-5 h-5 text-fuchsia-400" />
              </div>
              <div>
                <p className="text-sm font-medium text-white">Watchlist</p>
                <p className="text-xs text-white/40">34 products tracked</p>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
