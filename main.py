#!/usr/bin/env python
# coding: utf-8

# TODO: look into how to give credits; for now:
# inspired by https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/python/console

import platform
import tkinter as tk
from collections import OrderedDict

from PIL import ImageTk, Image

import intent_sample
import speech_sample
import speech_synthesis_sample
import translation_sample

eofkey = 'Ctrl-Z' if "Windows" == platform.system() else 'Ctrl-D'

samples = OrderedDict([
    (speech_sample, [
        speech_sample.speech_recognize_once_from_mic,
        speech_sample.speech_recognize_once_from_file,
        speech_sample.speech_recognize_once_from_file_with_customized_model,
        speech_sample.speech_recognize_once_from_file_with_custom_endpoint_parameters,
        speech_sample.speech_recognize_async_from_file,
        speech_sample.speech_recognize_continuous_from_file,
        speech_sample.speech_recognition_with_pull_stream,
        speech_sample.speech_recognition_with_push_stream,
        speech_sample.speech_recognize_keyword_from_microphone,
    ]), (intent_sample, [
        intent_sample.recognize_intent_once_from_mic,
        intent_sample.recognize_intent_once_async_from_mic,
    ]), (translation_sample, [
        translation_sample.translation_once_from_mic,
        translation_sample.translation_once_from_file,
        translation_sample.translation_continuous,
    ]), (speech_synthesis_sample, [
        speech_synthesis_sample.speech_synthesis_to_speaker,
        speech_synthesis_sample.speech_synthesis_with_language,
        speech_synthesis_sample.speech_synthesis_with_voice,
        speech_synthesis_sample.speech_synthesis_to_wave_file,
        speech_synthesis_sample.speech_synthesis_to_mp3_file,
        speech_synthesis_sample.speech_synthesis_to_pull_audio_output_stream,
        speech_synthesis_sample.speech_synthesis_to_push_audio_output_stream,
        speech_synthesis_sample.speech_synthesis_to_result,
        speech_synthesis_sample.speech_synthesis_to_audio_data_stream,
        speech_synthesis_sample.speech_synthesis_events,
        speech_synthesis_sample.speech_synthesis_word_boundary_event,
    ])
])


def select():
    print('select sample module, {} to abort'.format(eofkey))
    modules = list(samples.keys())
    for i, module in enumerate(modules):
        print("{}: {}\n\t{}".format(i, module.__name__, module.__doc__.strip()))

    try:
        num = int(input())
        selected_module = modules[num]
    except EOFError:
        raise
    except Exception as e:
        print(e)
        return

    print('select sample function, {} to abort'.format(eofkey))
    for i, fun in enumerate(samples[selected_module]):
        print("{}: {}\n\t{}".format(i, fun.__name__, fun.__doc__))

    try:
        num = int(input())
        selected_function = samples[selected_module][num]
    except EOFError:
        raise
    except Exception as e:
        print(e)
        return

    print('You selected: {}'.format(selected_function))
    try:
        selected_function()
    except Exception as e:
        print('Error running sample: {}'.format(e))

    print()


def pack_buttons(buttons=None):
    if buttons is None:
        buttons = []

    for b in buttons:
        b.pack()
    pass


def start_gui():
    root = tk.Tk()
    # img = ImageTk.PhotoImage(Image.open(z))
    frame2 = tk.PhotoImage(file="True1.gif", format="gif -index 2")

    gui = tk.Label(root, image=frame2)

    def start_cmd():
        print("start_cmd")
        intent_sample.recognize_intent_once_from_mic()

    gui_buttons = [
        # tk.Button(master=gui, text="Stop", width=5, command=gui.destroy),
        tk.Button(master=gui, text="Give command", width=10, command=start_cmd)
    ]

    pack_buttons(buttons=gui_buttons)
    gui.pack(side="bottom", fill="both", expand="yes")
    cmd_btn = gui_buttons[0]
    cmd_btn.focus_set()
    gui.mainloop()


if __name__ == '__main__':
    start_gui()

    # while True:
    #     try:
    #         select()
    #     except EOFError:
    #         break
