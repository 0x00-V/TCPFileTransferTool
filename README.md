## Usage

### Start the server

```bash
python TCPFileTransferTool.py server -p 4444
```

#### Send a file
```bash
python TCPFileTransferTool.py client \
  -H 127.0.0.1 \
  -p 4444 \
  -fp /path/to/file.exe \
  -fn example.exe
```
