import React from 'react'

const About = () => {
  return (
    <div className="max-w-2xl mx-auto py-16 px-4 text-center text-white">
  {/* Small Tagline */}
  <span className="text-blue-500 font-semibold tracking-widest uppercase text-sm">Made for Students</span>
  
  <h2 className="text-3xl md:text-4xl font-bold mt-4 mb-6">Stop sending just a PDF.</h2>
  
  <p className="text-lg text-gray-400 leading-relaxed">
    In 2026, a static resume isn't enough. We help students turn their class projects, 
    internships, and skills into a <span className="text-white font-medium">live link</span> that recruiters actually want to click.
  </p>

  {/* Student-Focused Benefits */}
  <div className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-6">
    <div className="text-left space-y-2">
      <h4 className="text-blue-400 font-bold">🚀 Zero Tech Skills</h4>
      <p className="text-sm text-gray-400">No coding or design experience needed. If you have a resume, you have a website.</p>
    </div>
    
    <div className="text-left space-y-2">
      <h4 className="text-blue-400 font-bold">🎓 Perfect for Internships</h4>
      <p className="text-sm text-gray-400">Stand out from other applicants by sharing a professional link on LinkedIn.</p>
    </div>
  </div>
</div>

  )
}

export default About
