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




abstract class MediaElement extends Element:
    
    def __init__(self):
    
    
    def getError(self):
        JS("""
        return (this.error == null) ? 0 : this.error;
        """)
    
    
    def getSrc(self):
        JS("""
        return this.getAttribute('src');
        """)
    
    
    def setSrc(self, url):
        JS("""
        this.setAttribute('src', url);
        """)
    
    
    def getCurrentSrc(self):
        JS("""
        return this.currentSrc;
        """)
    
    
    def getNetworkState(self):
        JS("""
        return this.networkState;
        """)
    
    
    def setAutobuffer(self, autobuffer):
        JS("""
        this.autobuffer = autobuffer;
        """)
    
    
    def getBuffered(self):
        JS("""
        return this.buffered;
        """)
    
    
    def load(self):
        JS("""
        this.load();
        """)
    
    
    def canPlayType(self, type):
        JS("""
        return this.canPlayType(type);
        """)
    
    
    def getReadyState(self):
        JS("""
        return this.readyState;
        """)
    
    
    def isSeeking(self):
        JS("""
        return media.seeking;
        """)
    
    
    def getCurrentTime(self):
        JS("""
        return this.currentTime;
        """)
    
    
    def setCurrentTime(self, time):
        JS("""
        this.currentTime = time;
        """)
    
    
    def getStartTime(self):
        JS("""
        return this.startTime;
        """)
    
    
    def getDuration(self):
        JS("""
        return this.duration;
        """)
    
    
    def isPaused(self):
        JS("""
        return this.paused;
        """)
    
    
    def getDefaultPlaybackRate(self):
        JS("""
        return this.defaultPlaybackRate;
        """)
    
    
    def setDefaultPlaybackRate(self, rate):
        JS("""
        this.defaultPlaybackRate = rate;
        """)
    
    
    def getPlaybackRate(self):
        JS("""
        return this.playbackRate;
        """)
    
    
    def setPlaybackRate(self, rate):
        JS("""
        this.playbackRate = rate;
        """)
    
    
    def getPlayed(self):
        JS("""
        return this.played;
        """)
    
    
    def getSeekable(self):
        JS("""
        return this.seekable;
        """)
    
    
    def hasEnded(self):
        JS("""
        return this.ended;
        """)
    
    
    def setAutoplay(self, autoplay):
        JS("""
        this.autoplay = autoplay;
        """)
    
    
    def setLoop(self, loop):
        JS("""
        this.loop = loop;
        """)
    
    
    def isLoop(self):
        JS("""
        return !!(this.loop);
        """)
    
    
    def play(self):
        JS("""
        this.play();
        """)
    
    
    def pause(self):
        JS("""
        this.pause();
        """)
    
    
    def setControls(self, controls):
        setBooleanAttr("controls", controls)
    
    
    def getVolume(self):
        JS("""
        return this.volume;
        """)
    
    
    def setVolume(self, volume):
        JS("""
        this.volume = volume
        """)
    
    
    def isMuted(self):
        JS("""
        return this.muted;
        """)
    
    
    def setMute(self, muted):
        JS("""
        this.muted = muted;
        """)
    
    
    def setBooleanAttr(self, name, value):
        if value:
            setAttribute(name, "")
        
        else:
            removeAttribute(name)
        
    
    
    def hasControls(self):
        JS("""
        return !!(elem.getAttribute('controls'));
        """)
    


