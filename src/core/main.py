from core import Core


if __name__ == "__main__":
    Handler = Core()
    Handler.Handler('mkdir /home/tuuna/good_folder')
    Handler.Handler('rm /home/tuuna/level1')
    Handler.Handler('mkdir /home/tuuna/readme')
    Handler.Handler('ifconfig')
