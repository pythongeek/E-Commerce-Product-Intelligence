import { useState } from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation, Navigate } from 'react-router';
import { 
  Zap, Search, Eye, Settings, Menu, X, 
  Sparkles, Bell, User, ChevronRight
} from 'lucide-react';
import { cn } from '@/lib/utils';
import Dashboard from '@/pages/Dashboard';
import Analyze from '@/pages/Analyze';
import ProductDetail from '@/pages/ProductDetail';
import Watchlist from '@/pages/Watchlist';
import SettingsPage from '@/pages/Settings';

function Sidebar({ isOpen, setIsOpen }: { isOpen: boolean; setIsOpen: (v: boolean) => void }) {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: Zap, label: 'Dashboard' },
    { path: '/analyze', icon: Search, label: 'Analyze' },
    { path: '/watchlist', icon: Eye, label: 'Watchlist' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
      
      {/* Sidebar */}
      <aside className={cn(
        "fixed top-0 left-0 z-50 h-full w-72 gradient-bg border-r border-white/[0.06] transition-transform duration-300 ease-out",
        isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      )}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center gap-3 px-6 py-6 border-b border-white/[0.06]">
            <div className="relative w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Sparkles className="w-5 h-5 text-white" />
              <div className="absolute inset-0 rounded-xl bg-cyan-400/20 animate-pulse" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white">ProductIntel</h1>
              <p className="text-[10px] uppercase tracking-widest text-cyan-400/70 font-semibold">AI Powered</p>
            </div>
            <button 
              onClick={() => setIsOpen(false)}
              className="ml-auto lg:hidden text-white/60 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Nav */}
          <nav className="flex-1 px-4 py-6 space-y-1">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path || location.pathname.startsWith(item.path + '/');
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setIsOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group",
                    isActive 
                      ? "bg-cyan-500/10 text-cyan-400 neon-border-cyan"
                      : "text-white/50 hover:text-white hover:bg-white/[0.04]"
                  )}
                >
                  <item.icon className={cn(
                    "w-5 h-5 transition-transform duration-200",
                    isActive ? "glow-cyan" : "group-hover:scale-110"
                  )} />
                  <span>{item.label}</span>
                  {isActive && (
                    <ChevronRight className="w-4 h-4 ml-auto opacity-60" />
                  )}
                </Link>
              );
            })}
          </nav>

          {/* Bottom stats */}
          <div className="px-6 py-4 border-t border-white/[0.06]">
            <div className="glass rounded-xl p-4 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="text-white/40">Plan</span>
                <span className="text-cyan-400 font-semibold">Pro</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-white/40">Analyses</span>
                <span className="text-white/70">42/500</span>
              </div>
              <div className="w-full h-1 bg-white/[0.06] rounded-full overflow-hidden">
                <div className="h-full w-[8%] bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full" />
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}

function TopBar({ onMenuClick }: { onMenuClick: () => void }) {
  return (
    <header className="sticky top-0 z-30 glass-strong border-b border-white/[0.06]">
      <div className="flex items-center justify-between px-4 lg:px-8 h-16">
        <div className="flex items-center gap-4">
          <button 
            onClick={onMenuClick}
            className="lg:hidden p-2 rounded-lg hover:bg-white/[0.06] text-white/70"
          >
            <Menu className="w-5 h-5" />
          </button>
          <div className="hidden sm:flex items-center gap-2 text-sm text-white/40">
            <span className="px-2 py-1 rounded-md bg-green-500/10 text-green-400 text-xs font-medium border border-green-500/20">
              System Online
            </span>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <button className="relative p-2 rounded-xl hover:bg-white/[0.06] text-white/60 hover:text-white transition-colors">
            <Bell className="w-5 h-5" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-magenta-500 rounded-full animate-pulse" style={{background: '#ff00a0'}} />
          </button>
          <div className="flex items-center gap-2 px-3 py-2 rounded-xl glass">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-magenta-500 to-orange-500 flex items-center justify-center" style={{background: 'linear-gradient(135deg, #ff00a0, #ff4d00)'}}>
              <User className="w-4 h-4 text-white" />
            </div>
            <span className="text-sm font-medium text-white/80 hidden sm:block">Seller Pro</span>
          </div>
        </div>
      </div>
    </header>
  );
}

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#0a0a0f] text-white">
        <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
        
        <div className="lg:pl-72">
          <TopBar onMenuClick={() => setSidebarOpen(true)} />
          
          <main className="p-4 lg:p-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analyze" element={<Analyze />} />
              <Route path="/product/:id" element={<ProductDetail />} />
              <Route path="/watchlist" element={<Watchlist />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
