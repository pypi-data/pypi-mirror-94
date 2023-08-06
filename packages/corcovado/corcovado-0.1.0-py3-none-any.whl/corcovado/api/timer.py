# import curses
# import os
# import re
# import unicodedata

# from datetime import datetime
# from datetime import timedelta
# from functools import wraps
# from math import ceil
# from os.path import abspath
# from os.path import dirname
# from queue import Empty
# from queue import Queue
# from subprocess import DEVNULL
# from subprocess import STDOUT
# from subprocess import Popen
# from sys import exit
# from sys import stderr
# from sys import stdout
# from threading import Event
# from threading import Lock
# from threading import Thread
# from time import sleep

# import click

# from dateutil import tz
# from dateutil.parser import parse
# from pyfiglet import CharNotPrinted
# from pyfiglet import Figlet

# DEFAULT_FONT = "univers"
# DEFAULT_TIME_FORMAT = "%H:%M:%S"  # --no-seconds expects this to end with :%S
# TIMEDELTA_REGEX = re.compile(
#     r"((?P<years>\d+)y ?)?"
#     r"((?P<days>\d+)d ?)?"
#     r"((?P<hours>\d+)h ?)?"
#     r"((?P<minutes>\d+)m ?)?"
#     r"((?P<seconds>\d+)s ?)?"
# )
# INPUT_PAUSE = 1
# INPUT_RESET = 2
# INPUT_EXIT = 3
# INPUT_LAP = 4
# INPUT_PLUS = 5
# INPUT_MINUS = 6


# def setup(stdscr):
#     # curses
#     curses.use_default_colors()
#     curses.init_pair(1, curses.COLOR_RED, -1)
#     curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
#     curses.init_pair(3, curses.COLOR_GREEN, -1)
#     curses.init_pair(4, -1, curses.COLOR_RED)
#     try:
#         curses.curs_set(False)
#     except curses.error:
#         # fails on some terminals
#         pass
#     stdscr.timeout(0)

#     # prepare input thread mechanisms
#     curses_lock = Lock()
#     input_queue = Queue()
#     quit_event = Event()
#     return (curses_lock, input_queue, quit_event)


# def draw_text(stdscr, text, color=0, fallback=None, title=None, no_figlet_y_offset=-1):
#     """
#     Draws text in the given color. Duh.
#     """
#     if fallback is None:
#         fallback = text
#     y, x = stdscr.getmaxyx()
#     effective_y = y if no_figlet_y_offset < 0 else 1
#     y_delta = 0 if no_figlet_y_offset < 0 else no_figlet_y_offset
#     if title:
#         title = pad_to_size(title, x, 1)
#         if "\n" in title.rstrip("\n"):
#             # hack to get more spacing between title and body for figlet
#             title += "\n" * 5
#         text = title + "\n" + pad_to_size(text, x, len(text.split("\n")))
#     lines = pad_to_size(text, x, effective_y).rstrip("\n").split("\n")

#     try:
#         for i, line in enumerate(lines):
#             stdscr.insstr(i + y_delta, 0, line, curses.color_pair(color))
#     except:
#         lines = pad_to_size(fallback, x, effective_y).rstrip("\n").split("\n")
#         try:
#             for i, line in enumerate(lines[:]):
#                 stdscr.insstr(i + y_delta, 0, line, curses.color_pair(color))
#         except:
#             pass
#     stdscr.refresh()


# def format_seconds(seconds, hide_seconds=False):
#     """
#     Returns a human-readable string representation of the given amount
#     of seconds.
#     """
#     if seconds <= 60:
#         return str(seconds)
#     output = ""
#     for period, period_seconds in (
#         ("y", 31557600),
#         ("d", 86400),
#         ("h", 3600),
#         ("m", 60),
#         ("s", 1),
#     ):
#         if seconds >= period_seconds and not (hide_seconds and period == "s"):
#             output += str(int(seconds / period_seconds))
#             output += period
#             output += " "
#             seconds = seconds % period_seconds
#     return output.strip()


# def format_seconds_alt(seconds, start, hide_seconds=False):
#     # make sure we always show at least 00:00:00
#     start = max(start, 86400)
#     output = ""
#     total_seconds = seconds
#     for period_seconds in (
#         31557600,
#         86400,
#         3600,
#         60,
#         1,
#     ):
#         if hide_seconds and period_seconds == 1 and total_seconds > 60:
#             break
#         actual_period_value = int(seconds / period_seconds)
#         if actual_period_value > 0:
#             output += str(actual_period_value).zfill(2) + ":"
#         elif start > period_seconds or total_seconds > period_seconds:
#             output += "00:"
#         seconds = seconds % period_seconds
#     return output.rstrip(":")


# def graceful_ctrlc(func):
#     """
#     Makes the decorated function exit with code 1 on CTRL+C.
#     """

#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except KeyboardInterrupt:
#             exit(1)

#     return wrapper


# NORMALIZE_TEXT_MAP = {
#     "ä": "ae",
#     "Ä": "Ae",
#     "ö": "oe",
#     "Ö": "Oe",
#     "ü": "ue",
#     "Ü": "Ue",
#     "ß": "ss",
# }


# def normalize_text(input_str):
#     for char, replacement in NORMALIZE_TEXT_MAP.items():
#         input_str = input_str.replace(char, replacement)
#     return "".join([c for c in unicodedata.normalize("NFD", input_str) if unicodedata.category(c) != "Mn"])


# def pad_to_size(text, x, y):
#     """
#     Adds whitespace to text to center it within a frame of the given
#     dimensions.
#     """
#     input_lines = text.rstrip().split("\n")
#     longest_input_line = max(map(len, input_lines))
#     number_of_input_lines = len(input_lines)
#     x = max(x, longest_input_line)
#     y = max(y, number_of_input_lines)
#     output = ""

#     padding_top = int((y - number_of_input_lines) / 2)
#     padding_bottom = y - number_of_input_lines - padding_top
#     padding_left = int((x - longest_input_line) / 2)

#     output += (
#         (" " * x + "\n")
#         + ((" " * int(x / 2)) + "Repetition" + "\n")
#         + ((" " * int(x / 2)) + "Set" + "\n")
#         + (" " * x + "\n")
#     )
#     for line in input_lines:
#         output += padding_left * " " + line + " " * (x - padding_left - len(line)) + "\n"
#     output += padding_bottom * (" " * x + "\n")

#     return output


# def parse_timestr(timestr):
#     """
#     Parse a string describing a point in time.
#     """
#     timedelta_secs = parse_timedelta(timestr)
#     sync_start = datetime.now()

#     if timedelta_secs:
#         target = datetime.now() + timedelta(seconds=timedelta_secs)
#     elif timestr.isdigit():
#         target = datetime.now() + timedelta(seconds=int(timestr))
#     else:
#         try:
#             target = parse(timestr)
#         except:
#             # unfortunately, dateutil doesn't raise the best exceptions
#             raise ValueError("Unable to parse '{}'".format(timestr))

#         # When I do "termdown 10" (the two cases above), I want a
#         # countdown for the next 10 seconds. Okay. But when I do
#         # "termdown 23:52", I want a countdown that ends at that exact
#         # moment -- the countdown is related to real time. Thus, I want
#         # my frames to be drawn at full seconds, so I enforce
#         # microsecond=0.
#         sync_start = sync_start.replace(microsecond=0)
#     try:
#         # try to convert target to naive local timezone
#         target = target.astimezone(tz=tz.tzlocal()).replace(tzinfo=None)
#     except ValueError:
#         # parse() already returned a naive datetime, all is well
#         pass
#     return (sync_start, target)


# def parse_timedelta(deltastr):
#     """
#     Parse a string describing a period of time.
#     """
#     matches = TIMEDELTA_REGEX.match(deltastr)
#     if not matches:
#         return None
#     components = {}
#     for name, value in matches.groupdict().items():
#         if value:
#             components[name] = int(value)
#     for period, hours in (("days", 24), ("years", 8766)):
#         if period in components:
#             components["hours"] = components.get("hours", 0) + components[period] * hours
#             del components[period]
#     return int(timedelta(**components).total_seconds())


# def print_version(ctx, param, value):
#     if not value or ctx.resilient_parsing:
#         return
#     click.echo(VERSION)
#     ctx.exit()


# def verify_outfile(ctx, param, value):
#     if value:
#         if os.path.exists(value):
#             raise click.BadParameter("File already exists: {}".format(value))
#         if not os.access(dirname(abspath(value)), os.W_OK):
#             raise click.BadParameter("Unable to write file: {}".format(value))
#     return value


# @graceful_ctrlc
# def countdown(
#     stdscr,
#     alt_format=False,
#     font=DEFAULT_FONT,
#     blink=False,
#     critical=3,
#     quit_after=None,
#     text=None,
#     timespec=None,
#     title=None,
#     voice=None,
#     voice_prefix=None,
#     exec_cmd=None,
#     outfile=None,
#     no_bell=False,
#     no_seconds=False,
#     no_text_magic=True,
#     no_figlet=False,
#     no_figlet_y_offset=-1,
#     no_window_title=False,
#     time=False,
#     time_format=None,
#     **kwargs
# ):
#     try:
#         sync_start, target = parse_timestr(timespec)
#     except ValueError:
#         raise click.BadParameter("Unable to parse TIME value '{}'".format(timespec))
#     curses_lock, input_queue, quit_event = setup(stdscr)
#     figlet = Figlet(font=font)
#     if not no_figlet:
#         no_figlet_y_offset = -1

#     if title and not no_figlet:
#         try:
#             title = figlet.renderText(title)
#         except CharNotPrinted:
#             title = ""

#     voice_cmd = None
#     if voice:
#         for cmd in ("/usr/bin/say", "/usr/bin/espeak", "/usr/bin/espeak-ng"):
#             if os.path.exists(cmd):
#                 voice_cmd = cmd
#                 break
#     if voice or exec_cmd:
#         voice_prefix = voice_prefix or ""

#     input_thread = Thread(
#         args=(stdscr, input_queue, quit_event, curses_lock),
#         target=input_thread_body,
#     )
#     input_thread.start()

#     seconds_total = seconds_left = int(ceil((target - datetime.now()).total_seconds()))

#     try:
#         while seconds_left >= 0 or blink or text:
#             figlet.width = stdscr.getmaxyx()[1]
#             if time:
#                 countdown_text = datetime.now().strftime(time_format)
#             elif alt_format:
#                 countdown_text = format_seconds_alt(seconds_left, seconds_total, hide_seconds=no_seconds)
#             else:
#                 countdown_text = format_seconds(seconds_left, hide_seconds=no_seconds)
#             if seconds_left >= 0:
#                 with curses_lock:
#                     if not no_window_title:
#                         os.write(stdout.fileno(), "\033]2;{0}\007".format(countdown_text).encode())
#                     if outfile:
#                         with open(outfile, "w") as f:
#                             f.write("{}\n{}\n".format(countdown_text, seconds_left))
#                     stdscr.erase()
#                     try:
#                         draw_text(
#                             stdscr,
#                             countdown_text if no_figlet else figlet.renderText(countdown_text),
#                             color=1 if seconds_left <= critical else 0,
#                             fallback=title + "\n" + countdown_text if title else countdown_text,
#                             title=title,
#                             no_figlet_y_offset=no_figlet_y_offset,
#                         )
#                     except CharNotPrinted:
#                         draw_text(stdscr, "E")
#             annunciation = None
#             if seconds_left <= critical:
#                 annunciation = str(seconds_left)
#             elif seconds_left in (5, 10, 20, 30, 60):
#                 annunciation = "{} {} seconds".format(voice_prefix, seconds_left)
#             elif seconds_left in (300, 600, 1800):
#                 annunciation = "{} {} minutes".format(voice_prefix, int(seconds_left / 60))
#             elif seconds_left == 3600:
#                 annunciation = "{} one hour".format(voice_prefix)
#             if annunciation or exec_cmd:
#                 if exec_cmd:
#                     Popen(
#                         exec_cmd.format(seconds_left, annunciation or ""),
#                         stdout=DEVNULL,
#                         stderr=STDOUT,
#                         shell=True,
#                     )

#                 if voice_cmd:
#                     Popen(
#                         [voice_cmd, "-v", voice, annunciation.strip()],
#                         stdout=DEVNULL,
#                         stderr=STDOUT,
#                     )

#             # We want to sleep until this point of time has been
#             # reached:
#             sleep_target = sync_start + timedelta(seconds=1)
#             if time:
#                 sleep_target = sleep_target.replace(microsecond=0)

#             # If sync_start has microsecond=0, it might happen that we
#             # need to skip one frame (the very first one). This occurs
#             # when the program has been startet at, say,
#             # "2014-05-29 20:27:57.930651". Now suppose rendering the
#             # frame took about 0.2 seconds. The real time now is
#             # "2014-05-29 20:27:58.130000" and sleep_target is
#             # "2014-05-29 20:27:58.000000" which is in the past! We're
#             # already too late. We could either skip that frame
#             # completely or we can draw it right now. I chose to do the
#             # latter: Only sleep if haven't already missed our target.
#             now = datetime.now()
#             if sleep_target > now and seconds_left > 0:
#                 try:
#                     input_action = input_queue.get(True, (sleep_target - now).total_seconds())
#                 except Empty:
#                     input_action = None
#                 if input_action == INPUT_PAUSE:
#                     pause_start = datetime.now()
#                     with curses_lock:
#                         stdscr.erase()
#                         try:
#                             draw_text(
#                                 stdscr,
#                                 countdown_text if no_figlet else figlet.renderText(countdown_text),
#                                 color=3,
#                                 fallback=countdown_text,
#                                 title=title,
#                                 no_figlet_y_offset=no_figlet_y_offset,
#                             )
#                         except CharNotPrinted:
#                             draw_text(stdscr, "E")
#                     input_action = input_queue.get()
#                     if input_action == INPUT_PAUSE:
#                         time_paused = datetime.now() - pause_start
#                         sync_start += time_paused
#                         target += time_paused
#                 if input_action == INPUT_EXIT:  # no elif here! input_action may have changed
#                     break
#                 elif input_action == INPUT_RESET:
#                     sync_start, target = parse_timestr(timespec)
#                     seconds_left = int(ceil((target - datetime.now()).total_seconds()))
#                     continue
#                 elif input_action == INPUT_PLUS:
#                     target += timedelta(seconds=10)
#                 elif input_action == INPUT_MINUS:
#                     target -= timedelta(seconds=10)
#                 elif input_action == INPUT_LAP:
#                     continue

#             sync_start = sleep_target

#             seconds_left = int(ceil((target - datetime.now()).total_seconds()))

#             if seconds_left < 0:
#                 # we could write this entire block outside the parent while
#                 # but that would leave us unable to reset everything

#                 if not no_bell:
#                     with curses_lock:
#                         curses.beep()

#                 if text and not no_text_magic:
#                     text = normalize_text(text)

#                 if outfile:
#                     with open(outfile, "w") as f:
#                         f.write("{}\n{}\n".format(text if text else "DONE", 0))

#                 rendered_text = text

#                 if text and not no_figlet:
#                     try:
#                         rendered_text = figlet.renderText(text)
#                     except CharNotPrinted:
#                         rendered_text = ""

#                 if blink or text:
#                     base_color = 1 if blink else 0
#                     blink_reset = False
#                     flip = True
#                     slept = 0
#                     extra_sleep = 0
#                     while True:
#                         with curses_lock:
#                             os.write(stdout.fileno(), "\033]2;{0}\007".format("/" if flip else "\\").encode())
#                             if text:
#                                 draw_text(
#                                     stdscr,
#                                     rendered_text,
#                                     color=base_color if flip else 4,
#                                     fallback=text,
#                                     no_figlet_y_offset=no_figlet_y_offset,
#                                 )
#                             else:
#                                 draw_text(stdscr, "", color=base_color if flip else 4)
#                         if blink:
#                             flip = not flip
#                         try:
#                             sleep_start = datetime.now()
#                             input_action = input_queue.get(True, 0.5 + extra_sleep)
#                         except Empty:
#                             input_action = None
#                         finally:
#                             extra_sleep = 0
#                             sleep_end = datetime.now()
#                         if input_action == INPUT_PAUSE:
#                             pause_start = datetime.now()
#                             input_action = input_queue.get()
#                             extra_sleep = (sleep_end - sleep_start).total_seconds()
#                         if input_action == INPUT_EXIT:
#                             # no elif here! input_action may have changed
#                             return
#                         elif input_action == INPUT_RESET:
#                             sync_start, target = parse_timestr(timespec)
#                             seconds_left = int(ceil((target - datetime.now()).total_seconds()))
#                             blink_reset = True
#                             break
#                         slept += (sleep_end - sleep_start).total_seconds()
#                         if quit_after and slept >= float(quit_after):
#                             return
#                     if blink_reset:
#                         continue
#     finally:
#         with curses_lock:
#             if not no_window_title:
#                 os.write(stdout.fileno(), "\033]2;\007".encode())
#             if outfile:
#                 os.remove(outfile)
#         quit_event.set()
#         input_thread.join()


# def input_thread_body(stdscr, input_queue, quit_event, curses_lock):
#     while not quit_event.is_set():
#         try:
#             with curses_lock:
#                 key = stdscr.getkey()
#         except:
#             key = None
#         if key in ("q", "Q"):
#             input_queue.put(INPUT_EXIT)
#         elif key == " ":
#             input_queue.put(INPUT_PAUSE)
#         elif key in ("r", "R"):
#             input_queue.put(INPUT_RESET)
#         elif key in ("l", "L"):
#             input_queue.put(INPUT_LAP)
#         elif key == "+":
#             input_queue.put(INPUT_PLUS)
#         elif key == "-":
#             input_queue.put(INPUT_MINUS)
#         sleep(0.01)


# def start_countdown():
#     data = {
#         "timespec": str(4),
#         "alt_format": False,
#         "blink": False,
#         "no_bell": False,
#         "critical": 3,
#         "font": "univers",
#         "voice_prefix": None,
#         "quit_after": None,
#         "no_seconds": False,
#         "text": None,
#         "title": None,
#         "no_window_title": False,
#         "voice": None,
#         "outfile": None,
#         "exec_cmd": None,
#         "no_figlet": False,
#         "no_figlet_y_offset": -1,
#         "no_text_magic": False,
#         "time": False,
#         "time_format": None,
#     }
#     curses.wrapper(countdown, **data)
