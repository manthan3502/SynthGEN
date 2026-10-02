import { useNavigate } from 'react-router-dom'

function Landing() {
  const navigate = useNavigate()

  return (
    <div style={{minHeight:'100vh',background:'#07090f',display:'flex',
      flexDirection:'column',alignItems:'center',justifyContent:'center',padding:24}}>

      <div style={{textAlign:'center',maxWidth:620}}>
        <div style={{width:64,height:64,background:'#2563eb',borderRadius:14,
          display:'flex',alignItems:'center',justifyContent:'center',
          fontSize:28,margin:'0 auto 24px'}}>
          ⚡
        </div>
        <h1 style={{fontSize:48,fontWeight:800,color:'#f1f5f9',marginBottom:12}}>
          SynthGEN
        </h1>
        <h2 style={{fontSize:22,fontWeight:500,color:'#60a5fa',marginBottom:16}}>
          Synthetic Data Generator
        </h2>
        <p style={{fontSize:16,color:'#64748b',marginBottom:40,lineHeight:1.7}}>
          Can't find the dataset you need on Kaggle?<br/>
          Describe it in plain English — Gemini proposes a schema; Faker generates the records.
        </p>

        <div style={{display:'flex',gap:12,justifyContent:'center',marginBottom:48}}>
          <button onClick={() => navigate('/register')}
            style={{background:'#2563eb',color:'#fff',border:'none',
              padding:'12px 28px',borderRadius:9,fontSize:15,fontWeight:600,cursor:'pointer'}}>
            Get Started
          </button>
          <button onClick={() => navigate('/login')}
            style={{background:'transparent',color:'#60a5fa',
              border:'1px solid #1e3a5f',
              padding:'12px 28px',borderRadius:9,fontSize:15,cursor:'pointer'}}>
            Login
          </button>
        </div>

        <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:16}}>
          {[
            {icon:'🤖',title:'AI Powered',desc:'Gemini proposes columns from your description'},
            {icon:'📊',title:'Tabular Data',desc:'Generate example records for testing and exploration'},
            {icon:'💰',title:'CSV Export',desc:'Download generated records as a CSV file'},
          ].map((f,i) => (
            <div key={i} style={{background:'#0d1117',border:'1px solid #1e2d3d',
              borderRadius:12,padding:'20px 16px',textAlign:'center'}}>
              <div style={{fontSize:28,marginBottom:10}}>{f.icon}</div>
              <div style={{fontSize:14,fontWeight:600,color:'#f1f5f9',marginBottom:6}}>{f.title}</div>
              <div style={{fontSize:12,color:'#475569',lineHeight:1.6}}>{f.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Landing
