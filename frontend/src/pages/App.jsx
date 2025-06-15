import { Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './Dashboard'
import Products from './Products'
import Customers from './Customers'
import UtangLedger from './UtangLedger'
import Login from './Login'
import Signup from './Signup'
import Sidebar from '../components/Sidebar'

export default function App() {
  const token = localStorage.getItem('token')

  if (!token) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1 p-4">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/products" element={<Products />} />
          <Route path="/customers" element={<Customers />} />
          <Route path="/utang" element={<UtangLedger />} />
        </Routes>
      </div>
    </div>
  )
}
