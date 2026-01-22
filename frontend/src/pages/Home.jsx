import React from 'react'
import { Link } from 'react-router-dom'
const Home = () => {
  return (
   <div className="flex justify-center items-center min-h-[90vh] px-4 text-center text-white">
  <div className="max-w-3xl ">
    <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
      Get your portfolio website <span className="underline decoration-blue-500"> in 60 seconds</span>
    </h1>
    
    {/* Subheading */}
    <p className="text-lg md:text-xl text-gray-300 mb-12">
      Instantly transform your resume into a stunning professional site. 
      Perfect for students and professionals.
    </p>

    {/* Simple Steps */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-sm md:text-base">
      <div className="space-y-2">
        <div className="text-blue-400 font-bold text-xl">01</div>
        <h4 className="font-semibold text-lg">Upload</h4>
        <p className="text-gray-400">Drop your resume PDF.</p>
      </div>
      
      <div className="space-y-2">
        <div className="text-blue-400 font-bold text-xl">02</div>
        <h4 className="font-semibold text-lg">AI Sync</h4>
        <p className="text-gray-400">We extract your skills.</p>
      </div>

      <div className="space-y-2">
        <div className="text-blue-400 font-bold text-xl">03</div>
        <h4 className="font-semibold text-lg">Go Live</h4>
        <p className="text-gray-400">Share your new link.</p>
      </div>
    </div> 
    <Link to="/generate" className='mt-10 inline-block bg-white text-black px-8 py-3 rounded-full font-bold text-lg hover:bg-blue-500 hover:text-white transition-colors duration-300'> Get Started Now!
      </Link>
     
  </div>
  
  
</div>
   


  )
}

export default Home



  
