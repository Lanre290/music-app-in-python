import customtkinter  as ctk
from PIL import Image,ImageTk,ImageEnhance
import os
import math
from tktooltip import ToolTip
import vlc
import threading
import time
import random

dir = "C:\\Users\\Admin\\Music"
listOfSongs = os.listdir(dir)
print(listOfSongs)


root = ctk.CTk()
root.title("Music Player")
root.anchor("w")
root.state("zoomed")


initialVolume = 50
isAtHome = False
isAtPlaylist = False
isShuffle = False
currentRepeatMode = ""
currentRepeatNumber = 2
shuffleBtnToolTip = 0
currentSong:vlc.MediaPlayer = vlc.MediaPlayer('')
songList = []
currentSongNumber = 0

# ctk.CTkImage(Image.open())
# searchImage = ctk.CTkImage(Image.open("loupe.png").resize((60,60)))
# homeImage = ctk.CTkImage(Image.open("home.png").resize((80,80)))
# playlistImage = ctk.CTkImage(Image.open("playlist.png").resize((80,80)))
# checkedHomeImage = ctk.CTkImage(Image.open("home_1.png").resize((80,80)))
# checkedPlaylistImage = ctk.CTkImage(Image.open("playlist_1.png").resize((80,80)))
searchImage = ImageTk.PhotoImage(Image.open("loupe.png").resize((30,30)))
homeImage = ImageTk.PhotoImage(Image.open("home.png").resize((40,40)))
playlistImage = ImageTk.PhotoImage(Image.open("playlist.png").resize((40,40)))
checkedHomeImage = ImageTk.PhotoImage(Image.open("home_1.png").resize((40,40)))
checkedPlaylistImage = ImageTk.PhotoImage(Image.open("playlist_1.png").resize((40,40)))
albumArtImage = ImageTk.PhotoImage(Image.open("imageArt.jpeg").resize((80,90)))

disabledShuffleImage = Image.open("shuffle_5.png").resize((30,30))
disabledRepeatImage = Image.open("replay.png").resize((30,30))
enhancer_1 = ImageEnhance.Brightness(disabledShuffleImage)
enhancer_2 = ImageEnhance.Brightness(disabledRepeatImage)
# to reduce brightness by 50%, use factor 0.5
img = enhancer_1.enhance(0.5)
img_2 = enhancer_2.enhance(0.5)


disabledShuffleImage = ImageTk.PhotoImage(img)
disabledRepeatImage = ImageTk.PhotoImage(img_2)

shuffleImage = ImageTk.PhotoImage(Image.open("shuffle_5.png").resize((30,30)))
prevImage = ImageTk.PhotoImage(Image.open("previous.png").resize((40,40)))
playImage = ImageTk.PhotoImage(Image.open("play.png").resize((60,60)))
nextImage = ImageTk.PhotoImage(Image.open("next-track.png").resize((30,30)))
replayImage = ImageTk.PhotoImage(Image.open("replay.png").resize((30,30)))
replayOnceImage = ImageTk.PhotoImage(Image.open("repeat-once.png").resize((30,30)))
highVolumeImage = ImageTk.PhotoImage(Image.open("high-volume.png").resize((30,30)))
play_2 = ImageTk.PhotoImage(Image.open("play (1).png").resize((26,26)))
pause_2 = ImageTk.PhotoImage(Image.open("pause_1.png").resize((26,26)))
pauseImage = ImageTk.PhotoImage(Image.open("pause.png").resize((60,60)))
muteImage = ImageTk.PhotoImage(Image.open("mute.png").resize((30,30)))
# ∙


bottomFrame = ctk.CTkFrame(root,height = 130,corner_radius=20)
bottomFrame.pack(fill = "x",side = "bottom",pady = (3,0))

topSideBottom = ctk.CTkFrame(bottomFrame,height = 50,fg_color = "transparent")
topSideBottom.pack(fill = "x",side = "top",anchor = "w")
durationPlayed = ctk.CTkLabel(topSideBottom,text = "1:20",font = ("Calibri Light",15))
durationPlayed.pack(side = "left",padx = 10)
slider = ctk.CTkSlider(topSideBottom,width = 1270,button_color="#0099cc",progress_color="#0099cc",button_hover_color="#00a9c9",corner_radius=20)
slider.pack(side = "left")
durationLeft = ctk.CTkLabel(topSideBottom,text = "1:20",font = ("Calibri Light",15))
durationLeft.pack(side = "left",padx = 10)

bottomSideBottom = ctk.CTkFrame(bottomFrame,height = 80,fg_color="transparent")
bottomSideBottom.pack(fill = "x",side = "top",anchor = "w")
leftBottomSide = ctk.CTkFrame(bottomSideBottom,fg_color="transparent",cursor = "hand2",corner_radius=12)
leftBottomSide.pack(side="left",ipady = 5,ipadx = 5)
albumArt = ctk.CTkLabel(leftBottomSide,image = albumArtImage,corner_radius=20,text = "")
albumArt.pack(padx = (3,6),pady = (3,6),side = "left")
musicDeetsCont = ctk.CTkFrame(leftBottomSide,width = 200)
musicDeetsCont.pack(fill = "y",side = "left",anchor = "w")
musicName = ctk.CTkLabel(musicDeetsCont,text= "FortNight || Thinknews.com.ng",font = ("Calibri Light",25,"bold"),text_color = "#fafafa")
musicName.pack(side = "top",pady = (15,0),anchor = "w")
musicOtherDeets = ctk.CTkLabel(musicDeetsCont,text= f"Polo g ∙ Die a Legend",font = ("Calibri Light",19),text_color="#777777")
musicOtherDeets.pack(side = "top",anchor = "w")

def enterLeftBottomSide(event):
    leftBottomSide.configure(fg_color = "#333333")
    albumArt.configure(fg_color = "#333333")
    musicDeetsCont.configure(fg_color = "#333333")
    musicName.configure(fg_color = "#333333")
    musicOtherDeets.configure(fg_color = "#333333")
def leaveLeftBottomSide(event):
    leftBottomSide.configure(fg_color = "transparent")
    albumArt.configure(fg_color = "transparent")
    musicDeetsCont.configure(fg_color = "transparent")
    musicName.configure(fg_color = "transparent")
    musicOtherDeets.configure(fg_color = "transparent")

musicName.bind("<Leave>",leaveLeftBottomSide)
leftBottomSide.bind("<Enter>",enterLeftBottomSide)
albumArt.bind("<Enter>",enterLeftBottomSide)
musicDeetsCont.bind("<Enter>",enterLeftBottomSide)
musicName.bind("<Enter>",enterLeftBottomSide)
musicOtherDeets.bind("<Enter>",enterLeftBottomSide)
leftBottomSide.bind("<Leave>",leaveLeftBottomSide)

controls = ctk.CTkFrame(bottomSideBottom,fg_color="transparent")
controls.pack(side = "left",padx = 30)
shuffleBtn = ctk.CTkLabel(controls,image = disabledShuffleImage,cursor = "hand2",text = "",corner_radius = 12)
shuffleBtn.pack(side = "left",ipadx = 3,ipady = 10,padx = 2)
prevBtn = ctk.CTkLabel(controls,image = prevImage,cursor = "hand2",text = "",corner_radius = 12)
prevBtn.pack(side = "left",ipadx =3,ipady = 3,padx = 2)
playBtn = ctk.CTkLabel(controls,image = playImage,cursor = "hand2",text = "",fg_color="transparent",corner_radius = 12)
playBtn.pack(side = "left",ipadx = 3,ipady = 10,padx = 2)
nextBtn = ctk.CTkLabel(controls,image = nextImage,cursor = "hand2",text = "",corner_radius = 12)
nextBtn.pack(side = "left",ipadx = 3,ipady = 10,padx = 2)
repeatBtn = ctk.CTkLabel(controls,image = replayImage,cursor = "hand2",text = "",corner_radius = 12)
repeatBtn.pack(side = "left",ipadx = 3,ipady = 10,padx = 2)

ToolTip(playBtn, msg="Play", delay=0.5, follow=False,y_offset=-30,fg="#ededed", bg="#222222", padx=7, pady=7)
shuffleBtnToolTip = ToolTip(shuffleBtn, msg="shuffle", delay=0.5, follow=False,y_offset=-30,fg="#ededed", bg="#222222", padx=7, pady=7)
ToolTip(repeatBtn, msg="Repeat", delay=0.5, follow=False,y_offset=-30,fg="#ededed", bg="#222222", padx=7, pady=7)

def toggleShuffle(event):
    global isShuffle
    if isShuffle == True:
        isShuffle = False
    else:
        isShuffle = True
    manageShuffle()
def manageShuffle():
    global isShuffle
    if isShuffle == True:
        shuffleBtn.configure(image = shuffleImage,cursor = "hand2")
        # shuffleBtnToolTip.configure(msg = "shuffle(on)")  
    else:
        shuffleBtn.configure(image = disabledShuffleImage,cursor = "")
        # shuffleBtnToolTip.configure(msg = "Shuffle(Off)")

manageShuffle()
shuffleBtn.bind('<Button-1>',toggleShuffle)

repeatModes = ['one','all','off']
currentRepeatMode = repeatModes[currentRepeatNumber]
def switchRepeat(event):
    global currentRepeatNumber,currentRepeatMode,repeatModes
    if currentRepeatNumber == 2:
        currentRepeatNumber = 0
        currentRepeatMode = repeatModes[currentRepeatNumber]
    else:
        currentRepeatNumber+=1
        currentRepeatMode = repeatModes[currentRepeatNumber]

    if currentRepeatMode == "one":
        repeatBtn.configure(image = replayOnceImage)
        ToolTip(repeatBtn, msg="Repeat(one)", delay=0.5, follow=False,y_offset=-30,fg="#ededed", bg="#222222", padx=7, pady=7)
    if currentRepeatMode == "all":
        repeatBtn.configure(image = replayImage)
        ToolTip(repeatBtn, msg="Repeat(all)", delay=0.5, follow=False,y_offset=-30,fg="#ededed", bg="#222222", padx=7, pady=7)
    if currentRepeatMode == "off":
        repeatBtn.configure(image = disabledRepeatImage)
        ToolTip(repeatBtn, msg="Repeat(off)", delay=0.5, follow=False,y_offset=-30,fg="#ededed", bg="#222222", padx=7, pady=7)
    
repeatBtn.bind('<Button-1>',switchRepeat)




bottomRightSide = ctk.CTkFrame(bottomSideBottom,fg_color="transparent")
bottomRightSide.pack(side = "right",padx = (10,20))
volumeLabel = ctk.CTkLabel(bottomRightSide,image = highVolumeImage,text = "",cursor = "hand2")
volumeLabel.pack(side = "left",padx = (5,8))
volumeSlider = ctk.CTkSlider(bottomRightSide,width = 120,button_color="#0099cc",progress_color="#0099cc",from_=0,to=100,button_hover_color="#00a9c9",corner_radius=20)
volumeSlider.pack(side = "left",pady = (10,10))
volumeValue  = ctk.CTkLabel(bottomRightSide,text = initialVolume,font = ("Calibri Light",18))
volumeValue.pack(side = "left",padx = (5,5))

def changeVolume(event):
    global volumeValue,volumeSlider,currentSong
    volumeValue.configure(text = math.floor(volumeSlider.get()))
    currentSong.audio_set_volume(math.floor(volumeSlider.get()))
volumeSlider.bind('<Motion>',changeVolume)


def mute(event):
    global initialVolume,volumeValue
    if volumeLabel.cget("image") == highVolumeImage:
        volumeLabel.configure(image= muteImage)
        initialVolume = volumeSlider.get()
        volumeValue = volumeSlider.get()
        volumeSlider.set(0)
    else:
        volumeLabel.configure(image= highVolumeImage)
        volumeValue = volumeSlider.get()
        volumeSlider.set(initialVolume)
    currentSong.audio_toggle_mute()
def changeVolume(event):
    global initialVolume,volumeValue
    print("chdjd")
    if volumeSlider.get() == 0:
        volumeLabel.configure(image= muteImage)
        initialVolume = volumeSlider.get()
        volumeValue = volumeSlider.get()
    else:
        volumeLabel.configure(image= highVolumeImage)
        initialVolume = volumeSlider.get()
        volumeValue = volumeSlider.get()

volumeLabel.bind('<Button-1>',mute)





# left side frame#########################
#
#
##########################################
leftFrame  = ctk.CTkFrame(root,border_width=0.5,border_color="#111111",width=200,corner_radius=10)
leftFrame.pack(fill = "y",side = "left")

searchFrame = ctk.CTkFrame(leftFrame,width = 70,corner_radius=12,height = 50,fg_color = "#333333")
searchFrame.pack(padx = (10,10),pady=(20,5))
searchInput = ctk.CTkEntry(searchFrame,bg_color="transparent",fg_color="transparent",placeholder_text="Search...",font = ("Calibri Light",25),width= 240,height = 15,border_width=0)
searchInput.grid(row = 0,column=0,padx=(3,0),ipadx = (10),ipady = (3))
searchButton = ctk.CTkLabel(searchFrame,width = 45,height = 45,image = searchImage,text="",cursor = "hand2",corner_radius = 12)
searchButton.grid(row= 0,column = 1,padx = (0,10))

secondLeftFrame = ctk.CTkFrame(leftFrame,fg_color = "transparent")
secondLeftFrame.pack(fill = "x",pady = (25,0))

homeFrame = ctk.CTkFrame(secondLeftFrame,cursor = "hand2",corner_radius = 12)
homeFrame.pack(fill = "x",ipady = (10),padx = (5,5))
homeActive = ctk.CTkFrame(homeFrame,width = 5,height = 30,corner_radius=7,fg_color = "#00ccff")
homeActive.pack(side = "left",padx = (5,1),fill = "x")
homeIcon = ctk.CTkLabel(homeFrame,image = homeImage,text = "")
homeIcon.pack(side = "left",padx = (10,20))
homeLabel = ctk.CTkLabel(homeFrame,text = "Home",font = ("Calibri Light",23),anchor = "s")
homeLabel.pack(side = "left",fill = "x")

playlistFrame = ctk.CTkFrame(secondLeftFrame,cursor = "hand2",height = 65,corner_radius = 12)
playlistFrame.pack(fill = "x",ipady = (10),padx = (5,5))
playListActive = ctk.CTkFrame(playlistFrame,width = 5,height = 30,corner_radius=7,fg_color = "transparent")
playListActive.pack(side = "left",padx = (5,1),fill = "x")
playlistIcon = ctk.CTkLabel(playlistFrame,image = playlistImage,text = "")
playlistIcon.pack(side = "left",padx = (10,20))
playlistLabel = ctk.CTkLabel(playlistFrame,text = "Playlists",font = ("Calibri Light",23),anchor = "s")
playlistLabel.pack(side = "left",fill = "x")

def changeToHome(event):
    global isAtHome,isAtPlaylist
    homeFrame.configure(fg_color = "#333333")
    playlistFrame.configure(fg_color = "transparent")
    homeActive.configure(fg_color = "#00ccff")
    playListActive.configure(fg_color = "transparent")
    isAtHome = True
    isAtPlaylist = False
def changeToPlaylist(event):
    global isAtHome,isAtPlaylist
    homeFrame.configure(fg_color = "transparent")
    playlistFrame.configure(fg_color = "#333333")
    playListActive.configure(fg_color = "#00ccff")
    homeActive.configure(fg_color = "transparent")
    isAtHome = False
    isAtPlaylist = True


def enterHome(event):
    homeFrame.configure(fg_color = "#333333")
def leaveHome(event):
    global isAtHome
    print(isAtHome)
    if isAtHome == False:
        homeFrame.configure(fg_color = "transparent")
    else:
        homeFrame.configure(fg_color = "#333333")

def enterPlayList(event):
    playlistFrame.configure(fg_color = "#333333")
def leavePlayList(event):
    global isAtPlaylist
    print(isAtPlaylist)
    if isAtPlaylist == False:
        playlistFrame.configure(fg_color = "transparent")
    else:
        playlistFrame.configure(fg_color = "#333333")
    

homeFrame.bind('<Enter>',enterHome)
homeFrame.bind('<Leave>',leaveHome)
playlistFrame.bind('<Enter>',enterPlayList)
playlistFrame.bind('<Leave>',leavePlayList)


homeFrame.bind('<Button-1>',changeToHome)
homeIcon.bind('<Button-1>',changeToHome)
homeLabel.bind('<Button-1>',changeToHome)
playlistFrame.bind('<Button-1>',changeToPlaylist)
playlistIcon.bind('<Button-1>',changeToPlaylist)
playlistLabel.bind('<Button-1>',changeToPlaylist)

#######################
#right side
#######################
rightFrame = ctk.CTkFrame(root,corner_radius=10,fg_color = "transparent")
rightFrame.pack(fill = "both",padx = (4,6),pady = (6,6),anchor = "n")
musicLabel = ctk.CTkLabel(rightFrame,text = "Music",font = ("Calibri Light",47,"bold"),text_color = "#fafafa")
musicLabel.pack(anchor = "w",padx = (20,10),pady = (30,15))

musicCont  = ctk.CTkScrollableFrame(rightFrame,fg_color = "transparent",scrollbar_button_hover_color="#0099bb",height=1000)
musicCont.pack(fill = "both")
currentBg = "transparent"
def stop():
    currentSong.stop()


def listSong(dir):
    global musicCont,currentSong,currentSongNumber,stop,currentBg
    listOfSongs = os.listdir(dir)
    for song in listOfSongs:
        try:
            songDir = f"{dir}\\{song}"
            if(os.path.isdir(songDir)):
                listSong(songDir)

            else:
                if os.path.exists(songDir):
                    songList.append(songDir)
                    songLength:int = 0
                    if songDir.endswith(".mp3"):
                        if currentBg == "transparent":
                            currentBg = "#333333"
                        else:
                            currentBg = "transparent"
                        musicListCont = ctk.CTkFrame(musicCont,corner_radius=12,fg_color = f'{currentBg}')
                        musicListCont.pack(side = "top",anchor = "w",ipadx = 5,ipady = 7,fill = "x",pady = (5,5))
                        musicPlayBtn = ctk.CTkLabel(musicListCont,image = "",text = "",cursor = "hand2",corner_radius = 8)
                        musicPlayBtn.pack(side = "left",padx = (30,7),ipadx = 1,ipady = 3)
                        if len(song) > 50:
                            song = song[:50-3] + '...'
                        musicListedTitle = ctk.CTkLabel(musicListCont,width = 490,text = f"{song.capitalize()}",font = ("Calibri Light",19),text_color="#fafafa",anchor="w",wraplength=490)
                        musicListedTitle.pack(side = "left",padx = (7,10))
                        musicListedArtist = ctk.CTkLabel(musicListCont,text = "Rema",font = ("Calibri Light",19),width = 10,text_color="#fafafa",anchor = "w")
                        musicListedArtist.pack(side = "left",padx = (15,10),anchor = "w")
                        musicListedAlbum = ctk.CTkLabel(musicListCont,text = "Rave and roses",font = ("Calibri Light",19),width = 10,text_color="#fafafa",anchor = "w")
                        musicListedAlbum.pack(side = "left",padx = (15,10),anchor = "w")
                        musicListedYear = ctk.CTkLabel(musicListCont,text = "2017",font = ("Calibri Light",19),width = 40,text_color="#fafafa",anchor = "w")
                        musicListedYear.pack(side = "left",padx = (15,10),anchor = "w")
                        musicListedGenre = ctk.CTkLabel(musicListCont,text = "Trap",font = ("Calibri Light",19),width = 60,text_color="#fafafa",anchor = "w")
                        musicListedGenre.pack(side = "left",padx = (15,10),anchor = "w")
                        musicListedDuration = ctk.CTkLabel(musicListCont,text = f"{math.floor(songLength/3)}",font = ("Calibri Light",19),width = 20,text_color="#fafafa",anchor = "w")
                        musicListedDuration.pack(side = "left",padx = (15,10),anchor = "w")

                        def hoverMusicListCont(event,btn = musicPlayBtn):
                            btn.configure(image = play_2)
                        def leaveMusicListCont(event,btn = musicPlayBtn):
                            btn.configure(image = "")

                        musicListCont.bind('<Enter>',hoverMusicListCont)
                        musicPlayBtn.bind('<Enter>',hoverMusicListCont)
                        musicListedTitle.bind('<Enter>',hoverMusicListCont)
                        musicListedArtist.bind('<Enter>',hoverMusicListCont)
                        musicListedAlbum.bind('<Enter>',hoverMusicListCont)
                        musicListedYear.bind('<Enter>',hoverMusicListCont)
                        musicListedGenre.bind('<Enter>',hoverMusicListCont)
                        musicListedDuration.bind('<Enter>',hoverMusicListCont)
                        musicListCont.bind('<Leave>',leaveMusicListCont)

                        def enterPlayBtn(event):
                            musicPlayBtn.configure(fg_color = "#333333")
                        def leavePlayBtn(event):
                            musicPlayBtn.configure(fg_color = "transparent")
                        def clickPlayBtn(event,songDir_ = songDir,button = musicPlayBtn):
                            global currentSong,stop
                            stop()
                            if button.cget("image") == play_2:
                                button.configure(image = pause_2)
                                currentSong = vlc.MediaPlayer(f'{songDir_}')
                            else:
                                button.configure(image = play_2)
                            playContent()
                        musicPlayBtn.bind('<Enter>',enterPlayBtn)
                        musicPlayBtn.bind('<Leave>',leavePlayBtn)
                        musicPlayBtn.bind('<Button-1>',clickPlayBtn)
        
        except FileNotFoundError:
            pass
        finally:
            pass

listSong(dir)
def playContent():
    if playBtn.cget("image") == playImage:
        playBtn.configure(image= pauseImage)
        currentSong.play()
    else:
        playBtn.configure(image= playImage)
        currentSong.pause()
    print(currentSong.get_length())
def playCurrentSong(event):
    playContent()


if isShuffle == True:
    currentSongNumber = random.randint(0,len(songList)-1)
# currentSong = songList[currentSongNumber]

# currentSong.get_length()

playBtn.bind('<Button-1>',playCurrentSong)


def updateEverySecond():
    global durationLeft,durationPlayed
    totalTime = currentSong.get_length()
    currentPosition = currentSong.get_position()/1000

    print(currentPosition)

    durationPlayed.configure(text = f'{math.floor(currentPosition/60)}:{math.floor(currentPosition%60)}')
    durationLeft.configure(text = f'{math.floor(totalTime/60)}:{math.floor(totalTime%60)}')
    time.sleep(1)


# FunctionTimer = threading.Thread(target = updateEverySecond)
# FunctionTimer.start()


def addGreyBg(widget:ctk.CTkFrame):
    def func(event):
        widget.configure(fg_color = "#333333")
    def func_2(event):
        widget.configure(fg_color = "transparent")
    widget.bind("<Enter>",func)
    widget.bind("<Leave>",func_2)

arrOfElementForGreyHover = [shuffleBtn,prevBtn,nextBtn,repeatBtn,homeFrame,playlistFrame]
for element in arrOfElementForGreyHover:
    addGreyBg(element)

root.mainloop()