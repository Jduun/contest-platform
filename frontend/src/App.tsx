import './App.css'
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import { LoginForm } from './pages/LoginForm'
import { SignUpForm } from './pages/SignUpForm'
import { ProblemSet } from './pages/ProblemSet'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<ProblemSet />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/signup" element={<SignUpForm />} />
      </Routes>
    </Router>
  );
}

export default App
