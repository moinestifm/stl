function drawVUMeter(canvasId, value) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    ctx.fillStyle = '#333';
    ctx.fillRect(0, 0, width, height);

    const meterHeight = Math.max(0, Math.min(height, height * value));
    ctx.fillStyle = value > 0.7 ? '#f39c12' : '#27ae60';
    ctx.fillRect(0, height - meterHeight, width, meterHeight);
}
