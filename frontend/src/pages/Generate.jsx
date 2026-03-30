import { useState } from 'react'
import { generateDataset, downloadCSV } from '../utils/api'
import Sidebar from '../components/Sidebar'

const EXAMPLES = [
  'Generate AQI data for Indian cities with PM2.5, PM10, CO2 and air quality level',
  'Generate hospital patient data with name, age, blood group, diagnosis and doctor',
  'Generate IPL player auction data with player name, team, role, bid amount',
  'Generate e-commerce orders with product, price, customer, status and date',
  'Generate student exam results with name, subject, marks, grade and result',
  'Generate bank transactions with account number, amount, type and merchant',
  'Generate farmer crop data with crop type, yield, rainfall and soil quality',
  'Generate stock market data for NSE with symbol, open, close, high and volume',
]
const TYPE_COLORS = {
  name:'#1e1b4b', integer:'#14532d', float:'#431407',
  date:'#422006', email:'#0c4a6e', phone:'#134e4a',
  city:'#1e3a5f', choice:'#3b0764', boolean:'#3f0f0f',
  text:'#1c1917', uuid:'#1a2e05', company:'#0f172a',
}
const TYPE_TEXT = {
  name:'#a5b4fc', integer:'#86efac', float:'#fdba74',
  date:'#fcd34d', email:'#7dd3fc', phone:'#5eead4',
  city:'#93c5fd', choice:'#d8b4fe', boolean:'#fca5a5',
  text:'#d6d3d1', uuid:'#a3e635', company:'#94a3b8',
}

function Generate() {
  const [prompt,   setPrompt]   = useState('')
  const [rows,     setRows]     = useState(100)
  const [loading,  setLoading]  = useState(false)
  const [preview,  setPreview]  = useState(null)
  const [schema,   setSchema]   = useState([])
  const [error,    setError]    = useState('')
  const [totalGen, setTotalGen] = useState(0)
  const [curPrompt,setCurPrompt]= useState('')
  const [curRows,  setCurRows]  = useState(100)

  const generate = async () => {
    if (!prompt.trim()) return
    setError('')
    setLoading(true)
    setPreview(null)
    setCurPrompt(prompt)
    setCurRows(rows)
    try {
      const res = await generateDataset(prompt, rows)
      setPreview(res.data)
      setSchema(res.data.schema || [])
      setTotalGen(t => t + 1)
    } catch (err) {
      setError(err.response?.data?.error || 'Generation failed. Try again.')
    } finally {
      setLoading(false)
    }
  }

  const download = async () => {
    try {
      const res = await downloadCSV(curPrompt, curRows)
      const url = URL.createObjectURL(new Blob([res.data]))
      const a   = document.createElement('a')
      a.href    = url
      a.download = `dataset_${curRows}rows.csv`
      a.click()
    } catch {
      setError('Download failed. Try again.')
    }
  }

  return (
    <div className='app-layout'>
      <Sidebar />
      <div className='main-content'>

        <div style={{marginBottom:24}}>
          <div className='page-title'>Generate Dataset</div>
          <div className='page-sub'>Describe any dataset in plain English — Gemini AI understands it</div>
        </div>

        <div style={{display:'grid',gridTemplateColumns:'1fr 300px',gap:16}}>
          <div>
            <div className='card'>
              <div style={{display:'inline-flex',alignItems:'center',gap:6,
                background:'#1a1033',border:'1px solid #6d28d9',borderRadius:12,
                padding:'3px 12px',fontSize:11,color:'#a855f7',marginBottom:12}}>
                <span style={{width:6,height:6,borderRadius:'50%',background:'#a855f7',display:'inline-block'}}></span>
                Powered by Gemini AI
              </div>
              <div className='label'>What dataset do you need?</div>
              <textarea className='input-field'
                rows={4}
                placeholder='e.g. Generate AQI data for 10 Indian cities with PM2.5, PM10, CO2 levels and air quality index'
                value={prompt}
                onChange={e => setPrompt(e.target.value)}
                style={{resize:'none'}}
              />
              <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:10,marginTop:12}}>
                <div>
                  <label style={{fontSize:11,color:'#475569',display:'block',marginBottom:4}}>Number of rows</label>
                  <input className='input-field' type='number'
                    value={rows} min={10} max={5000}
                    onChange={e => setRows(parseInt(e.target.value)||100)}
                    style={{marginTop:0}}
                  />
                </div>
                <div>
                  <label style={{fontSize:11,color:'#475569',display:'block',marginBottom:4}}>Format</label>
                  <select className='input-field' style={{marginTop:0}}>
                    <option>CSV</option>
                  </select>
                </div>
              </div>

              <button className='btn-primary' onClick={generate} disabled={loading}>
                {loading ? 'Gemini is thinking...' : '✦ Generate with Gemini'}
              </button>

              <div style={{fontSize:11,color:'#334155',marginTop:12,marginBottom:6}}>Try an example:</div>
              <div style={{display:'flex',flexWrap:'wrap',gap:6}}>
                {EXAMPLES.map((ex,i) => (
                  <span key={i}
                    onClick={() => setPrompt(ex)}
                    style={{background:'#111827',border:'1px solid #1e2d3d',
                      color:'#64748b',fontSize:11,padding:'4px 10px',
                      borderRadius:14,cursor:'pointer'}}>
                    {ex.split(' ').slice(1,4).join(' ')}...
                  </span>
                ))}
              </div>
            </div>

            {error && <div className='error-msg' style={{marginTop:12}}>{error}</div>}

            {loading && (
              <div style={{textAlign:'center',padding:'32px',color:'#475569',fontSize:13}}>
                Sending prompt to Gemini AI...
              </div>
            )}

            {preview && !loading && (
              <div style={{marginTop:16}}>
                <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:10}}>
                  <div style={{fontSize:12,fontWeight:600,color:'#94a3b8'}}>
                    Preview — first 20 of {preview.rows} rows
                  </div>
                  <button onClick={download}
                    style={{background:'#111827',border:'1px solid #1e2d3d',
                      color:'#60a5fa',fontSize:12,padding:'6px 14px',
                      borderRadius:7,cursor:'pointer',fontWeight:500}}>
                    ↓ Download CSV
                  </button>
                </div>
                <div style={{overflowX:'auto',border:'1px solid #1e2d3d',borderRadius:9}}>
                  <table style={{width:'100%',borderCollapse:'collapse',fontSize:11}}>
                    <thead>
                      <tr style={{background:'#111827'}}>
                        {preview.columns.map((col,i) => (
                          <th key={i} style={{padding:'9px 13px',textAlign:'left',
                            color:'#475569',fontWeight:500,borderBottom:'1px solid #1e2d3d',
                            whiteSpace:'nowrap',fontFamily:'monospace'}}>
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {preview.data.map((row,i) => (
                        <tr key={i} style={{borderBottom:'1px solid #0d1117'}}>
                          {row.map((cell,j) => (
                            <td key={j} style={{padding:'8px 13px',color:'#94a3b8',
                              fontFamily:'monospace',whiteSpace:'nowrap'}}>
                              {String(cell)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div style={{fontSize:11,color:'#334155',textAlign:'right',marginTop:6}}>
                  {preview.rows} rows x {preview.columns.length} columns generated
                </div>
              </div>
            )}
          </div>

          <div style={{display:'flex',flexDirection:'column',gap:14}}>
            <div className='card'>
              <div className='label'>Stats</div>
              <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:9}}>
                {[
                  {val:preview?.rows||'—',lbl:'Rows',color:'#60a5fa'},
                  {val:preview?.columns?.length||'—',lbl:'Columns',color:'#4ade80'},
                  {val:totalGen,lbl:'Today',color:'#f472b6'},
                  {val:'Rs.0',lbl:'Cost',color:'#fb923c'},
                ].map((s,i) => (
                  <div key={i} style={{background:'#111827',borderRadius:9,
                    padding:'13px 14px',border:'1px solid #1e2d3d'}}>
                    <div style={{fontSize:22,fontWeight:700,color:s.color,
                      fontFamily:'monospace'}}>{s.val}</div>
                    <div style={{fontSize:10,color:'#334155',marginTop:3}}>{s.lbl}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className='card'>
              <div className='label'>Schema detected by Gemini</div>
              {schema.length === 0 ? (
                <div style={{fontSize:12,color:'#334155',padding:'10px 0',textAlign:'center'}}>
                  Schema appears after generation
                </div>
              ) : (
                <div style={{display:'flex',flexDirection:'column',gap:5}}>
                  {schema.map((col,i) => (
                    <div key={i} style={{display:'flex',alignItems:'center',
                      justifyContent:'space-between',padding:'7px 10px',
                      background:'#111827',borderRadius:7,border:'1px solid #1e2d3d'}}>
                      <span style={{fontSize:11,fontWeight:500,color:'#e2e8f0',
                        fontFamily:'monospace'}}>{col.name}</span>
                      <span style={{fontSize:10,padding:'2px 8px',borderRadius:10,
                        background:TYPE_COLORS[col.type]||'#1c1917',
                        color:TYPE_TEXT[col.type]||'#d6d3d1'}}>{col.type}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Generate
