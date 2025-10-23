 import React from "react"
 import Navbar from "./components/Navbar/Navbar"
 import Hero from "./components/Hero/Hero"
 import Cards from "./components/Cards/Cards"
 import Footer from "./components/Footer/Footer"

 const App = () => {
  return(
    <div>
      <Navbar/>
      <Hero/>
      <Footer/>
      <Cards/>
    </div>
  )
 }

export default App