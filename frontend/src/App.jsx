import { useState } from 'react'
import './App.css'
import Home from './pages/Home'
import Generate from './pages/Generate'
import About from './pages/About'
import Contact from './pages/Contact'
import {BrowserRouter,Routes, Route} from "react-router-dom"
import Navbar from './Navigation/Navbar'

function App() {

  return (
    <>
      <BrowserRouter>
        <div className='min-h-screen bg-black text-white'>
          <Navbar/>
          <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="/generate" element={<Generate/>}/>
            <Route path="/about" element={<About/>}/>
            <Route path="/contact" element={<Contact/>}/>
          </Routes>
        </div>
      </BrowserRouter>
    </>
  )
}

export default App

