import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../utils/api'

export default function Signup() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/api/auth/register/', form)
      navigate('/login')
    } catch (err) {
      setError('Unable to sign up')
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen">
      <form className="p-6 bg-white rounded shadow" onSubmit={handleSubmit}>
        <h1 className="text-xl font-bold mb-4">Sign Up</h1>
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
        <button className="bg-blue-500 text-white px-4 py-2 w-full">Sign Up</button>
        <p className="mt-2 text-center text-sm">
          <Link to="/login" className="text-blue-500">Back to login</Link>
        </p>
      </form>
    </div>
  )
}
