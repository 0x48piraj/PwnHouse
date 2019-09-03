#### AdobePSRAT : RCE using 

Adobe has a feature called "Remote Connections" which is used for various purposes. And we know that PS supports scripting. (https://www.adobe.com/devnet/photoshop/scripting.html)

The bug is, if the Remote Connection setting is enabled, then, we can execute arbitrary javascript code on Photoshop instance and for getting RCE, we have undocumented function called `app.system` (https://forums.adobe.com/thread/2300740)

The proof-of-concept doesn't work for now, but, I'll fiddle around in my spare time.