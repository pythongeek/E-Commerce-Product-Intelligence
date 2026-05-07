import { 
  Zap, Eye, BarChart3, Check, Key,
  Globe, Mail, Bell, Moon, Database
} from 'lucide-react';
import { cn } from '@/lib/utils';

const plans = [
  {
    id: 'starter',
    name: 'Starter',
    price: 49,
    color: '#00f0ff',
    features: ['50 analyses/day', '10 watchlist items', '5 exports/month', 'Email support'],
    current: false,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: 149,
    color: '#ff00a0',
    features: ['500 analyses/day', '100 watchlist items', '50 exports/month', 'Priority support', 'API access'],
    current: true,
  },
  {
    id: 'agency',
    name: 'Agency',
    price: 499,
    color: '#00ff88',
    features: ['5000 analyses/day', '1000 watchlist items', '500 exports/month', 'White-label reports', 'Dedicated support'],
    current: false,
  },
];

function PlanCard({ plan }: { plan: typeof plans[0] }) {
  return (
    <div 
      className={cn(
        "glass rounded-2xl p-6 relative overflow-hidden transition-all duration-300 hover:scale-[1.02]",
        plan.current && "neon-border-cyan"
      )}
    >
      {plan.current && (
        <div className="absolute top-4 right-4 px-3 py-1 rounded-full bg-cyan-400/10 text-cyan-400 text-xs font-bold uppercase tracking-wider border border-cyan-400/20">
          Current Plan
        </div>
      )}
      
      <div 
        className="w-12 h-12 rounded-xl flex items-center justify-center mb-4"
        style={{ background: plan.color + '15', border: `1px solid ${plan.color}25` }}
      >
        <Zap className="w-6 h-6" style={{ color: plan.color }} />
      </div>
      
      <h3 className="text-xl font-bold text-white">{plan.name}</h3>
      <div className="flex items-baseline gap-1 mt-2 mb-6">
        <span className="text-3xl font-bold text-white">${plan.price}</span>
        <span className="text-white/40 text-sm">/month</span>
      </div>
      
      <ul className="space-y-3">
        {plan.features.map((feature, i) => (
          <li key={i} className="flex items-center gap-2 text-sm text-white/60">
            <Check className="w-4 h-4 shrink-0" style={{ color: plan.color }} />
            {feature}
          </li>
        ))}
      </ul>
      
      <button 
        className={cn(
          "w-full mt-6 py-3 rounded-xl font-semibold text-sm transition-all duration-200",
          plan.current 
            ? "bg-white/[0.05] text-white/40 cursor-default"
            : "bg-white/[0.05] text-white hover:bg-white/[0.1]"
        )}
      >
        {plan.current ? 'Current Plan' : 'Upgrade'}
      </button>
    </div>
  );
}

export default function SettingsPage() {
  return (
    <div className="max-w-5xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight">Settings</h1>
        <p className="text-white/40 mt-1">Manage your account, plan, and preferences</p>
      </div>

      {/* Plans */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-white">Subscription Plan</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {plans.map(plan => (
            <PlanCard key={plan.id} plan={plan} />
          ))}
        </div>
      </div>

      {/* Usage */}
      <div className="glass rounded-2xl p-6 space-y-6">
        <h2 className="text-lg font-semibold text-white">Current Usage</h2>
        
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-white/50 flex items-center gap-2">
                <BarChart3 className="w-4 h-4" /> Daily Analyses
              </span>
              <span className="text-white font-medium">42/500</span>
            </div>
            <div className="w-full h-2 bg-white/[0.06] rounded-full overflow-hidden">
              <div className="h-full w-[8%] bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full" />
            </div>
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-white/50 flex items-center gap-2">
                <Eye className="w-4 h-4" /> Watchlist
              </span>
              <span className="text-white font-medium">34/100</span>
            </div>
            <div className="w-full h-2 bg-white/[0.06] rounded-full overflow-hidden">
              <div className="h-full w-[34%] bg-gradient-to-r from-fuchsia-400 to-pink-500 rounded-full" />
            </div>
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-white/50 flex items-center gap-2">
                <Database className="w-4 h-4" /> Exports
              </span>
              <span className="text-white font-medium">12/50</span>
            </div>
            <div className="w-full h-2 bg-white/[0.06] rounded-full overflow-hidden">
              <div className="h-full w-[24%] bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full" />
            </div>
          </div>
        </div>
      </div>

      {/* Preferences */}
      <div className="glass rounded-2xl p-6 space-y-4">
        <h2 className="text-lg font-semibold text-white">Preferences</h2>
        
        <div className="space-y-3">
          {[
            { icon: Bell, label: 'Email Notifications', desc: 'Get alerts when watchlist products change', enabled: true },
            { icon: Mail, label: 'Weekly Digest', desc: 'Receive a summary of your analyses every week', enabled: true },
            { icon: Globe, label: 'Default Market', desc: 'United States', enabled: false, value: 'US' },
            { icon: Moon, label: 'Dark Mode', desc: 'Always on for this interface', enabled: true },
          ].map((pref, i) => (
            <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white/[0.02] hover:bg-white/[0.04] transition-colors">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-white/[0.04] flex items-center justify-center text-white/50">
                  <pref.icon className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-sm font-medium text-white">{pref.label}</div>
                  <div className="text-xs text-white/40">{pref.desc}</div>
                </div>
              </div>
              <div className={cn(
                "w-11 h-6 rounded-full relative transition-colors",
                pref.enabled ? "bg-cyan-400/30" : "bg-white/10"
              )}>
                <div className={cn(
                  "absolute top-1 w-4 h-4 rounded-full transition-all duration-200",
                  pref.enabled ? "left-6 bg-cyan-400" : "left-1 bg-white/40"
                )} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* API Keys */}
      <div className="glass rounded-2xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">API Access</h2>
          <div className="px-3 py-1 rounded-full bg-emerald-400/10 text-emerald-400 text-xs font-bold border border-emerald-400/20">
            Pro Feature
          </div>
        </div>
        
        <div className="p-4 rounded-xl bg-white/[0.02] border border-dashed border-white/10">
          <div className="flex items-center gap-3">
            <Key className="w-5 h-5 text-white/30" />
            <div className="flex-1">
              <div className="text-sm font-medium text-white/60">API Key</div>
              <div className="text-xs text-white/30 font-mono mt-0.5">pk_live_••••••••••••••••••••••••••••••</div>
            </div>
            <button className="px-4 py-2 rounded-lg bg-white/[0.05] text-white/60 text-sm hover:bg-white/[0.08] transition-colors">
              Reveal
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
