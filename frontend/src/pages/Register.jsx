import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { registerUser } from '../utils/api'

function Register() {
  const navigate = useNavigate()
  const [form, setForm]       = useState({ name: '', email: '', password: '' })
  const [error, setError]     = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const handle = e => setForm({ ...form, [e.target.name]: e.target.value })

  const submit = async () => {
    setError('')
    setLoading(true)
    try {
      await registerUser(form)
      setSuccess('Account created! Redirecting to login...')
      setTimeout(() => navigate('/login'), 1500)
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed. Try again.')
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
          <h1 style={{fontSize:24,fontWeight:700,color:'#f1f5f9'}}>Create Account</h1>
          <p style={{fontSize:13,color:'#475569',marginTop:6}}>Join DataForge for free</p>
        </div>

        <div className='card'>
          <div style={{marginBottom:16}}>
            <label style={{fontSize:12,color:'#64748b'}}>Full Name</label>
            <input className='input-field' type='text' name='name'
              placeholder='Your full name'
              value={form.name} onChange={handle} />
          </div>
          <div style={{marginBottom:16}}>
            <label style={{fontSize:12,color:'#64748b'}}>Email</label>
            <input className='input-field' type='email' name='email'
              placeholder='you@example.com'
              value={form.email} onChange={handle} />
          </div>
          <div style={{marginBottom:8}}>
            <label style={{fontSize:12,color:'#64748b'}}>Password</label>
            <input className='input-field' type='password' name='password'
              placeholder='Create a password'
              value={form.password} onChange={handle} />
          </div>
          {error   && <div className='error-msg'>{error}</div>}
          {success && <div style={{background:'#052e16',border:'1px solid #14532d',
            color:'#4ade80',padding:'10px 14px',borderRadius:8,fontSize:13,marginTop:10}}>
            {success}</div>}
          <button className='btn-primary' onClick={submit} disabled={loading}>
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
          <p style={{textAlign:'center',fontSize:13,color:'#475569',marginTop:16}}>
            Already have an account?{' '}
            <Link to='/login' style={{color:'#60a5fa'}}>Login here</Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Register
