import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import Calls from './pages/Calls'
import Customers from './pages/Customers'
import Appointments from './pages/Appointments'
import Settings from './pages/Settings'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="calls" element={<Calls />} />
        <Route path="customers" element={<Customers />} />
        <Route path="appointments" element={<Appointments />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  )
}

export default App
