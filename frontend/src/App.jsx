import { useState } from "react"
import ReactMarkdown from "react-markdown"

export default function App() {
  const [cv, setCv] = useState("")
  const [oferta, setOferta] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const analyze = async () => {
    if (!cv || !oferta) return
    setLoading(true)
    setResult(null)
    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cv_texto: cv, oferta_texto: oferta })
      })
      const data = await res.json()
      setResult(data)
    } catch (e) {
      console.error(e)
    }
    setLoading(false)
  }

  const downloadWord = async () => {
    const res = await fetch("http://127.0.0.1:8000/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cv_adaptado: result.cv_adaptado })
    })
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "cv_adaptado.docx"
    a.click()
    window.URL.revokeObjectURL(url)
  }

  return (
    <div style={{ minHeight: "100vh", background: "#ffffff", color: "#1a1a1a", fontFamily: "system-ui", padding: "40px 20px" }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        <h1 style={{ fontSize: 32, fontWeight: 300, marginBottom: 8, color: "#1a1a1a" }}>CV Match Agent</h1>
        <p style={{ color: "#6b6b8a", marginBottom: 40 }}>Analiza el fit entre tu CV y una oferta de trabajo</p>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 24 }}>
          <div>
            <label style={{ display: "block", fontSize: 12, color: "#6b6b8a", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.1em" }}>Tu CV</label>
            <textarea
              value={cv}
              onChange={e => setCv(e.target.value)}
              placeholder="Pega aquí tu CV..."
              style={{ width: "100%", height: 300, background: "#f8f8f8", border: "1px solid #e0e0e0", borderRadius: 8, padding: 16, color: "#1a1a1a", fontSize: 13, resize: "vertical", boxSizing: "border-box" }}
            />
          </div>
          <div>
            <label style={{ display: "block", fontSize: 12, color: "#6b6b8a", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.1em" }}>Oferta de trabajo</label>
            <textarea
              value={oferta}
              onChange={e => setOferta(e.target.value)}
              placeholder="Pega aquí la oferta..."
              style={{ width: "100%", height: 300, background: "#f8f8f8", border: "1px solid #e0e0e0", borderRadius: 8, padding: 16, color: "#1a1a1a", fontSize: 13, resize: "vertical", boxSizing: "border-box" }}
            />
          </div>
        </div>

        <button
          onClick={analyze}
          disabled={loading || !cv || !oferta}
          style={{ background: loading ? "#e0e0e0" : "#7c6af7", color: loading ? "#6b6b8a" : "#fff", border: "none", borderRadius: 8, padding: "12px 32px", fontSize: 14, cursor: loading ? "not-allowed" : "pointer", marginBottom: 40 }}
        >
          {loading ? "Analizando..." : "Analizar fit →"}
        </button>

        {result && (
          <div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 32 }}>
              <div style={{ background: "#f8f8f8", border: "1px solid #e0e0e0", borderRadius: 12, padding: 24 }}>
                <div style={{ fontSize: 12, color: "#6b6b8a", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.1em" }}>Fit Score</div>
                <div style={{ fontSize: 48, fontWeight: 300, color: result.fit_score >= 60 ? "#0f6e56" : result.fit_score >= 40 ? "#b85c00" : "#c0392b" }}>{result.fit_score}%</div>
              </div>
              <div style={{ background: "#f8f8f8", border: "1px solid #e0e0e0", borderRadius: 12, padding: 24 }}>
                <div style={{ fontSize: 12, color: "#6b6b8a", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.1em" }}>Skills match</div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {result.skills_match.map(s => (
                    <span key={s} style={{ background: "rgba(15,110,86,0.08)", border: "1px solid rgba(15,110,86,0.3)", color: "#0f6e56", borderRadius: 100, padding: "3px 10px", fontSize: 12 }}>{s}</span>
                  ))}
                </div>
              </div>
              <div style={{ background: "#f8f8f8", border: "1px solid #e0e0e0", borderRadius: 12, padding: 24 }}>
                <div style={{ fontSize: 12, color: "#6b6b8a", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.1em" }}>Skills gap</div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {result.skills_gap.map(s => (
                    <span key={s} style={{ background: "rgba(192,57,43,0.08)", border: "1px solid rgba(192,57,43,0.3)", color: "#c0392b", borderRadius: 100, padding: "3px 10px", fontSize: 12 }}>{s}</span>
                  ))}
                </div>
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <div style={{ background: "#f8f8f8", border: "1px solid #e0e0e0", borderRadius: 12, padding: 24 }}>
                <div style={{ fontSize: 12, color: "#6b6b8a", marginBottom: 16, textTransform: "uppercase", letterSpacing: "0.1em" }}>Recomendaciones</div>
                <div style={{ fontSize: 13, lineHeight: 1.7, color: "#1a1a1a", textAlign: "left" }}>
                  <ReactMarkdown>{result.recomendaciones}</ReactMarkdown>
                </div>
              </div>
              <div style={{ background: "#f8f8f8", border: "1px solid #e0e0e0", borderRadius: 12, padding: 24 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
                  <div style={{ fontSize: 12, color: "#6b6b8a", textTransform: "uppercase", letterSpacing: "0.1em" }}>CV adaptado</div>
                  <button
                    onClick={downloadWord}
                    style={{ background: "#7c6af7", color: "#fff", border: "none", borderRadius: 6, padding: "6px 14px", fontSize: 12, cursor: "pointer" }}
                  >
                    ↓ Descargar Word
                  </button>
                </div>
                <div style={{ fontSize: 13, lineHeight: 1.7, color: "#1a1a1a", textAlign: "left" }}>
                  <ReactMarkdown>{result.cv_adaptado}</ReactMarkdown>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}