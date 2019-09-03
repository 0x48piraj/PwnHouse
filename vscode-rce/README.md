#### VSCode 1.19.2 RCE

Issue - https://github.com/microsoft/vscode/issues/39569

- Runs in debug mode, on port 9333.
- Protocol implemented is devtools
- For exploitation, we need to interact with devtools protocol
- Using Chrome, we can inject arbitrary javascript code
- See `poc.js` for popping calc.exe on Windows