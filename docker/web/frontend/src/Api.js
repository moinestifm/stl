const API = {
    getAlsadevices: () => fetch("/api/devices/alsa").then(r => r.json()),
    getTxConfig: () => fetch("/api/tx/config").then(r => r.json()),
    postTxConfig: (content) => fetch("/api/tx/config", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({content})}).then(r => r.json()),
    restartTx: () => fetch("/api/tx/restart", {method:"POST"}).then(r => r.json()),
    getRxConfig: () => fetch("/api/rx/config").then(r => r.json()),
    postRxConfig: (content) => fetch("/api/rx/config", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({content})}).then(r => r.json()),
    restartRx: () => fetch("/api/rx/restart", {method:"POST"}).then(r => r.json())
  };
  
  export default API;
  