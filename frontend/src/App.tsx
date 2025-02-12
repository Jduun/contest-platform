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
import { UserProfile } from './pages/UserProfile'

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="App">
        <Router>
          <Routes>
            <Route path="/" element={<ProblemList />} />
            <Route path="/login" element={<LoginForm />} />
            <Route path="/signup" element={<SignUpForm />} />
            <Route path="/problems/:problem_id" element={<ProblemPage />} />
            <Route path="/contests" element={<ContestList />} />
            <Route path="/contests/:id" element={<ContestPage />} />
            <Route path="/contests" element={<ContestList />} />
            <Route path="/users/:username" element={<UserProfile />} />
            <Route
              path="/contests/:contest_id/problems/:problem_id"
              element={<ProblemPage />}
            />
          </Routes>
        </Router>
        <Toaster />
      </div>
    </ThemeProvider>
  )
}

export default App
