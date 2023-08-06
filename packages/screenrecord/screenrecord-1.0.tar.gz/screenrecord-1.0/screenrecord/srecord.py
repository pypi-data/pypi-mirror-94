import imageio
import time
from PIL import Image
import argparse

# from pygifsicle import optimize
# from subprocess import run


def create_parser():
    parser = argparse.ArgumentParser(
        prog='record', description='Screen Recording with python')
    parser.add_argument("filename", type=str, default="test.gif",
                        help='filename can be mp4 or gif or mov')
    parser.add_argument("-i", "--initdelay", type=int, default=5,
                        help='Initial delay in seconds, default 5 s')
    parser.add_argument("-d", "--delay", type=float, default=0.5,
                        help='Delay between frames in seconds, default 0.5 s')
    parser.add_argument("-dur", "--duration", type=int,
                        default=20, help='Duration of capture, default 20 s')
    parser.add_argument("--bbox", type=int, nargs="+",
                        default=[0, 0, 800, 400], help='Bounding box, default (0, 0, 800, 400)')
    parser.add_argument("-f", "--fullscreen", action='store_true')

    return parser


def record(outfilename, initdelay=5, delay=0.1, duration=5, area=None):

    img = []
    time.sleep(initdelay)
    print("Started..\a")
    sc = imageio.get_reader('<screen>')
    t0 = time.time()
    while True:
        t1 = time.time()
        still = sc.get_next_data()
        if area:
            still = Image.fromarray(still).crop(area)
        img.append(still)
        t2 = time.time()
        time.sleep(abs(delay - (t2-t1)))
        if t2 - t0 > duration:
            break
    print("Ended..\a\a")
    imageio.mimsave(outfilename, img)
    # if outfilename.endswith('.gif'):
    #     optimize(outfilename, "optimized.gif")


def main():
    parser = create_parser()
    args = parser.parse_args()
    # print(args)

    area = args.bbox
    if args.fullscreen:
        area = None

    record(args.filename, initdelay=args.initdelay,
         duration=args.duration, delay=args.delay, area=area)


if __name__ == "__main__":
    main()
