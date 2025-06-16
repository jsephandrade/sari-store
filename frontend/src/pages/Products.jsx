import { useEffect, useState } from 'react'
import api from '../utils/api'

export default function Products() {
  const [products, setProducts] = useState([])
  const [form, setForm] = useState({ name: '', sku: '', price: '', stock: '' })

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    const res = await api.get('/api/products/')
    setProducts(res.data)
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    await api.post('/api/products/', { ...form, price: parseFloat(form.price), stock: parseInt(form.stock || 0) })
    setForm({ name: '', sku: '', price: '', stock: '' })
    fetchProducts()
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Products</h1>

      <form className="mb-4 space-x-2" onSubmit={handleSubmit}>
        <input name="name" value={form.name} onChange={handleChange} placeholder="Name" className="border p-2" />
        <input name="sku" value={form.sku} onChange={handleChange} placeholder="SKU" className="border p-2" />
        <input name="price" value={form.price} onChange={handleChange} placeholder="Price" className="border p-2" />
        <input name="stock" value={form.stock} onChange={handleChange} placeholder="Stock" className="border p-2" />
        <button className="bg-blue-500 text-white px-4 py-2">Add</button>
      </form>

      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="border p-2 text-left">Name</th>
            <th className="border p-2 text-left">SKU</th>
            <th className="border p-2 text-right">Price</th>
            <th className="border p-2 text-right">Stock</th>
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td className="border p-2">{p.name}</td>
              <td className="border p-2">{p.sku}</td>
              <td className="border p-2 text-right">₱{p.price}</td>
              <td className="border p-2 text-right">{p.stock}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
