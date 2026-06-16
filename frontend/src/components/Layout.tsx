import { Outlet, Link, useLocation } from 'react-router-dom'
import { Phone, Users, Calendar, Settings, BarChart3, LogOut } from 'lucide-react'

export default function Layout() {
  const location = useLocation()
  const nav = [
    { path: '/', icon: BarChart3, label: 'Dashboard' },
    { path: '/calls', icon: Phone, label: 'Calls' },
    { path: '/customers', icon: Users, label: 'Customers' },
    { path: '/appointments', icon: Calendar, label: 'Appointments' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ]

  return (
    <div className="flex h-screen">
      <aside className="w-64 bg-slate-900 border-r border-slate-800">
        <div className="p-6">
          <h1 className="text-xl font-bold text-white">AI Receptionist</h1>
          <p className="text-xs text-slate-400 mt-1">Enterprise v2.0</p>
        </div>
        <nav className="px-4 space-y-1">
          {nav.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                location.pathname === item.path
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <item.icon size={18} />
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="absolute bottom-0 w-64 p-4 border-t border-slate-800">
          <button className="flex items-center gap-3 text-slate-400 hover:text-white text-sm">
            <LogOut size={18} />
            Sign Out
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-auto p-8">
        <Outlet />
      </main>
    </div>
  )
}
