import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()


def englishCalculate():
    english_sentence = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                        'm': 0,
                        'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0,
                        'z': 0}

    english_letter_count = 0
    for x in english_sentence_bank:
        for y in x:
            if y in english_sentence:
                english_sentence[y] += 1
                english_letter_count += 1

    for key in english_sentence:
        english_freq[key] = english_sentence[key] / english_letter_count


def spanishCalculate():
    spanish_sentence = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                        'm': 0,
                        'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0,
                        'z': 0}

    spanish_letter_count = 0
    for x in spanish_sentence_bank:
        for y in x:
            if y in spanish_sentence:
                spanish_sentence[y] += 1
                spanish_letter_count += 1

    for key in spanish_sentence:
        spanish_freq[key] = spanish_sentence[key] / spanish_letter_count


def incorrectHandler():
    if currPrediction == "This sentence is in English!":
        spanish_sentence_bank.append(currSentence)
        spanishCalculate()
        clear(T)
        add(T, "This has been added to the Spanish Dictionary")
    elif currPrediction == "This sentence is in Spanish!":
        english_sentence_bank.append(currSentence)
        englishCalculate()
        clear(T)
        add(T, "This has been added to the English Dictionary")


def correctHandler():
    if currPrediction == "This sentence is in Spanish!":
        spanish_sentence_bank.append(currSentence)
        spanishCalculate()
        clear(T)
        add(T, "This has been added to the Spanish Dictionary")
    elif currPrediction == "This sentence is in English!":
        english_sentence_bank.append(currSentence)
        englishCalculate()
        clear(T)
        add(T, "This has been added to the English Dictionary")

def Predict(sentence):
    word_sentence = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                     'm': 0,
                     'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0,
                     'z': 0}

    word_sentence_count = 0
    for x in sentence:
        if x in word_sentence:
            word_sentence[x] += 1
            word_sentence_count += 1

    for key in word_sentence:
        word_freq[key] = word_sentence[key] / word_sentence_count

    spanish_diff = 0
    english_diff = 0
    for key in word_freq:
        spanish_diff += abs(word_freq[key] - spanish_freq[key])
        english_diff += abs(word_freq[key] - english_freq[key])

    if spanish_diff < english_diff:
        return "This sentence is in Spanish!"
    elif english_diff < spanish_diff:
        return "This sentence is in English!"
    else:
        return "I couldn't decide what this was!"


def TrySentence():
    global currPrediction
    global currSentence
    # Exception handling to handle
    # exceptions at the runtime
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            currPrediction = Predict(MyText)
            currSentence = MyText
            clear(T)
            add(T, MyText)
            add(T, currPrediction)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occured")


def runTests():
    english = open('./englishSentences.txt', 'r')
    lines = english.readlines()

    englishCorrect = 0
    for line in lines:
        answer = Predict(line)
        if answer == "This sentence is in English!":
            englishCorrect += 1

    spanish = open('./spanishSentences.txt', 'r')
    lines = spanish.readlines()

    spanishCorrect = 0
    for line in lines:
        answer = Predict(line)
        if answer == "This sentence is in Spanish!":
            spanishCorrect += 1

    clear(T)
    add(T, "English is predicted correctly " + str(englishCorrect) + "% of the time")
    add(T, "Spanish is predicted correctly " + str(spanishCorrect) + "% of the time")


def clear(T):
    T.delete("1.0", "end")


def add(T, text):
    T.insert(tk.END, text + '\n')


root = ThemedTk(theme='yaru')

# specify size of window.
root.title("Language Predictor ML")
root.geometry("600x425")
T = tk.Text(root, height=5, width=52)
# Create label
l = ttk.Label(root, text="Language Predictor ML")
l.config(font=("Courier", 14))


text_box = """"""

l.pack()
T.pack()

# Insert The Fact.
T.insert(tk.END, text_box)

# Button Creation
incorrectButton = ttk.Button(root,
                       text="Incorrect",
                       command=incorrectHandler)
incorrectButton.pack()
incorrectButton.place(relx=.4, rely=.3, anchor='center')
correctButton = ttk.Button(root,
                       text="Correct",
                       command=correctHandler)
correctButton.pack()
correctButton.place(relx=.6, rely=.3, anchor='center')
predictButton = ttk.Button(root,
                         text="Predict",
                         command=TrySentence)
predictButton.pack()
predictButton.place(relx=.5, rely=.4, anchor='center')
runTestsButton = ttk.Button(root,
                         text="Run Tests",
                         command=runTests)
runTestsButton.pack()
runTestsButton.place(relx=.5, rely=.5, anchor='center')

root.resizable(False, False)
root.iconbitmap('./icon.ico')

spanish_sentence = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0,
                'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

english_sentence = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0,
                'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

word_sentence = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0,
                'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

spanish_freq = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0,
                'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

english_freq = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0,
                'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

word_freq = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0,
                'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

spanish_sentence_bank = ["porque un archivo comprimido desecha fotogramas, y necesito ver cada fotograma",
                         "se debe tener especial precaución cuando se retira y desecha la aguja",
                         "un hombre recoge lo que otro hombre desecha"]

english_sentence_bank = ["he was so preoccupied with whether or not he could that he failed to stop to consider if he should",
                         "kevin embraced his ability to be at the wrong place at the wrong time",
                         "the most exciting eureka moment ive had was when i realized that the instructions on food packets were just guidelines"]

currSentence = ""
currPrediction = ""

englishCalculate()

spanishCalculate()

tk.mainloop()
