import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Manifesto from './components/Manifesto'
import Services from './components/Services'
import About from './components/About'
import Work from './components/Work'
import Testimonials from './components/Testimonials'
import Contact from './components/Contact'
import Footer from './components/Footer'

export default function App() {
  return (
    <>
      <Navbar />
      <main id="main">
        <Hero />
        <Manifesto />
        <Services />
        <About />
        <Work />
        <Testimonials />
        <Contact />
      </main>
      <Footer />
    </>
  )
}
