import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { loginUser } from '../utils/api'

function Login() {
  const navigate = useNavigate()
  const [form, setForm]     = useState({ email: '', password: '' })
  const [error, setError]   = useState('')
  const [loading, setLoading] = useState(false)

  const handle = e => setForm({ ...form, [e.target.name]: e.target.value })

  const submit = async () => {
    setError('')
    setLoading(true)
    try {
      const res = await loginUser(form)
      localStorage.setItem('token', res.data.token)
      localStorage.setItem('name',  res.data.name)
      localStorage.setItem('email', res.data.email)
      navigate('/generate')
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{minHeight:'100vh',background:'#07090f',display:'flex',
      alignItems:'center',justifyContent:'center',padding:24}}>
      <div style={{width:'100%',maxWidth:400}}>
        <div style={{textAlign:'center',marginBottom:32}}>
          <div style={{fontSize:28,marginBottom:8}}>⚡</div>
          <h1 style={{fontSize:24,fontWeight:700,color:'#f1f5f9'}}>Welcome back</h1>
          <p style={{fontSize:13,color:'#475569',marginTop:6}}>Login to your DataForge account</p>
        </div>

        <div className='card'>
          <div style={{marginBottom:16}}>
            <label style={{fontSize:12,color:'#64748b'}}>Email</label>
            <input className='input-field' type='email' name='email'
              placeholder='you@example.com'
              value={form.email} onChange={handle} />
          </div>
          <div style={{marginBottom:8}}>
            <label style={{fontSize:12,color:'#64748b'}}>Password</label>
            <input className='input-field' type='password' name='password'
              placeholder='Enter your password'
              value={form.password} onChange={handle} />
          </div>
          {error && <div className='error-msg'>{error}</div>}
          <button className='btn-primary' onClick={submit} disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
          <p style={{textAlign:'center',fontSize:13,color:'#475569',marginTop:16}}>
            Don't have an account?{' '}
            <Link to='/register' style={{color:'#60a5fa'}}>Register here</Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login
