const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const liquidsoap = require('./controllers/liquidsoap');

const app = express();
app.use(bodyParser.json());

// API
app.use('/api', liquidsoap);

// Serve frontend build
app.use(express.static(path.join(__dirname, '../frontend/build')));
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/build', 'index.html'));
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`deva-web listening ${PORT}`));
