import os
from twitchio.ext import commands
from random import randrange
import tkinter
import cv2
import time
import PIL.Image, PIL.ImageTk
from multiprocessing import Process, Pipe, Queue

## .ENV variables
# TMI_TOKEN => Twitch App Client Secret
# CLIENT_ID => Twitch App Client ID
# BOT_NICK => Name of account bot is hosted on
# BOT_PREFIX => The character/text that signifies the start of a command
# initial_channels => The channels that the bot will be active on
# SLEEP_STATE_1 => Image that represents complete dormant stationary state
# SLEEP_STATE_2 => Image that represents semi-dormant stationary state
# SLEEP_STATE_3 => Image that represents complete active stationary state


# Signifies certain animations must occur on next cycle
Event_Flag = None
viewer_count = 0

# State Machine global variables
frameInSequence = 0
sequence = 0

# magic variables
activeFrame = os.environ['SLEEP_STATE_1']

# Create a window
window = tkinter.Tk()

# Creates a numpy array from image
cv_img = cv2.cvtColor(cv2.imread(activeFrame, cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGBA)
# Get the image dimensions (OpenCV stores image data as NumPy ndarray)
height, width, no_channels = cv_img.shape
# Create a canvas that can fit the above image
canvas = tkinter.Canvas(window, width = width, height = height)
canvas.pack()
# Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
# Add a PhotoImage to the Canvas
image_container = canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

# Overlay Animation
def animation_thread(out_queue):
    global window

    # Updates frame before window loop completion
    def update_frame():
        global window
        window.update_idletasks()
        window.update()

    # Adds new image to canvas
    def addImage():
        global activeFrame, canvas, photo
        cv_img = cv2.cvtColor(cv2.imread(activeFrame, cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGBA)
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
        # Add a PhotoImage to the Canvas
        canvas.itemconfig(image_container,image=photo)

    # Blinking animation between SLEEP_STATE_1 and SLEEP_STATE_3
    def sequence1():
        global frameInSequence, activeFrame, canvas

        if frameInSequence == 0:
            frameInSequence = 1
            # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
            cv_img1 = cv2.cvtColor(cv2.imread(os.environ['SLEEP_STATE_3'], cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGBA)
            photo1 = PIL.Image.fromarray(cv_img1)
            # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
            cv_img2 = cv2.cvtColor(cv2.imread(os.environ['SLEEP_STATE_1'], cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGBA)
            photo2 = PIL.Image.fromarray(cv_img2)
            alpha = 0
            # Establishes a fade transition
            while 1.0 > alpha:
                new_img = PIL.Image.blend(photo2,photo1,alpha)
                photo = PIL.ImageTk.PhotoImage(image = new_img)
                alpha = alpha + 0.15
                time.sleep(0.02)
                canvas.itemconfig(image_container,image=photo)
                update_frame()
            window.after(0, sequence1)
            return
        elif frameInSequence == 1:
            frameInSequence = 2
            activeFrame = os.environ['SLEEP_STATE_2']
            window.after(0, addImage)
            window.after(randrange(50, 300), sequence1)
            return
        elif frameInSequence == 2:
            frameInSequence = 3
            activeFrame = os.environ['SLEEP_STATE_3']
            window.after(0, addImage)
            window.after(randrange(50, 300), sequence1)
            return
        elif frameInSequence == 3:
            frameInSequence = 4
            activeFrame = os.environ['SLEEP_STATE_2']
            window.after(0, addImage)
            window.after(randrange(50, 300), sequence1)
            return
        elif frameInSequence == 4:
            frameInSequence = 5
            activeFrame = os.environ['SLEEP_STATE_3']
            window.after(0, addImage)
            window.after(randrange(50, 300), sequence1)
            return
        elif frameInSequence == 5:
            frameInSequence = 6
            activeFrame = os.environ['SLEEP_STATE_2']
            window.after(0, addImage)
            window.after(randrange(50, 300), sequence1)
            return
        elif frameInSequence == 6:
            frameInSequence = 7
            activeFrame = os.environ['SLEEP_STATE_3']
            window.after(0, addImage)
            window.after(2000, sequence1)
            return
        elif frameInSequence == 7:
            frameInSequence = 8
            # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
            cv_img1 = cv2.cvtColor(cv2.imread(os.environ['SLEEP_STATE_3'], cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGBA)
            photo1 = PIL.Image.fromarray(cv_img1)
            # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
            cv_img2 = cv2.cvtColor(cv2.imread(os.environ['SLEEP_STATE_2'], cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGBA)
            photo2 = PIL.Image.fromarray(cv_img2)
            alpha = 0
            # Establishes a fade transition
            while 1.0 > alpha:
                new_img = PIL.Image.blend(photo1,photo2,alpha)
                photo = PIL.ImageTk.PhotoImage(image = new_img)
                alpha = alpha + 0.01
                time.sleep(0.04)
                canvas.itemconfig(image_container,image=photo)
                update_frame()
            window.after(0, sequence1)
            return
        elif frameInSequence == 8:
            frameInSequence = 0
            sequence = 0
            # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
            cv_img1 = cv2.cvtColor(cv2.imread(os.environ['SLEEP_STATE_2'], cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGBA)
            photo1 = PIL.Image.fromarray(cv_img1)
            # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
            cv_img2 = cv2.cvtColor(cv2.imread(os.environ['SLEEP_STATE_1'], cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGBA)
            photo2 = PIL.Image.fromarray(cv_img2)
            alpha = 0
            # Establishes a fade transition
            while 1.0 > alpha:
                new_img = PIL.Image.blend(photo1,photo2,alpha)
                photo = PIL.ImageTk.PhotoImage(image = new_img)
                alpha = alpha + 0.01
                time.sleep(0.03)
                canvas.itemconfig(image_container,image=photo)
                update_frame()
            # Updates image as current photo will be distroyed on function completion
            activeFrame = os.environ['SLEEP_STATE_1']
            window.after(0, addImage)
            window.after(3000, trySequence)
            return

    # Determines next animation sequence to take
    def trySequence():
        global sequence, Event_Flag
        sequenceChance = randrange(20) + 1
        if not out_queue.empty():
            Event_Flag = out_queue.get()
        if Event_Flag == "NewViewerEvent" or sequenceChance == 20:
            Event_Flag = None
            sequence = 1
            print("Sleepyhead is blinking (~_~ )Zzzzz")
            window.after(0, sequence1)
            return
        else:
            # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
            cv_img1 = cv2.cvtColor(cv2.imread(os.environ['SLEEP_STATE_2'], cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGBA)
            photo1 = PIL.Image.fromarray(cv_img1)
            # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
            cv_img2 = cv2.cvtColor(cv2.imread(os.environ['SLEEP_STATE_1'], cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGBA)
            photo2 = PIL.Image.fromarray(cv_img2)
            alpha = 0
            # Establishes a fade transition
            while 1.0 > alpha:
                new_img = PIL.Image.blend(photo2,photo1,alpha)
                photo = PIL.ImageTk.PhotoImage(image = new_img)
                alpha = alpha + 0.01
                canvas.itemconfig(image_container,image=photo)
                update_frame()
                time.sleep(0.03)
            alpha = 0
            # Establishes a fade transition
            while 1.0 > alpha:
                new_img = PIL.Image.blend(photo1,photo2,alpha)
                photo = PIL.ImageTk.PhotoImage(image = new_img)
                alpha = alpha + 0.01
                canvas.itemconfig(image_container,image=photo)
                update_frame()
                time.sleep(0.03)
            # Updates image as current photo will be distroyed on function completion
            activeFrame = os.environ['SLEEP_STATE_1']
            window.after(0, addImage)
            window.after(3000, trySequence)
            return

    # Begins fade in/out primary loop
    window.after(5000, trySequence)
    # Begins event loop
    window.mainloop()

# Twitch inteactions
def bot_thread(in_queue):
    # set up the bot
    bot = commands.Bot(
        token=os.environ['TMI_TOKEN'],
        client_id=os.environ['CLIENT_ID'],
        nick=os.environ['BOT_NICK'],
        prefix=os.environ['BOT_PREFIX'],
        initial_channels=[os.environ['CHANNEL']]
    )
    ## Establishes bot commands
    # Listens for new viewers
    @bot.event()
    async def event_join(channel, user):
        print("Someone New!")
        in_queue.put_nowait("NewViewerEvent")

    # Sends message response to "test"
    @bot.command(name='test')
    async def test(ctx):
        print("Responding to user")
        await ctx.send('test passed!')

    # Updates state flag in response to "wakeup"
    @bot.command(name='wakeup')
    async def wakeup(ctx):
        print("Someone wants me to wake up...")
        in_queue.put_nowait("NewViewerEvent")

    # Begins event loop
    bot.run()

# Establishes bot connection on file exicution
if __name__ == "__main__":
    event_queue = Queue()
    bot_process = Process(target=bot_thread, args=(event_queue,))
    animation_process = Process(target=animation_thread, args=(event_queue,))
    bot_process.start()
    animation_process.start()

#@bot.event
#async def event_ready():
#    'Called once when the bot goes online.'
#    print(f"{os.environ['BOT_NICK']} is online!")
#    ws = bot._ws  # this is only needed to send messages within event_ready
#    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")
#
#
#@bot.event
#async def event_message(ctx):
#    'Runs every time a message is sent in chat.'
#
#    # make sure the bot ignores itself and the streamer
#    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
#        return
#
#    await bot.handle_commands(ctx)
#
#    # await ctx.channel.send(ctx.content)
#
#    if 'hello' in ctx.content.lower():
#        await ctx.channel.send(f"Hi, @{ctx.author.name}!")
