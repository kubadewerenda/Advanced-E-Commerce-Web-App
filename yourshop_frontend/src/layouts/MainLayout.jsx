import Footer from "../components/ui/Footer"
import Navbar from "../components/ui/Navbar"

const MainLayout = ({children, numCartItems, totalValue}) => {
    return (
        <div className="min-h-screen flex flex-col">
            <Navbar numCartItems={numCartItems} totalValue={totalValue}/>
            <main className="min-h-screen flex justify-center">{children}</main>
            <Footer />
        </div>
    )
}

export default MainLayout