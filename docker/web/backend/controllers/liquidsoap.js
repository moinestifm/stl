const express = require('express');
const router = express.Router();
const { execSync, spawnSync } = require('child_process');
const fs = require('fs');
const axios = require('axios');

const TX_CONTROL_URL = process.env.TX_CONTROL_URL || "http://deva_tx:8081";
const RX_CONTROL_URL = process.env.RX_CONTROL_URL || "http://deva_rx:8081";
const CONTROL_TOKEN = process.env.CONTROL_TOKEN || "change_me_token";

// return ALSA devices
router.get('/devices/alsa', (req, res) => {
  try {
    const out = execSync('arecord -l || true').toString();
    res.json({ok:true, raw: out});
  } catch (e) {
    res.status(500).json({ok:false, error: e.message});
  }
});

// fetch current tx.liq config (via tx control server)
router.get('/tx/config', async (req, res) => {
  try {
    const r = await axios.get(`${TX_CONTROL_URL}/control/readconf`, { headers: {"X-Control-Token": CONTROL_TOKEN}, timeout: 3000 });
    res.json({ok:true, config: r.data.config});
  } catch (e) {
    res.status(500).json({ok:false, error: e.message});
  }
});

// write tx config - body: { content: "..." }
router.post('/tx/config', async (req, res) => {
  const content = req.body.content || "";
  try {
    await axios.post(`${TX_CONTROL_URL}/control/writeconf`, {content}, { headers: {"X-Control-Token": CONTROL_TOKEN} });
    res.json({ok:true});
  } catch (e) {
    res.status(500).json({ok:false, error: e.message});
  }
});

// restart tx
router.post('/tx/restart', async (req, res) => {
  try {
    const r = await axios.post(`${TX_CONTROL_URL}/control/restart`, {}, { headers: {"X-Control-Token": CONTROL_TOKEN} });
    res.json({ok:true, result: r.data});
  } catch (e) {
    res.status(500).json({ok:false, error: e.message});
  }
});

// same for rx
router.post('/rx/restart', async (req, res) => {
  try {
    const r = await axios.post(`${RX_CONTROL_URL}/control/restart`, {}, { headers: {"X-Control-Token": CONTROL_TOKEN} });
    res.json({ok:true, result: r.data});
  } catch (e) {
    res.status(500).json({ok:false, error: e.message});
  }
});

router.get('/rx/config', async (req, res) => {
  try {
    const r = await axios.get(`${RX_CONTROL_URL}/control/readconf`, { headers: {"X-Control-Token": CONTROL_TOKEN}, timeout: 3000 });
    res.json({ok:true, config: r.data.config});
  } catch (e) {
    res.status(500).json({ok:false, error: e.message});
  }
});

router.post('/rx/config', async (req, res) => {
  const content = req.body.content || "";
  try {
    await axios.post(`${RX_CONTROL_URL}/control/writeconf`, {content}, { headers: {"X-Control-Token": CONTROL_TOKEN} });
    res.json({ok:true});
  } catch (e) {
    res.status(500).json({ok:false, error: e.message});
  }
});

module.exports = router;
