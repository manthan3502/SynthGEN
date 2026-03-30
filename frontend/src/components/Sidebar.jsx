import { useNavigate, useLocation } from 'react-router-dom'

const navItems = [
  { path: '/generate', label: 'Generate',  icon: '✦' },
  { path: '/history',  label: 'History',   icon: '◷' },
  { path: '/settings', label: 'Settings',  icon: '◎' },
]

function Sidebar() {
  const navigate  = useNavigate()
  const location  = useLocation()
  const name      = localStorage.getItem('name') || 'User'

  const logout = () => {
    localStorage.clear()
    navigate('/login')
  }

  return (
    <div className='sidebar'>
      <div style={{padding:'20px 16px',borderBottom:'1px solid #1e2d3d'}}>
        <div style={{display:'flex',alignItems:'center',gap:10}}>
          <div style={{width:34,height:34,background:'#2563eb',borderRadius:8,
            display:'flex',alignItems:'center',justifyContent:'center',fontSize:16}}>
            ⚡
          </div>
          <div>
            <div style={{fontSize:15,fontWeight:700,color:'#f1f5f9'}}>DataForge</div>
            <div style={{fontSize:10,color:'#475569'}}>Synthetic Data Generator</div>
          </div>
        </div>
      </div>

      <div style={{padding:'10px',flex:1}}>
        <div style={{fontSize:10,fontWeight:600,color:'#334155',
          textTransform:'uppercase',letterSpacing:'.07em',padding:'12px 8px 6px'}}>
          Menu
        </div>
        {navItems.map(item => (
          <div key={item.path}
            onClick={() => navigate(item.path)}
            style={{
              display:'flex',alignItems:'center',gap:9,padding:'9px 10px',
              borderRadius:8,cursor:'pointer',fontSize:13,marginBottom:2,
              background: location.pathname===item.path ? '#162040' : 'transparent',
              color: location.pathname===item.path ? '#60a5fa' : '#64748b',
            }}>
            <span style={{fontSize:14,width:18,textAlign:'center'}}>{item.icon}</span>
            {item.label}
          </div>
        ))}
      </div>

      <div style={{padding:'12px 14px',borderTop:'1px solid #1e2d3d'}}>
        <div style={{display:'flex',alignItems:'center',gap:8,
          padding:'8px 10px',borderRadius:8,background:'#111827',marginBottom:8}}>
          <div style={{width:28,height:28,borderRadius:'50%',background:'#2563eb',
            display:'flex',alignItems:'center',justifyContent:'center',
            fontSize:12,fontWeight:700,color:'#fff',flexShrink:0}}>
            {name.charAt(0).toUpperCase()}
          </div>
          <div>
            <div style={{fontSize:12,fontWeight:500,color:'#94a3b8'}}>{name}</div>
            <div style={{fontSize:10,color:'#334155'}}>Free Plan</div>
          </div>
        </div>
        <button onClick={logout}
          style={{width:'100%',background:'transparent',border:'1px solid #1e2d3d',
            color:'#64748b',padding:'7px',borderRadius:7,fontSize:12,cursor:'pointer'}}>
          Logout
        </button>
      </div>
    </div>
  )
}

export default Sidebar
