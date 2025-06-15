import { useEffect, useState } from 'react'
import axios from 'axios'

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
      <pre>{JSON.stringify(summary, null, 2)}</pre>
    </div>
  )
}
