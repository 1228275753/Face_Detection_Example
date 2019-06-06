import sys
import http.client
import time
from vlc import VideoMarqueeOption, Position, EventType, Instance

# class RTSP_Client():
#    　　pass


class VLC_Player():

    def __init__(self, url):
        self.url = url

    def start(self):
# 　　　　　这种是最简方案，用来测试播放足够了
        instance = Instance()
        player = instance.media_player_new()
        Media = instance.media_new(self.url)
        Media.get_mrl()
        player.set_media(Media)
        player.play()

        event_manager = player.event_manager()
        # 播放到视频结尾时,返回end_callback()方法
        # event_manager.event_attach(EventType.MediaPlayerEndReached, end_callback)
        # 播放进度发生改变时,继续播放视频并(在控制台)显示播放进度
        event_manager.event_attach(EventType.MediaPlayerPositionChanged, pos_callback, player)
#         如果是视频,会在视频的最后一个画面停止
        while True:
            pass

def end_callback(event):
    print('End of media stream (event %s)' % event.type)
    print("视频播放结束")
    # p.start(1000)
    # sys.exit(0)

echo_position = True

def pos_callback(event, player):
    if echo_position:
        sys.stdout.write('\r%s to %.2f%% (%.2f%%)' % (event.type, event.u.new_position * 100, player.get_position() * 100))
        sys.stdout.flush()

if __name__ == "__main__":
# 　　 测试url为网络视频
#     url = "https://siiva-video-public.oss-cn-hangzhou.aliyuncs.com/1557886955xa/1557886955xa_1559297504675.mp4"
    url = "http://220.194.238.103/5/f/a/e/a/faeabxhpcuwjbugxqpgavhvibjfikc/hd.yinyuetai.com/22970150925A6BB75E20D95798D129EE.flv?sc\u003d17d6a907580e9892\u0026br\u003d1103\u0026vid\u003d2400382\u0026aid\u003d32\u0026area\u003dML\u0026vst\u003d0"
    p = VLC_Player(url)
    p.start()