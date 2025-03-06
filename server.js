const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

// Status endpoint
app.get('/api/status', (req, res) => {
  res.json({
    status: 'running',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Simple static file serving for testing
app.use(express.static('public'));

// Default route
app.get('/', (req, res) => {
  res.send(`
    <html>
      <head>
        <title>Development Server</title>
        <style>
          body { 
            font-family: Arial, sans-serif; 
            line-height: 1.6; 
            padding: 20px; 
            max-width: 800px; 
            margin: 0 auto; 
          }
          h1 { color: #333; }
          a { color: #0066cc; }
        </style>
      </head>
      <body>
        <h1>Development Server</h1>
        <p>This is the dev server for the OpenSaaS project.</p>
        <p>API endpoints:</p>
        <ul>
          <li><a href="/api/status">/api/status</a> - Server status</li>
        </ul>
      </body>
    </html>
  `);
});

app.listen(port, () => {
  console.log(`Dev server running at http://localhost:${port}`);
}); 