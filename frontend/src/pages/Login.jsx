import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../utils/api'

export default function Login() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await api.post('/api/auth/token/', form)
      localStorage.setItem('token', res.data.access)
      navigate('/')
    } catch (err) {
      setError('Invalid credentials')
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen">
      <form className="p-6 bg-white rounded shadow" onSubmit={handleSubmit}>
        <h1 className="text-xl font-bold mb-4">Login</h1>
        {error && <p className="text-red-500 mb-2">{error}</p>}
        <input
          name="username"
          onChange={handleChange}
          placeholder="Username"
          className="border p-2 w-full mb-2"
        />
        <input
          name="password"
          type="password"
          onChange={handleChange}
          placeholder="Password"
          className="border p-2 w-full mb-4"
        />
        <button className="bg-blue-500 text-white px-4 py-2 w-full">Login</button>
        <p className="mt-2 text-center text-sm">
          No account? <Link to="/signup" className="text-blue-500">Sign up</Link>
        </p>
      </form>
    </div>
  )
}
