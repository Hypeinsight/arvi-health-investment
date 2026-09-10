/* Arvi dev-pipeline - shared feature-status board.
 * Zero-dependency Node server. Serves the static board and stores the
 * shared board as a .txt on a persistent disk (DATA_DIR). Every edit
 * from any teammate POSTs here and updates that one file.
 */
const http = require('http');
const fs   = require('fs');
const path = require('path');

const PORT      = process.env.PORT || 3000;
// On Render, default to the persistent disk mount; locally, a ./data folder.
const DATA_DIR  = process.env.DATA_DIR || (process.env.RENDER ? '/var/data' : path.join(__dirname, 'data'));
const DATA_FILE = path.join(DATA_DIR, 'arvi-feature-status.txt');
const SEED_FILE = path.join(__dirname, 'seed.txt');
const MARK = '=== BOARD DATA (needed to load this file back, please do not edit) ===';

function ensureData(){
  fs.mkdirSync(DATA_DIR, { recursive:true });
  if(!fs.existsSync(DATA_FILE)){
    let seed;
    try { seed = fs.readFileSync(SEED_FILE, 'utf8'); }
    catch(e){ seed = MARK + '\r\n[]'; }
    fs.writeFileSync(DATA_FILE, seed);
  }
}
function readBoard(){
  const text = fs.readFileSync(DATA_FILE, 'utf8');
  let items = [];
  const at = text.indexOf(MARK);
  if(at >= 0){ try { items = JSON.parse(text.slice(at + MARK.length).trim()); } catch(e){ items = []; } }
  const updatedAt = Math.floor(fs.statSync(DATA_FILE).mtimeMs);
  return { text, items, updatedAt };
}

const TYPES = {
  '.html':'text/html; charset=utf-8', '.txt':'text/plain; charset=utf-8',
  '.js':'text/javascript', '.css':'text/css', '.json':'application/json',
  '.png':'image/png', '.svg':'image/svg+xml', '.ico':'image/x-icon',
  '.webp':'image/webp', '.avif':'image/avif'
};
function serveStatic(req, res){
  let p = decodeURIComponent(req.url.split('?')[0]);
  if(p === '/' || p === '') p = '/index.html';
  const file = path.join(__dirname, path.normalize(p));
  if(!file.startsWith(__dirname)){ res.writeHead(403); res.end('forbidden'); return; }
  fs.readFile(file, (err, buf) => {
    if(err){ res.writeHead(404); res.end('not found'); return; }
    res.writeHead(200, {
      'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-cache'
    });
    res.end(buf);
  });
}

const server = http.createServer((req, res) => {
  const url = req.url.split('?')[0];
  if(url === '/api/board'){
    if(req.method === 'GET'){
      try { const b = readBoard();
        res.writeHead(200, { 'Content-Type':'application/json', 'Cache-Control':'no-store' });
        res.end(JSON.stringify(b));
      } catch(e){ res.writeHead(500); res.end(JSON.stringify({ error:String(e) })); }
      return;
    }
    if(req.method === 'POST'){
      let body = '', tooBig = false;
      req.on('data', c => { body += c; if(body.length > 5e6){ tooBig = true; req.destroy(); } });
      req.on('end', () => {
        if(tooBig){ res.writeHead(413); res.end('too large'); return; }
        try {
          const { text } = JSON.parse(body);
          if(typeof text !== 'string' || text.indexOf(MARK) < 0) throw new Error('bad payload');
          JSON.parse(text.slice(text.indexOf(MARK) + MARK.length).trim()); // validate embedded JSON
          const tmp = DATA_FILE + '.tmp';
          fs.writeFileSync(tmp, text);
          fs.renameSync(tmp, DATA_FILE); // atomic replace
          const updatedAt = Math.floor(fs.statSync(DATA_FILE).mtimeMs);
          res.writeHead(200, { 'Content-Type':'application/json' });
          res.end(JSON.stringify({ ok:true, updatedAt }));
        } catch(e){
          res.writeHead(400, { 'Content-Type':'application/json' });
          res.end(JSON.stringify({ error:String(e) }));
        }
      });
      return;
    }
    res.writeHead(405); res.end('method not allowed'); return;
  }
  if(req.method === 'GET'){ serveStatic(req, res); return; }
  res.writeHead(404); res.end('not found');
});

ensureData();
server.listen(PORT, () => console.log('arvi dev-pipeline listening on :' + PORT + '  data=' + DATA_FILE));
