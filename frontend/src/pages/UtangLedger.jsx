import { useEffect, useState } from 'react'
import api from '../utils/api'

export default function UtangLedger() {
  const [entries, setEntries] = useState([])
  const [payment, setPayment] = useState({ utang_entry: '', amount_paid: '' })

  const fetchEntries = async () => {
    const res = await api.get('/api/utang/?status=pending')
    setEntries(res.data)
  }

  useEffect(() => {
    fetchEntries()
  }, [])

  const handleChange = (e) => {
    setPayment({ ...payment, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    await api.post('/api/payments/', { ...payment, amount_paid: parseFloat(payment.amount_paid) })
    setPayment({ utang_entry: '', amount_paid: '' })
    fetchEntries()
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Utang Ledger</h1>

      <form className="mb-4 space-x-2" onSubmit={handleSubmit}>
        <select name="utang_entry" value={payment.utang_entry} onChange={handleChange} className="border p-2">
          <option value="">Select Entry</option>
          {entries.map((e) => (
            <option key={e.id} value={e.id}>
              {e.customer} - {e.product} ({e.quantity})
            </option>
          ))}
        </select>
        <input name="amount_paid" value={payment.amount_paid} onChange={handleChange} placeholder="Amount" className="border p-2" />
        <button className="bg-blue-500 text-white px-4 py-2">Record Payment</button>
      </form>

      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="border p-2 text-left">Customer</th>
            <th className="border p-2 text-left">Product</th>
            <th className="border p-2 text-right">Qty</th>
            <th className="border p-2 text-right">Total</th>
            <th className="border p-2 text-left">Due</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((e) => (
            <tr key={e.id}>
              <td className="border p-2">{e.customer_name}</td>
              <td className="border p-2">{e.product_name}</td>
              <td className="border p-2 text-right">{e.quantity}</td>
              <td className="border p-2 text-right">₱{e.total_amount}</td>
              <td className="border p-2">{e.due_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
