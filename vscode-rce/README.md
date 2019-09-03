#### VSCode 1.19.2 RCE

Issue - https://github.com/microsoft/vscode/issues/39569

- Runs in debug mode, on port 9333.
- Protocol implemented is devtools
- For exploitation, we need to interact with devtools protocol
- We can inject arbitrary javascript code using Inspect, attaching `localhost:9333`, interacting it via Chrome's devtool console
- See `poc.js` for popping calc.exe on Windows
- For making it **remote** RCE, we need to interact with devtools protocol which is based on HTTP and WebSocket
- The debugger URL can be used to communicate with `ws://` directly. (https://nodejs.org/de/docs/guides/debugging-getting-started/)

> Node.js 6.x and later include a debugger protocol (also known as "inspector") that can be activated by the --inspect and related command line flags. This debugger service was vulnerable to a DNS rebinding attack which could be exploited to perform remote code execution. The attack was possible from malicious websites open in a web browser on the same computer, or another computer with network access to the computer running the Node.js process.

That's the same debugger protocol vs-code uses, but already running with `--inspect`, & someone already exploited it cleverly. _(via DNS Rebinding Attack)_

DNS rebinding attack was probably used to fetch the URL because a website can't access `127.0.0.1` directly as stated below,

> By default node --inspect binds to 127.0.0.1. You explicitly need to provide a public IP address or 0.0.0.0, etc., if you intend to allow external connections to the debugger. Doing so may expose you to a potentially significant security threat. We suggest you ensure appropriate firewalls and access controls in place to prevent a security exposure.