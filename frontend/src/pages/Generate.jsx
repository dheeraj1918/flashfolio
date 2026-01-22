import React from 'react'
import { useState,useRef , useEffect} from 'react'


const styleOptions=[
    "Classic",
    "Complex UI",
    "Hacker UI",
    "Windows 95",
    "Mac OS",
    "VS Code",
    "Terminal",
    "Cyberpunk UI"
]

const Generate = () => {
    const [selectedFile,setSelectedFile]=useState(null)
    const [isDragging,setIsDragging]=useState(false)
    const [error,setError]=useState("")
    const inputref=useRef(null)
    const [selectedStyle,setSelectedStyle]=useState(null)
    const [link,setLink]=useState("")
    const [loading,setLoading]=useState(false)
    const handleFile=(file)=>{
        if (!file) return
        if(file.type!=="application/pdf"){
            selectedFile(null)
            setError("Only PDF files are allowed.")
            return
        }
        setError("")
        setSelectedFile(file)
        
    }
    const handleInputChange=(e)=>{
        handleFile(e.target.files[0])
    }
    const handleDragOver=(e)=>{
        e.preventDefault()
        setIsDragging(true)
    }
    const handleDragLeave = () => {
    setIsDragging(false);
    };
    const handleDrop=(e)=>{
        e.preventDefault()
        setIsDragging(false)
        handleFile(e.dataTransfer.files[0])
    }
    function uploadFile(selectedFile,selectedStyle){
        const formData =new FormData()
        formData.append("pdf",selectedFile)
        formData.append("style",selectedStyle)
        fetch("http://127.0.0.1:8080/upload",{
            method:"POST",
            body:formData
        }).then(res=>res.json())
        .then(data=>{
          console.log(data)
          setLink(data.link)
          setLoading(false)
        })
        .catch(error=>{
          console.log(error)
          setLoading(false)
        })
    }
    
    return(
        <div className='flex flex-col items-center justify-center min-h-screen h-[10vh] '>
            <div className='text-2xl font-bold mb-6'>
                Try Once - Ready in 60s
            </div>
            {!selectedFile && (
                <div onClick={
                ()=>inputref.current.click()
            } onDragOver={handleDragOver} onDragLeave={handleDragLeave} onDrop={handleDrop}  className={`w-96 h-48 border-2 border-dashed rounded-xl flex flex-col items-center justify-center cursor-pointer transition
          ${
            isDragging
              ? "border-blue-500 bg-blue-50"
              : error
              ? "border-red-500 bg-red-50"
              : "border-gray-400 bg-white"
          }`}>
            <p className="text-gray-600 text-center px-4">
          Drag & drop your <strong>PDF</strong> here <br />
          or <span className="text-blue-500 font-semibold">click to browse</span>
        </p>
        <input
          ref={inputref}
          type="file"
          accept="application/pdf"
          className="hidden"
        
          onChange={handleInputChange}
        />
      </div>
            )}

      {/* Error Message */}
      {error && (
        <p className="mt-3 text-sm text-red-600 bg-red-100 px-4 py-2 rounded-lg">
          ❌ {error}
        </p>
      )}
      {selectedFile && !selectedStyle &&(
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 flex-row">
            {styleOptions.map((style)=>(
                <div key={style} onClick={()=>{
                    setSelectedStyle(style)
                    uploadFile(selectedFile,style)
                }} className={`cursor-pointer rounded-lg p-6 flex-row  transaction ${
                    selectedStyle===style? "border-2 border-blue-500 bg-blue-900"
                      : "border-b-2 border-gray-600 hover:border-blue-500 hover:bg-gray-800"
                }`}>
                    {style}
                </div>
            ))}
        </div>
      )}
      {selectedFile && selectedStyle &&(
        <div className="mt-6 w-full max-w-4xl bg-gray-900 px-7 py-7 rounded-lg shadow text-center">
          <h2 className="text-2xl font-bold mb-2">You selected: <strong className="text-xl text-blue-400">{selectedStyle}</strong></h2>
          <p className="text-sm text-blue-400">
            📄 <strong>{selectedFile.name}</strong>
          </p>
          <p className="text-xs text-blue-400">
            {(selectedFile.size / 1024).toFixed(2)} KB
          </p>
          {link?(
            <div >
              <p className='bg-orange-100 border-l-4 border-orange-500  p-4 text-black '>Link: {" "}  <span className='text-blue-900 hover:text-red-400'><a href={link} target="_blank" rel="noopener noreferrer">{link}</a></span></p> <br />
              <div class="bg-orange-100 border-l-4 border-orange-500 text-orange-700 p-2" role="alert">
                <p class="font-bold ">Be Warned</p>
                <p>Activation of the link may take up to 10–30 seconds.</p>
              </div>
            </div>
            
            
          ):(<p>Loading... <span>this process may take 40-60 seconds.</span></p>)}
        </div>
      )}
        </div>
    )


}

export default Generate
