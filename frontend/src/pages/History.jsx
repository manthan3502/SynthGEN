import { useState, useEffect } from 'react'
import { getHistory, deleteHistory } from '../utils/api'
import Sidebar from '../components/Sidebar'

function History() {
  const [items,   setItems]   = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchHistory() }, [])

  const fetchHistory = async () => {
    try {
      const res = await getHistory()
      setItems(res.data)
    } catch {
      setItems([])
    } finally {
      setLoading(false)
    }
  }

  const remove = async (id) => {
    try {
      await deleteHistory(id)
      setItems(items.filter(i => i.id !== id))
    } catch {}
  }

  return (
    <div className='app-layout'>
      <Sidebar />
      <div className='main-content'>
        <div style={{marginBottom:24}}>
          <div className='page-title'>Generation History</div>
          <div className='page-sub'>All your past datasets — re-download anytime</div>
        </div>

        <div className='card'>
          <div className='label'>Recent generations ({items.length})</div>
          {loading && <div style={{color:'#475569',fontSize:13,padding:20,textAlign:'center'}}>Loading...</div>}
          {!loading && items.length === 0 && (
            <div style={{color:'#334155',fontSize:13,padding:'32px 20px',textAlign:'center'}}>
              No generations yet. Go to Generate page to create your first dataset!
            </div>
          )}
          {items.map(item => (
            <div key={item.id}
              style={{display:'flex',alignItems:'center',gap:12,padding:'12px 14px',
                background:'#111827',border:'1px solid #1e2d3d',borderRadius:10,
                marginBottom:8}}>
              <div style={{width:34,height:34,background:'#1e3a5f',borderRadius:8,
                display:'flex',alignItems:'center',justifyContent:'center',
                fontSize:16,flexShrink:0}}>📊</div>
              <div style={{flex:1,minWidth:0}}>
                <div style={{fontSize:13,color:'#94a3b8',overflow:'hidden',
                  textOverflow:'ellipsis',whiteSpace:'nowrap'}}>
                  {item.prompt}
                </div>
                <div style={{fontSize:11,color:'#334155',marginTop:3}}>
                  {item.rows} rows · {item.columns} columns · {item.created_at}
                </div>
              </div>
              <button onClick={() => remove(item.id)}
                style={{background:'transparent',border:'1px solid #1e2d3d',
                  color:'#ef4444',fontSize:11,padding:'4px 10px',
                  borderRadius:6,cursor:'pointer',flexShrink:0}}>
                Delete
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default History
