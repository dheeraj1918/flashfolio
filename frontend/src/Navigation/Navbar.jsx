import { NavLink } from "react-router-dom"

const Navbar = () => {
  return (
    <div>
      
      <nav className="flex justify-between  px-10 py-4 bg-neutral-900 text-white">
      <div className="text-xl text-blue-400 border-b-2 border-white">
            FlashFolio
      </div>
        <div className="flex gap-8">
            <NavLink   to="/"
            className={({isActive})=>{
                return isActive?"text-blue-400 border-b-2 border-blue-400":"text-white"
            }}>Home</NavLink>
            <NavLink to="/generate" className={({isActive})=>{
                return isActive?"text-blue-400 border-b-2 border-blue-400":"text-white"
            }}>Generate</NavLink>
            <NavLink to="/about" className={({isActive})=>{
                return isActive?"text-blue-400 border-b-2 border-blue-400":"text-white"
            }}>About</NavLink>
            
            <NavLink to="/contact" className={({isActive})=>{
                return isActive?"text-blue-400 border-b-2 border-blue-400":"text-white"
            }}>Contact</NavLink>
        </div>
      </nav>
    </div>
  )
}

export default Navbar
