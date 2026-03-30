import { useState, useEffect } from 'react'
import { getSettings, updateSettings } from '../utils/api'
import Sidebar from '../components/Sidebar'

function Settings() {
  const [form,    setForm]    = useState({ name: '', email: '' })
  const [success, setSuccess] = useState('')
  const [error,   setError]   = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    getSettings().then(res => setForm(res.data)).catch(() => {})
  }, [])

  const handle = e => setForm({ ...form, [e.target.name]: e.target.value })

  const save = async () => {
    setError('') ; setSuccess('')
    setLoading(true)
    try {
      await updateSettings(form)
      localStorage.setItem('name', form.name)
      setSuccess('Settings saved successfully!')
    } catch {
      setError('Failed to save. Try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='app-layout'>
      <Sidebar />
      <div className='main-content'>
        <div style={{marginBottom:24}}>
          <div className='page-title'>Settings</div>
          <div className='page-sub'>Manage your account</div>
        </div>

        <div style={{maxWidth:460}}>
          <div className='card' style={{marginBottom:14}}>
            <div className='label'>Account Details</div>
            <div style={{marginBottom:14}}>
              <label style={{fontSize:12,color:'#64748b'}}>Name</label>
              <input className='input-field' type='text' name='name'
                value={form.name} onChange={handle} />
            </div>
            <div style={{marginBottom:8}}>
              <label style={{fontSize:12,color:'#64748b'}}>Email</label>
              <input className='input-field' type='email' name='email'
                value={form.email} onChange={handle} />
            </div>
            {error   && <div className='error-msg'>{error}</div>}
            {success && <div style={{background:'#052e16',border:'1px solid #14532d',
              color:'#4ade80',padding:'10px 14px',borderRadius:8,fontSize:13,marginTop:10}}>
              {success}</div>}
            <button className='btn-primary' onClick={save} disabled={loading}>
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </div>

          <div className='card'>
            <div className='label'>Gemini API</div>
            <div style={{display:'flex',alignItems:'center',gap:8,fontSize:13,
              color:'#4ade80',background:'#05140d',border:'1px solid #14532d',
              borderRadius:8,padding:'10px 14px',marginTop:4}}>
              ✓ Gemini 1.5 Flash connected · Free tier · 1500 req/day
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings
