import { Link } from 'react-router';
import { 
  Eye, Trash2, TrendingUp, AlertTriangle, XCircle, Bell, BellOff,
  ArrowUpRight, Package, Clock
} from 'lucide-react';
import { cn } from '@/lib/utils';

const watchlistItems = [
  { id: '1', name: "Portable LED Ring Light", verdict: 'pursue' as const, score: 82, added: '3 days ago', alerts: true, price_change: '+12%' },
  { id: '2', name: "Wireless Charging Pad", verdict: 'risky' as const, score: 54, added: '1 week ago', alerts: true, price_change: '-8%' },
  { id: '3', name: "Magnetic Phone Mount", verdict: 'pursue' as const, score: 76, added: '2 weeks ago', alerts: false, price_change: '+5%' },
  { id: '4', name: "Bluetooth Sleep Mask", verdict: 'skip' as const, score: 31, added: '3 weeks ago', alerts: true, price_change: '-15%' },
  { id: '5', name: "Car Phone Holder", verdict: 'pursue' as const, score: 88, added: '1 month ago', alerts: false, price_change: '+3%' },
];

const verdictConfig = {
  pursue: { color: '#00ff88', bg: 'rgba(0,255,136,0.1)', border: 'rgba(0,255,136,0.25)', icon: TrendingUp },
  risky: { color: '#ffd700', bg: 'rgba(255,215,0,0.1)', border: 'rgba(255,215,0,0.25)', icon: AlertTriangle },
  skip: { color: '#ff0040', bg: 'rgba(255,0,64,0.1)', border: 'rgba(255,0,64,0.25)', icon: XCircle },
};

export default function Watchlist() {
  return (
    <div className="max-w-5xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Watchlist</h1>
          <p className="text-white/40 mt-1">Track products and get alerted on changes</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="glass px-4 py-2 rounded-xl text-sm text-white/60">
            <Eye className="w-4 h-4 inline mr-2" />
            {watchlistItems.length} products
          </div>
        </div>
      </div>

      {/* Watchlist Grid */}
      <div className="space-y-3">
        {watchlistItems.map((item) => {
          const v = verdictConfig[item.verdict];
          const Icon = v.icon;
          
          return (
            <div 
              key={item.id}
              className="glass rounded-xl p-5 flex flex-col sm:flex-row items-start sm:items-center gap-4 hover:scale-[1.005] transition-all duration-200 group"
            >
              <div 
                className="w-14 h-14 rounded-xl flex items-center justify-center shrink-0"
                style={{ background: v.bg, border: `1px solid ${v.border}` }}
              >
                <Icon className="w-7 h-7" style={{ color: v.color }} />
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="text-lg font-semibold text-white truncate">{item.name}</h3>
                  <span 
                    className="px-2 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider"
                    style={{ background: v.bg, color: v.color, border: `1px solid ${v.border}` }}
                  >
                    {item.verdict}
                  </span>
                </div>
                <div className="flex items-center gap-4 text-xs text-white/40">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" /> {item.added}
                  </span>
                  <span className="flex items-center gap-1">
                    <Package className="w-3 h-3" /> Score: {item.score}
                  </span>
                  <span className={cn(
                    "flex items-center gap-1 font-medium",
                    item.price_change.startsWith('+') ? "text-emerald-400" : "text-red-400"
                  )}>
                    <TrendingUp className="w-3 h-3" /> {item.price_change}
                  </span>
                </div>
              </div>
              
              <div className="flex items-center gap-2 shrink-0">
                <button 
                  className={cn(
                    "p-2.5 rounded-xl transition-colors",
                    item.alerts 
                      ? "bg-cyan-400/10 text-cyan-400 hover:bg-cyan-400/20" 
                      : "bg-white/[0.03] text-white/30 hover:text-white/60"
                  )}
                >
                  {item.alerts ? <Bell className="w-4 h-4" /> : <BellOff className="w-4 h-4" />}
                </button>
                <Link 
                  to={`/product/${item.id}`}
                  className="p-2.5 rounded-xl bg-white/[0.03] text-white/40 hover:text-white hover:bg-white/[0.06] transition-colors"
                >
                  <ArrowUpRight className="w-4 h-4" />
                </Link>
                <button className="p-2.5 rounded-xl bg-white/[0.03] text-white/40 hover:text-red-400 hover:bg-red-400/10 transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Empty state would go here */}
      {watchlistItems.length === 0 && (
        <div className="glass rounded-2xl p-12 text-center">
          <Eye className="w-12 h-12 text-white/20 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-white/60">No products in watchlist</h3>
          <p className="text-white/30 mt-1">Analyze a product and add it here to track changes</p>
        </div>
      )}
    </div>
  );
}
