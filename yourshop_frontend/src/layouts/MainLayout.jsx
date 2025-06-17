import Footer from "../components/ui/Footer"
import Navbar from "../components/ui/Navbar"
const MainLayout = ({children}) => {
  return (
    <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="min-h-screen flex justify-center">{children}</main>
        <Footer />
    </div>
  )
}

export default MainLayout