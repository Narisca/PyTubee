from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
from pytube import YouTube, Playlist
from colorama import Fore, init, Style
import sys, os

init()
class Downloader(object):
    def __init__(self) -> None:
        self.invalid_chars = r'<>:"/\|?*'

    def sanitize_filename(self, filename):
        for char in self.invalid_chars:
            filename = filename.replace(char, '')
        return filename

    def down_video(self, video_link = None) -> None:
        if video_link == None:
            video_link = console.question("Youtube video link: ")
        yt = YouTube(video_link)

        try:
            sanitized_title = self.sanitize_filename(yt.title)
            stay = yt.streams.filter(progressive=True, res="1080p").first()
            res = "1080p"
            if stay is None:
                stay = yt.streams.filter(progressive=True, res="720p").first()
                res = "720p"
                if stay is None:
                    stay = yt.streams.filter(progressive=True, res="480p").first()
                    res = "480p"
                    if stay is None:
                        stay = yt.streams.filter(progressive=True, res="360p").first()
                        res = "360p"
                        if stay is None:
                            return ""
                        
            console.info(f"Başlık: {yt.title} Çözünürlük: {res}")

            stay.download(output_path="Videolar")
            console.success(f"{sanitized_title} Video 'Videolar' klasörüne kayıt edildi.")

        except Exception as e:
            console.error(e)

    def down_mp3(self, video_link = None) -> None:
        try:
            if video_link == None:
                video_link = console.question("Youtube video link: ")

            yt = YouTube(video_link)

            video = yt.streams.filter(only_audio=True).first()
            console.info(f"Başlık: {yt.title}")

            down = video.download(output_path="Sesler")
            base, extension = os.path.splitext(down)

            new_file = base + '.mp3'
            original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

            ffmpeg_extract_audio(down, new_file)
            os.remove(down)

            sys.stdout = original_stdout
            console.success(f"{yt.streams[0].title} 'Sesler' klasörüne kayıt edildi.")
        except Exception as e:
            console.error(e)
    
    def down_play_video(self) -> None:
        playlist = console.question("Youtube playlist link: ")
        print()
        pl = Playlist(playlist)

        for video_url in pl.video_urls:
            self.down_video(video_url)

    def down_play_mp3(self) -> None:
        playlist = console.question("Youtube playlist link: ")
        print()
        pl = Playlist(playlist)

        for video_url in pl.video_urls:
            self.down_mp3(video_url)

class Console(object):
    def __init__(self) -> None:
        self.colors()

    def colors(self) -> None:
        self.red       = Fore.RED + Style.BRIGHT
        self.blue      = Fore.BLUE + Style.BRIGHT
        self.green     = Fore.GREEN + Style.BRIGHT
        self.yellow    = Fore.YELLOW + Style.BRIGHT
        self.magenta   = Fore.MAGENTA + Style.BRIGHT
        self.white     = Fore.WHITE    + Style.BRIGHT

    def print_logo(self) -> None:
        print(fr"""
{self.white}__________        ___________   {self.yellow}___.                  
{self.white}\______   \___.__.\__    ___/_ _{self.yellow}\_ |__   ____   ____  
{self.white} |     ___<   |  |  |    | |  |  {self.yellow}\ __ \_/ __ \_/ __ \ 
{self.white} |    |    \___  |  |    | |  |  {self.yellow}/ \_\ \  ___/\  ___/ 
{self.white} |____|    / ____|  |____| |____/{self.yellow}|___  /\___  >\___  >
{self.white}           \/                    {self.yellow}    \/     \/     \/
              
    {self.yellow}1.{self.white} Youtube videosu indir
    {self.yellow}2.{self.white} Youtube'dan MP3 indir
    {self.yellow}3.{self.white} Youtube Playlist'inden video indir
    {self.yellow}4.{self.white} Youtube Playlist'inden MP3 indir
              
        {self.white}""")

    def info(self, message) -> None:
        print(f" {self.blue}[*]{self.white} {message}")

    def success(self, message) -> None:
        print(f" {self.green}[+]{self.white} {message}")

    def error(self, message) -> None:
        print(f"\n{self.yellow}[!]{self.white} {message}")

    def question(self, message):
        print(f"{self.green} {message} {self.white}", end="")
        return input()

if __name__ == "__main__":
    try:
        console = Console()
        down = Downloader()

        while True:
            console.print_logo()
            
            #try:
            choice = int(console.question("Seçiminiz [1/2/3/4]:"))

            if choice == 1   :   down.down_video()
            elif choice == 2 :   down.down_mp3()
            elif choice == 3 :   down.down_play_video()
            elif choice == 4 :   down.down_play_mp3()

            print(f"\n{console.white}Devam etmek için [{console.green}Enter{console.white}]'a basın...", end="")
            input()

            #except ValueError:
            #    color.error("Geçersiz karakter girildi")
    except KeyboardInterrupt:
        sys.exit()