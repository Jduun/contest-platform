import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { LoginForm } from './pages/LoginForm'
import { SignUpForm } from './pages/SignUpForm'
import { ProblemList } from './pages/ProblemList'
import { ProblemPage } from './pages/ProblemPage'
import { ThemeProvider } from '@/components/ui/theme-provider'
import { ContestList } from './pages/ContestList'
import { ContestPage } from './pages/ContestPage'
import { Toaster } from '@/components/ui/sonner'

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="App">
        <Router>
          <Routes>
            <Route path="/" element={<ProblemList />} />
            <Route path="/login" element={<LoginForm />} />
            <Route path="/signup" element={<SignUpForm />} />
            <Route path="/problems/:id" element={<ProblemPage />} />
            <Route path="/contests" element={<ContestList />} />
            <Route path="/contests/:id" element={<ContestPage />} />
          </Routes>
        </Router>
        <Toaster />
      </div>
    </ThemeProvider>
  )
}

export default App
