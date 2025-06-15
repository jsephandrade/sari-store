import { NavLink } from 'react-router-dom'

export default function Sidebar() {
  const linkClass = ({ isActive }) =>
    `block px-4 py-2 rounded hover:bg-gray-200 ${isActive ? 'bg-gray-200 font-bold' : ''}`

  return (
    <aside className="w-48 bg-white border-r min-h-screen p-4">
      <nav className="space-y-2">
        <NavLink to="/" className={linkClass} end>
          Dashboard
        </NavLink>
        <NavLink to="/products" className={linkClass}>
          Products
        </NavLink>
        <NavLink to="/customers" className={linkClass}>
          Customers
        </NavLink>
        <NavLink to="/utang" className={linkClass}>
          Utang Ledger
        </NavLink>
      </nav>
    </aside>
  )
}
