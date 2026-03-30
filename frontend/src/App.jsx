import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Landing  from './pages/Landing'
import Login    from './pages/Login'
import Register from './pages/Register'
import Generate from './pages/Generate'
import History  from './pages/History'
import Settings from './pages/Settings'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/'         element={<Landing />} />
        <Route path='/login'    element={<Login />} />
        <Route path='/register' element={<Register />} />
        <Route path='/generate' element={<ProtectedRoute><Generate /></ProtectedRoute>} />
        <Route path='/history'  element={<ProtectedRoute><History /></ProtectedRoute>} />
        <Route path='/settings' element={<ProtectedRoute><Settings /></ProtectedRoute>} />
        <Route path='*'         element={<Navigate to='/' />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
