# discord-gateway-presence

A minimal Python client that sets Discord user presence directly through the Gateway WebSocket.  
No Discord libraries. No API wrappers. Lightweight, async, and ideal for learning the Discord protocol.

> ⚠️ **Educational use only.** User account automation is against Discord’s Terms of Service.  
> Use at your own risk.

## Features
- Raw WebSocket presence update
- Supports desktop, mobile, and browser client properties
- Custom status, activity type, and text fields
- Heartbeat and auto-reconnect logic
- Minimal dependencies (`aiohttp` only)
- 
## Quick Start

### Requirements
```sh
pip install aiohttp
