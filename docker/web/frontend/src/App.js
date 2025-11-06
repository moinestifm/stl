import React from "react";
import DeviceList from "./components/DeviceList";
import TxConfigForm from "./components/TxConfigForm";

export default function App() {
  return (
    <div style={{padding:20,fontFamily:'sans-serif'}}>
      <h1>DEVA-STL Control Panel</h1>
      <p>Use the forms below to configure TX/RX Liquidsoap and restart services.</p>
      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:20}}>
        <div>
          <DeviceList/>
        </div>
        <div>
          <TxConfigForm/>
        </div>
      </div>
    </div>
  );
}
