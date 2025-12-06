# discord-gateway-presence
# Minimal user presence over raw Gateway (no discord libs needed)
# Not Discord API friendly — use at your own risk.

TOKEN = "YOUR_TOKEN"
platform = "mobile"   # desktop | mobile | browser
status   = "online"   # online | idle | dnd
activity = "playing"  # playing | streaming | competing | listening | watching
name="a" # big text aka title
details="a" # small text
state="a" # bottom text
appid="" # your bot's / app ID


import aiohttp,asyncio,json,time,sys,random
GW = "wss://gateway.discord.gg/?v=10&encoding=json"
PROPS={
 "desktop":{"$os":"Windows","$browser":"Discord Client","$device":""},
 "mobile":{"$os":"Android","$browser":"Discord Android","$device":"Mobile"},
 "browser":{"$os":"Windows","$browser":"Chrome","$device":""}
}
T={"playing":0,"streaming":2,"listening":3,"watching":4,"competing":5}

sid=None;seq=None

async def sb():
    global sid,seq
    while True:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.ws_connect(GW,max_msg_size=0) as ws:
                    hello = await ws.receive_json()
                    hb = hello["d"]["heartbeat_interval"] / 1000
                    next_hb = time.time() + hb

                    A={"name":name,"details":details,"state":state,
                       "type":T.get(activity,0),"application_id":appid,
                       "timestamps":{"start":int(time.time()*1000)},
                       "assets":{},"flags":1}
                    P={"since":0,"activities":[A],"status":status,"afk":False}
                    ID={"token":TOKEN,"intents":0,
                        "properties":PROPS.get(platform,PROPS["desktop"]),
                        "presence":P}

                    await ws.send_json({"op":6,"d":{"token":TOKEN,"session_id":sid,"seq":seq}} if sid else {"op":2,"d":ID})
                    print(f"ok {platform}/{status}/{activity}")

                    while True:
                        if time.time() >= next_hb:
                            await ws.send_json({"op":1,"d":seq})
                            next_hb = time.time() + hb

                        r = await ws.receive(timeout=hb*1.3)
                        if r.type in (aiohttp.WSMsgType.CLOSED,aiohttp.WSMsgType.ERROR):
                            raise Exception("closed")

                        if r.type != aiohttp.WSMsgType.TEXT:
                            continue
                        j=json.loads(r.data)
                        op=j.get("op")
                        seq=j.get("s",seq)

                        if op==10: continue

                        if j.get("t")=="READY":
                            sid=j["d"]["session_id"]
                            await ws.send_json({"op":3,"d":P})

                        elif op==9:
                            sid=None
                            raise Exception("invalid session")
        except Exception as er:
            print("reconnect", er)
            await asyncio.sleep(random.uniform(4,9))

try:
    asyncio.run(sb())
except:
    sys.exit()