import { useEffect, useState } from 'react'
import api from '../utils/api'

export default function Customers() {
  const [customers, setCustomers] = useState([])
  const [form, setForm] = useState({ name: '', contact: '' })

  useEffect(() => {
    fetchCustomers()
  }, [])

  const fetchCustomers = async () => {
    const res = await api.get('/api/customers/')
    setCustomers(res.data)
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    await api.post('/api/customers/', form)
    setForm({ name: '', contact: '' })
    fetchCustomers()
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Customers</h1>

      <form className="mb-4 space-x-2" onSubmit={handleSubmit}>
        <input name="name" value={form.name} onChange={handleChange} placeholder="Name" className="border p-2" />
        <input name="contact" value={form.contact} onChange={handleChange} placeholder="Contact" className="border p-2" />
        <button className="bg-blue-500 text-white px-4 py-2">Add</button>
      </form>

      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="border p-2 text-left">Name</th>
            <th className="border p-2 text-left">Contact</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((c) => (
            <tr key={c.id}>
              <td className="border p-2">{c.name}</td>
              <td className="border p-2">{c.contact}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
