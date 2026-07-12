import Sidebar from './Sidebar'
import Header from './Header'

function MainLayout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Header />
        <main className="page-content">{children}</main>
      </div>
    </div>
  )
}

export default MainLayout
