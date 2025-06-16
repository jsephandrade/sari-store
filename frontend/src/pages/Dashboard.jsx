import { useEffect, useState } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const [summary, setSummary] = useState({})

  useEffect(() => {
    axios
      .get('/api/summary/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      })
      .then((res) => setSummary(res.data))
      .catch(() => {})
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 bg-white rounded shadow">
          <p className="text-gray-500">Total Sales</p>
          <p className="text-2xl font-bold">₱{summary.total_sales || 0}</p>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <p className="text-gray-500">Outstanding Balances</p>
          <p className="text-2xl font-bold">₱{summary.outstanding_balances || 0}</p>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <p className="text-gray-500">New Customers (30d)</p>
          <p className="text-2xl font-bold">{summary.new_customers || 0}</p>
        </div>
      </div>
      <div className="space-x-4">
        <Link to="/products" className="text-blue-500">
          Manage Products
        </Link>
        <Link to="/customers" className="text-blue-500">
          Manage Customers
        </Link>
        <Link to="/utang" className="text-blue-500">
          Utang Ledger
        </Link>
      </div>
    </div>
  )
}
