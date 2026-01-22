import React from 'react'

const Contact = () => {
  return (
    <div className="max-w-2xl mx-auto py-20 px-4 text-center text-white">
  {/* Small Heading */}
  <h2 className="text-3xl font-bold mb-4">Have questions?</h2>

  {/* Contact Card */}
  <div className="bg-white/5 border border-white/10 p-8 rounded-3xl backdrop-blur-sm">
    <p className="text-sm text-blue-400 font-semibold uppercase tracking-widest mb-2">Email us at</p>
    <a 
      href="mailto:1dheerajpabolu@gmail.com" 
      className="text-xl md:text-2xl font-medium hover:text-blue-500 transition-colors duration-300 break-all"
    >
      1dheerajpabolu@gmail.com
    </a>
    
    <div className="mt-8">
      <a 
        href="mailto:1dheerajpabolu@gmail.com"
        className="inline-flex items-center gap-2 bg-white text-black px-6 py-2 rounded-full font-bold hover:bg-blue-500 hover:text-white transition-all duration-300"
      >
        Send a Message
        <svg xmlns="http://www.w3.org" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </a>
    </div>
  </div>
</div>

  )
}

export default Contact
