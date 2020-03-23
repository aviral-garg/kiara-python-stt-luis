#!/usr/bin/env python
# coding: utf-8

"""
Intent recognition for the Microsoft Cognitive Services Speech SDK
"""

import time

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys

    sys.exit(1)

# Subscription info for the Language Understanding Service (not Speech Service).
luis_prediction_subscription_key = "009a7d0fe55a44c1a59e5fe8835cde05"
luis_service_region = "westus"  # usually westus
luis_app_id = "17f95c54-4c57-4c3f-8c6c-157edd83b345"


def recognize_intent_once_from_mic():
    """performs one-shot intent recognition from input from the default microphone"""
    # <IntentRecognitionOnceWithMic>

    # Set up the config for the intent recognizer (Language Understanding key, not the Speech Services key)!
    luis_config = speechsdk.SpeechConfig(subscription=luis_prediction_subscription_key, region=luis_service_region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Set up the intent recognizer
    intent_recognizer = speechsdk.intent.IntentRecognizer(speech_config=luis_config, audio_config=audio_config)

    # Set up the intents that are to be recognized. These can be a mix of simple phrases and
    # intents specified through a LanguageUnderstanding Model.
    model = speechsdk.intent.LanguageUnderstandingModel(app_id=luis_app_id)
    # TODO: fill in the intents
    intents = [
        (model, "HomeAutomation.TurnOn"),
        (model, "HomeAutomation.TurnOff"),
        ("This is a test.", "test"),
        ("Switch to channel 34.", "34"),
        ("what's the weather like", "weather"),
    ]
    intent_recognizer.add_intents(intents)

    # Starts intent recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    intent_result = intent_recognizer.recognize_once()

    # Check the results
    if intent_result.reason == speechsdk.ResultReason.RecognizedIntent:
        print("Recognized: \"{}\" with intent id `{}`".format(intent_result.text, intent_result.intent_id))
    elif intent_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(intent_result.text))
    elif intent_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(intent_result.no_match_details))
    elif intent_result.reason == speechsdk.ResultReason.Canceled:
        print("Intent recognition canceled: {}".format(intent_result.cancellation_details.reason))
        if intent_result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(intent_result.cancellation_details.error_details))
    # </IntentRecognitionOnceWithMic>


def recognize_intent_once_async_from_mic():
    """performs one-shot asynchronous intent recognition from input from the default microphone"""
    # Set up the config for the intent recognizer
    intent_config = speechsdk.SpeechConfig(subscription=luis_prediction_subscription_key,
                                           region=luis_service_region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Set up the intent recognizer
    intent_recognizer = speechsdk.intent.IntentRecognizer(speech_config=intent_config, audio_config=audio_config)

    # Add callbacks to the recognition events

    # Set up a flag to mark when asynchronous recognition is done
    done = False

    def recognized_callback(evt):
        """
        Callback that is called on successful recognition of a full utterance by both speech
        processing and intent classification
        """
        result = evt.result
        print("Recognized: \"{}\" with intent id `{}`".format(result.text, result.intent_id))
        nonlocal done
        done = True

    def canceled_callback(evt):
        """Callback that is called on a failure by either speech or language processing"""
        result = evt.result
        print("Intent recognition canceled: {}".format(result.cancellation_details.reason))
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(result.cancellation_details.error_details))
        nonlocal done
        done = True

    def recognizing_callback(evt):
        """Callback that is called on intermediate results from speech transcription"""
        result = evt.result
        print("Intermediate transcription: \"{}\"".format(result.text))

    # Connect the callbacks
    intent_recognizer.recognized.connect(recognized_callback)
    intent_recognizer.canceled.connect(canceled_callback)
    intent_recognizer.recognizing.connect(recognizing_callback)

    # set up the intents that are to be recognized. These can be a mix of simple phrases and
    # intents specified through a LanguageUnderstanding Model.
    model = speechsdk.intent.LanguageUnderstandingModel(app_id=luis_app_id)
    intents = [
        (model, "HomeAutomation.TurnOn"),
        (model, "HomeAutomation.TurnOff"),
        ("This is a test.", "test"),
        ("Switch to channel 34.", "34"),
        ("what's the weather like", "weather"),
    ]
    intent_recognizer.add_intents(intents)

    # Starts non-blocking intent recognition and stop after a single utterance has been recognized.
    # The end of a single utterance is determined by listening for silence at the end or until a
    # maximum of 15 seconds of audio is processed.
    # Note: Since recognize_once() stops after a single utterance, it is suitable only for single
    # shot recognition like command or query. For long-running multi-utterance recognition, use
    # start_continuous_recognition() instead.
    intent_recognizer.recognize_once_async()

    # wait until recognition is complete
    while not done:
        time.sleep(1)
