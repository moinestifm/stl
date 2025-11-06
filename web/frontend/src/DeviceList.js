import React, { useEffect, useState } from "react";
import API from "../Api";

export default function DeviceList() {
  const [devices, setDevices] = useState(null);
  useEffect(() => {
    API.getAlsadevices().then(r => setDevices(r.raw || "no data"));
  }, []);
  return (
    <div>
      <h3>ALSA Devices</h3>
      <pre style={{whiteSpace:"pre-wrap"}}>{devices || "loading..."}</pre>
    </div>
  );
}
