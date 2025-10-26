import React from "react"
import Navbar from "./components/Navbar/Navbar"
import Footer from "./components/Footer/Footer"
import Report from "./pages/Report.jsx"

const App = () => {
  return(
    <div>
      <Navbar/>
      <Report/>
      <Footer/>
    </div>
  )
}

export default App