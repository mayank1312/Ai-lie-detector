import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingAudio, setLoadingAudio] = useState(null);

  const analyze = async () => {
    if (!text) return;

    setLoading(true);
    setResult(null);

    const currentText = text;
    setText("");

    const loadAudio = new Audio("/loading.mp3");
  loadAudio.loop = true;
  loadAudio.play().catch(() => {});
  setLoadingAudio(loadAudio);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: currentText }),
      });

      const data = await res.json();

      loadAudio.pause();
    loadAudio.currentTime = 0;

      setResult({
        ...data,
        statement: currentText,
      });

      playSound(data.verdict);
    } catch (err) {
      console.error(err);
      loadAudio.pause();
    loadAudio.currentTime = 0;
    } finally {
      setLoading(false);
    }
  };

  const playSound = (verdict) => {
    const audio = new Audio(
      verdict === "True" ? "/truth.mp3" : "/lie.mp3"
    );
    audio.play();
  };

  return (
    <div className="app-layout">
      <header className="topbar">
        <h1 className="logo">AI Lie Detector</h1>
      </header>

      <main className="main-content">
        {/* INPUT */}
        <section className="panel">
          <div className="panel-header">
            <h2>Input Statement</h2>
          </div>

          <div className="input-group">
            <span className="input-icon">🔗</span>

            <input
              className="text-input"
              type="text"
              placeholder="Type your statement..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />

            <button
              className="primary-btn"
              onClick={analyze}
              disabled={loading}
            >
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </div>
        </section>


        <section className="panel">
          <div className="panel-header status-header">
            <h2>Analysis Engine</h2>

            <div className="indicators">
            
              <div
                className={`bulb bulb-blue ${
                  !loading && result?.verdict === "True" ? "glow-blue" : ""
                } ${loading ? "bulb-pulse" : ""}`}
              />

           
              <div
                className={`bulb bulb-red ${
                  !loading && result?.verdict === "False" ? "glow-red" : ""
                } ${loading ? "bulb-pulse" : ""}`}
              />
            </div>
          </div>

      
          {loading && (
            <div className="loading-text">
              🔍 Analyzing statement...
            </div>
          )}


          {result && !loading && (
            <div className="result-data">
              <div className="data-row">
                <span className="data-label">Verdict</span>
                <span
                  className={`badge badge-${result.verdict.toLowerCase()}`}
                >
                  {result.verdict}
                </span>
              </div>

              <div className="data-row">
                <span className="data-label">Statement</span>
                <span className="data-value statement-text">
                  "{result.statement}"
                </span>
              </div>

              <div className="data-row">
                <span className="data-label">Reasoning</span>
                <span className="data-value">{result.reason}</span>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;