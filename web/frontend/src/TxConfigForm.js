import React, { useEffect, useState } from "react";
import API from "../Api";

export default function TxConfigForm() {
  const [config, setConfig] = useState("");
  useEffect(() => {
    API.getTxConfig().then(r => {
      if (r.ok) setConfig(r.config);
    });
  }, []);
  function save() {
    API.postTxConfig(config).then(r => {
      if (r.ok) alert("Saved and reloaded TX");
    }).catch(e => alert("error " + e));
  }
  function restart() {
    API.restartTx().then(r => {
      if (r.ok) alert("Restarted TX");
    }).catch(e => alert("error " + e));
  }
  return (
    <div>
      <h3>TX Liquidsoap config</h3>
      <textarea value={config} onChange={e=>setConfig(e.target.value)} style={{width:"100%",height:300}} />
      <div style={{marginTop:8}}>
        <button onClick={save}>Save & reload</button>
        <button style={{marginLeft:8}} onClick={restart}>Restart</button>
      </div>
    </div>
  );
}
