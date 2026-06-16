import { Outlet, Link } from 'react-router-dom'

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex gap-4">
          <Link to="/" className="font-bold text-blue-600">Dashboard</Link>
          <Link to="/calls">Calls</Link>
          <Link to="/customers">Customers</Link>
          <Link to="/appointments">Appointments</Link>
          <Link to="/settings">Settings</Link>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}
