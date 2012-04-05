"""
* Copyright 2009 Mark Renouf
*
* Licensed under the Apache License, Version 2.0 (the "License"); you may not
* use this file except in compliance with the License. You may obtain a copy of
* the License at
*
* http:#www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHDIR
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
* License for the specific language governing permissions and limitations under
* the License.
"""


class Media(Widget):

    def mediaEventGetTypeInt(self, eventType):
        JS("""
        window.console.log('mediaEventGetTypeInt: ' + eventType);
        switch (eventType) {
            case "abort":             return 0x00001;
            case "canplay":           return 0x00002;
            case "canplaythrough":    return 0x00004;
            case "durationchange":    return 0x00008;
            case "emptied":           return 0x00010;
            case "ended":             return 0x00020;
            case "error":             return 0x00040;
            case "loadstart":         return 0x00080;
            case "loadeddata":        return 0x00100;
            case "loadedmetadata":    return 0x00200;
            case "pause":             return 0x00400;
            case "play":              return 0x00800;
            case "playing":           return 0x01000;
            case "progress":          return 0x02000;
            case "ratechange":        return 0x04000;
            case "seeked":            return 0x08000;
            case "seeking":           return 0x10000;
            case "stalled":           return 0x20000;
            case "suspend":           return 0x40000;
            case "timeupdate":        return 0x80000;
            case "volumechange":      return 0x100000;
            case "waiting":           return 0x200000;
            default:
            window.console.debug("Unknown media eventType: " + eventType);
            return 0;
        }
        """)
    
    def nativeSinkMediaEvents(self, elem, bits):
        JS("""
        var chMask = (elem.__mediaEventBits || 0) ^ bits;
        elem.__mediaEventBits = bits;
        if (!chMask) return;
        
        if (chMask & 0x00001) if (bits & 0x00001)
        elem.addEventListener('abort', mediaDispatchEvent, false)
        else elem.removeEventListener('abort', mediaDispatchEvent, false);
        if (chMask & 0x00002) if (bits & 0x00002)
        elem.addEventListener('canplay', mediaDispatchEvent, false)
        else elem.removeEventListener('canplay', mediaDispatchEvent, false);
        if (chMask & 0x00004) if (bits & 0x00004)
        elem.addEventListener('canplaythrough', mediaDispatchEvent, false)
        else elem.removeEventListener('canplaythrough', mediaDispatchEvent, false);
        if (chMask & 0x00008) if (bits & 0x00008)
        elem.addEventListener('durationchange', mediaDispatchEvent, false)
        else elem.removeEventListener('durationchange', mediaDispatchEvent, false);
        if (chMask & 0x00010) if (bits & 0x00010)
        elem.addEventListener('emptied', mediaDispatchEvent, false)
        else elem.removeEventListener('emptied', mediaDispatchEvent, false);
        if (chMask & 0x00020) if (bits & 0x00020)
        elem.addEventListener('ended', mediaDispatchEvent, false)
        else elem.removeEventListener('ended', mediaDispatchEvent, false);
        if (chMask & 0x00040) if (bits & 0x00040)
        elem.addEventListener('error', mediaDispatchEvent, false)
        else elem.removeEventListener('error', mediaDispatchEvent, false);
        if (chMask & 0x00080) if (bits & 0x00080)
        elem.addEventListener('loadstart', mediaDispatchEvent, false)
        else elem.removeEventListener('loadstart', mediaDispatchEvent, false);
        if (chMask & 0x00100) if (bits & 0x00100)
        elem.addEventListener('loadeddata', mediaDispatchEvent, false)
        else elem.removeEventListener('loadeddata', mediaDispatchEvent, false);
        if (chMask & 0x00200) if (bits & 0x00200)
        elem.addEventListener('loadedmetadata', mediaDispatchEvent, false)
        else elem.removeEventListener('loadedmetadata', mediaDispatchEvent, false);
        if (chMask & 0x00400) if (bits & 0x00400)
        elem.addEventListener('pause', mediaDispatchEvent, false)
        else elem.removeEventListener('pause', mediaDispatchEvent, false);
        if (chMask & 0x00800) if (bits & 0x00800)
        elem.addEventListener('play', mediaDispatchEvent, false)
        else elem.removeEventListener('play', mediaDispatchEvent, false);
        if (chMask & 0x01000) if (bits & 0x01000)
        elem.addEventListener('playing', mediaDispatchEvent, false)
        else elem.removeEventListener('playing', mediaDispatchEvent, false);
        if (chMask & 0x02000) if (bits & 0x02000)
        elem.addEventListener('progress', mediaDispatchEvent, false)
        else elem.removeEventListener('progress', mediaDispatchEvent, false);
        if (chMask & 0x04000) if (bits & 0x04000)
        elem.addEventListener('ratechange', mediaDispatchEvent, false)
        else elem.removeEventListener('ratechange', mediaDispatchEvent, false);
        if (chMask & 0x08000) if (bits & 0x08000)
        elem.addEventListener('seeked', mediaDispatchEvent, false)
        else elem.removeEventListener('seeked', mediaDispatchEvent, false);
        if (chMask & 0x10000) if (bits & 0x10000)
        elem.addEventListener('seeking', mediaDispatchEvent, false)
        else elem.removeEventListener('seeking', mediaDispatchEvent, false);
        if (chMask & 0x20000) if (bits & 0x20000)
        elem.addEventListener('stalled', mediaDispatchEvent, false)
        else elem.removeEventListener('stalled', mediaDispatchEvent, false);
        if (chMask & 0x40000) if (bits & 0x40000)
        elem.addEventListener('suspend', mediaDispatchEvent, false)
        else elem.removeEventListener('suspend', mediaDispatchEvent, false);
        if (chMask & 0x80000) if (bits & 0x80000)
        elem.addEventListener('timeupdate', mediaDispatchEvent, false)
        else elem.removeEventListener('timeupdate', mediaDispatchEvent, false);
        if (chMask & 0x100000) if (bits & 0x100000)
        elem.addEventListener('volumechange', mediaDispatchEvent, false)
        else elem.removeEventListener('volumechange', mediaDispatchEvent, false);
        if (chMask & 0x200000) if (bits & 0x200000)
        elem.addEventListener('waiting', mediaDispatchEvent, false)
        else elem.removeEventListener('waiting', mediaDispatchEvent, false);
        """)
    
    '''*
    * Warning: W3C/Standards version
    def initMediaEvents(self):
        JS("""
        mediaDispatchEvent = function(evt) {
            var curElem = evt.target;
            var listener = curElem.__listener;
            if (listener) {
                @{{dispatchMediaEvent}}(evt, listener);
            }
        }
        """)
    
    '''
