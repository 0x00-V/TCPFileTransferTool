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


#### Unencrypted Example
<img width="1073" height="729" alt="image" src="https://github.com/user-attachments/assets/795e4ffd-c0b2-4cf6-8987-f727dcaf83a1" />

#### Encrypted Example
<img width="1070" height="696" alt="image" src="https://github.com/user-attachments/assets/f46fbbbe-5a38-4e67-8f8b-e89c6acc31ed" />
