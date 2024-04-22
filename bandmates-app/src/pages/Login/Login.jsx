import React from 'react'

const Login = () => {
    return (
        <div className="w-screen h-screen bg-blue-100 flex items-center justify-center">
            <div className="w-[75%] h-[70%] flex">
                <div className="flex flex-col justify-center" style={{flex:1}}>
                    <h1 className="font-extrabold text-3xl text-blue-700">BandMates</h1>
                    <span className="text-lg font-semibold">Where music finds its match. Groove now with BandMates!</span>
                </div>
                <div className="flex flex-col justify-center" style={{flex:1}}>
                    <div className="bg-white h-[300px] p-[20px] rounded-md flex flex-col justify-between shadow-lg">
                        <input type="username" placeholder="username" className="h-[50px] rounded-md border border-gray-200 text-lg p-[20px] focus:outline-none"/>
                        <input type="password" placeholder="password" className="h-[50px] rounded-md border border-gray-200 text-lg p-[20px] focus:outline-none"/>
                        <button className="h-[50px] rounded-lg bg-blue-700 hover:bg-blue-800 transition text-white text-lg font-bold">Log In</button>
                        <span className="text-center text-blue-700 cursor-pointer"> Forgot password?</span>
                        <button className="h-[50px] rounded-lg bg-green-600 hover:bg-green-700 transition text-white text-lg font-bold">New here? Create a new account</button>
                    </div>
    
                </div>
            </div>
        </div>
      )
}

export default Login