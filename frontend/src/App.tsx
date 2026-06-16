import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Calls from './pages/Calls'
import Customers from './pages/Customers'
import Appointments from './pages/Appointments'
import Login from './pages/Login'
import Settings from './pages/Settings'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/calls" element={<Calls />} />
          <Route path="/customers" element={<Customers />} />
          <Route path="/appointments" element={<Appointments />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
