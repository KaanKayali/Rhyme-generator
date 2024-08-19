# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font, PhotoImage
import re
import PyPDF2
import os
import json

class gui(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialize
        self.title("Rhyme generator")
        self.resizable(False, False)
        self.minsize(640, 360)

        #Variables
        self.userInput = ""
        self.filteredInput = ""
        self.selectedOption = ""
        self.loadFileName = "loadwords.txt"
        self.isLightModeOn = tk.BooleanVar(value=True)
        self.charsToAdd = "aeiouäüö1234567890"
        self.keypressTimer = None;

        # Fonts
        self.titleFont = font.Font(family="Comic Sans MS", size=18, weight="bold")
        self.copyrightFont = font.Font(family="Comic Sans MS", size=8)
        self.inputFont = font.Font(family="Comic Sans MS", size=12)
        self.listFont = font.Font(family="Comic Sans MS", size=10)
        self.comboboxFont = font.Font(family="Comic Sans MS", size=10)
        self.buttonFont = font.Font(family="Comic Sans MS", size=10)

        # Colors
        self.labelColor = "black"
        self.buttonColor = "gray85"
        self.backgroundColor = "gray95"
        self.textboxColor = "white"
        self.comboboxColor = "white"
        self.listboxColor = "white"
        self.checkboxColor = "black"

        # Images
        self.imagepath = "images/"
        self.imgSun = PhotoImage(file=self.imagepath + "sun.png")
        self.imgMoon = PhotoImage(file=self.imagepath + "moon.png")

        # Grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # Title
        self.titleLabel = tk.Label(self, text="Rhyme generator", font=self.titleFont, fg=self.labelColor)
        self.titleLabel.grid(column=0, row=0, sticky='wn', padx=8, pady=(18, 0))

        # Copyright
        self.copyrightLabel = tk.Label(self, text="Made by ©SohleKNKI", font=self.copyrightFont, fg=self.labelColor)
        self.copyrightLabel.grid(column=0, row=0, sticky='ws', padx=8, pady=(0, 6))

        # Textfield
        self.entry = tk.Entry(self, font=self.inputFont, fg=self.labelColor, bg=self.textboxColor)
        self.entry.bind("<KeyRelease>", self.onKeyreleased)
        self.entry.grid(column=0, row=1, sticky='new', padx=8)

        # Combobox
        self.combo = ttk.Combobox(self, values=["Vowel rhyme", "Vowel rhyme + consonant ending", "Classic rhyme"], font=self.comboboxFont)
        self.combo.config(state="readonly")
        self.combo.bind("<<ComboboxSelected>>", self.onComboSelected)
        self.combo.current(0)
        self.combo.grid(column=0, row=2, sticky='ew', padx=8)
        self.selectedOption = self.combo.get()

        # Checkbutton
        self.isPerfectRhyme = tk.BooleanVar(value=False)
        self.checkPerfectRhyme = tk.Checkbutton(self, text="Perfect rhymes", variable=self.isPerfectRhyme, command=self.reloadList)
        self.checkPerfectRhyme.grid(column=0, row=1, sticky='e', padx=8)

        # Additional words
        self.withAdditionalwords = tk.BooleanVar()
        self.checkWithAdditionalwords = tk.Checkbutton(self, text="Additional words", variable=self.withAdditionalwords, command=self.reloadList)
        self.checkWithAdditionalwords.grid(column=0, row=2, sticky='ne', padx=8)

        # Add list
        self.chooseFileButton = tk.Button(self, text="Add a list (txt/PDF)", command=self.chooseFile, font=self.buttonFont, fg=self.labelColor, bg=self.buttonColor)
        self.chooseFileButton.grid(column=1, row=0, sticky='w')

        # Toggle Lightmode button
        self.lightmodeButton = tk.Button(self, text="Lightmode", image=self.imgSun ,command=self.switchLightMode, font=self.buttonFont)
        self.lightmodeButton.grid(column=2, row=0, sticky='e', padx=(0, 8))

        # Delete list button
        self.deleteListButton = tk.Button(self, text="Delete list", command=self.deleteList, font=self.buttonFont, fg=self.labelColor, bg=self.buttonColor)
        self.deleteListButton.grid(column=0, row=3, sticky='ws', padx=(8, 0), pady=(0, 8))

        # Delete word button
        self.deleteWordButton = tk.Button(self, text="Delete word", command=self.deleteWord, font=self.buttonFont,fg=self.labelColor, bg=self.buttonColor)
        self.deleteWordButton.grid(column=0, row=3, sticky='s', padx=(8, 0), pady=(0, 8))
        self.deleteWordButton.config(state='disabled')

        # Listbox
        self.wordListbox = tk.Listbox(self, font=self.listFont)
        self.wordListbox.grid(column=1, row=1, rowspan=3, columnspan=2, sticky='nesw', padx=(0, 8), pady=(0, 8))
        self.wordListbox.bind('<<ListboxSelect>>', self.onListWordSelected)

        # Scrollbar to wordlistbox
        self.scrollbarWords = ttk.Scrollbar(self)
        self.scrollbarWords.grid(column=2, row=1, rowspan=3, sticky='nse', padx=(0, 8), pady=(0, 8))

        # Amount of rhymes
        self.countValuesLabel = tk.Label(self, text="number entries: 0", font=self.listFont, fg=self.labelColor, bg=self.backgroundColor)
        self.countValuesLabel.grid(column=2, row=3, sticky='se', padx=(0, 28), pady=(0, 10))

        # Configure listbox and scrollbar
        self.wordListbox.config(yscrollcommand=self.scrollbarWords.set)
        self.scrollbarWords.config(command=self.wordListbox.yview)

        # Initialize settings
        self.settings = {
            'lightmodeOn': self.isLightModeOn.get(),
            'isPerfectRhyme': self.isPerfectRhyme.get(),
            'withAdditionalwords': self.withAdditionalwords.get(),
            'combobox': "Vowel rhyme"
        }
        self.loadSettings()

        # List
        self.everyWord = []
        self.everyWordFiltered = []
        self.wordsInList = []
        self.loadWords()
        self.reloadList()
        self.amountOfAddedWords = 0
        self.amountOfUnconsideredWords = 0
        self.amountOfDuplicates = 0

        # Styles
        self.updateColors()
        self.toggleLightmodeImage()

        # List empty?
        self.checkListboxEmpty()


    def saveSettings(self):
        self.settings['lightmodeOn'] = self.isLightModeOn.get()
        self.settings['isPerfectRhyme'] = self.isPerfectRhyme.get()
        self.settings['withAdditionalwords'] = self.withAdditionalwords.get()
        self.settings['combobox'] = self.combo.get()
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)

    def loadSettings(self):
        with open('settings.json', 'r') as f:
            settings = json.load(f)

        # Update variables
        self.isLightModeOn.set(settings.get('lightmodeOn', True))
        self.isPerfectRhyme.set(settings.get('isPerfectRhyme', False))
        self.withAdditionalwords.set(settings.get('withAdditionalwords', False))
        self.combo.set(settings.get('combobox', "Vowel rhyme"))

    def checkListboxEmpty(self):
        if self.wordListbox.size() == 0:
            self.instructionsListbox()

    def instructionsListbox(self):
        space = ""
        instructions = [
            "This is Rhyme generator!",
            space,
            "Write a word for which you are looking for a rhyme",
            "in the text field.",
            space,
            "If you are using this programme for the first time, you",
            "do not yet have any words that could rhyme with the",
            "word you have typed. ",
            space,
            "Add a list by clicking on ‘Add a list (txt)’ and selecting",
            "a text file from your explorer. The text file must",
            "contain words.",
            space,
            "It is not required to follow a certain pattern in order",
            "to identify the words. It just finds every word.",
            space,
            "If ‘Perfect rhyme’ is not selected, e and i as well as",
            "u and o are treated as the same letter in the rhyme.",
            space,
            "it is easy to overhear the difference between the two",
            "letters, in a rap text. ",
            space,
            "Try your hand at this program!",
            space,
            "Thank you for using rhyme Generator :)"
        ]

        for instruction in instructions:
            self.wordListbox.insert(tk.END, instruction)

        self.countValuesLabel.config(text=f"")


    def switchLightMode(self):
        currentValue = self.isLightModeOn.get()
        self.isLightModeOn.set(not currentValue)
        self.updateColors()
        self.toggleLightmodeImage()
        self.saveSettings()


    def allConstructFromWords(self, target, wordListfiltered, wordlist):
        if target == "":
            return [[]]  # Base case: If the target is an empty string, return an empty list

        def stripSubstring(mainString, substring):
            # Remove from the start if it exists
            if mainString.startswith(substring):
                mainString = mainString[len(substring):]

            # Remove from the end if it exists
            if mainString.endswith(substring):
                mainString = mainString[:-len(substring)]

            return mainString;

        foundAdditionalWordslist = [];

        newWordListfiltered = [];
        newWordlist = [];

        for word in wordListfiltered:
            newWordListfiltered.append(word);
        for word in wordlist:
            newWordlist.append(word);

        iterations = 0;
        while iterations < len(newWordlist):
            def backTrack(newTarget):
                prevtarget = newTarget;
                matchedWordfiltered = [];
                matchedWord = [];

                found = False;
                while True:
                    wordsToRemoveFiltered = [];
                    wordsToRemove = [];

                    for i, word in enumerate(newWordListfiltered):
                        if(newTarget.startswith(word)):
                            matchedWordfiltered.append(word);
                            wordsToRemoveFiltered.append(word);

                            matchedWord.append(newWordlist[i]);
                            wordsToRemove.append(newWordlist[i]);

                            newTarget = newTarget[len(word):]
                            newTarget = stripSubstring(newTarget, ".");

                            if(".".join(matchedWordfiltered) == prevtarget):
                                found = True;
                                break;

                    # Remove from lists
                    for word in wordsToRemoveFiltered:
                        if word in newWordListfiltered:
                            index = newWordListfiltered.index(word)
                            newWordListfiltered.pop(index)
                            newWordlist.pop(index)

                    break;

                if(found):
                    #for index, word in enumerate(" ".join(matchedWord)):
                    return " ".join(matchedWord);
                else:
                    return "";

            word = backTrack(target);
            if(word != ""):
                foundAdditionalWordslist.append(word);
            else:
                iterations += 1;


        return foundAdditionalWordslist;


    def deleteList(self):
        questionResult = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all words?")

        if questionResult:
            self.everyWord = []
            self.everyWordFiltered = []
            self.wordsInList = []

            # Deleting content of file
            try:
                with open(self.loadFileName, "w") as file:
                    # Clear text
                    file.write("")
                messagebox.showinfo("Cleared", "The word list has been cleared.")
            except Exception as error:
                messagebox.showerror("Error", f"An error occurred while deleting the words: {error}")

            self.reloadList()

            # List empty?
            self.checkListboxEmpty()

    def onListWordSelected(self, event):
        self.checkWordSelection()
        self.deleteWordButton.config(state='normal')
        if self.withAdditionalwords.get():
            self.deleteWordButton.config(state='disabled')

    def checkWordSelection(self):
        selectedIndex = self.wordListbox.curselection()
        if selectedIndex:
            self.deleteWordButton.config(state='normal')
        else:
            self.deleteWordButton.config(state='disabled')

    def deleteWord(self):
        selectedIndex = self.wordListbox.curselection()
        index = selectedIndex[0]
        value = self.wordListbox.get(0, tk.END)[index]

        questionResult = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {value}?")

        if(questionResult):
            self.wordListbox.delete(index)
            self.everyWord.remove(value)
            self.reloadList()
            self.saveWords(self.everyWord)
            messagebox.showinfo("Cleared", f"{value} has been deleted.")

        self.checkWordSelection()

    def chooseFile(self):
        # Open file dialog | Only .txt and .pdf files
        filePaths = filedialog.askopenfilenames(
            filetypes=[("Text Files", "*.txt"), ("PDF Files", "*.pdf")],
            defaultextension=".txt"
        )

        # Path selected?
        if filePaths:
            # Load in list
            for filePath in filePaths:
                if filePath.endswith('.txt'):
                    self.extractWordsFromFile(filePath)
                elif filePath.endswith('.pdf'):
                    self.extractWordsFromPDF(filePath)

            amountFiles = len(filePaths)

            # Message
            fileTerm = "files" if amountFiles > 1 else "file"
            UnconsideredTerm = f"\n{self.amountOfUnconsideredWords} entries were not considered as a word" if self.amountOfUnconsideredWords > 1 else ""
            duplicateTerm = f"\nIt found {self.amountOfDuplicates} duplicate words that were not added." if self.amountOfDuplicates > 1 else ""
            message = f"Extracted {self.amountOfAddedWords} words from the {fileTerm}.{duplicateTerm}{UnconsideredTerm}".strip()
            messagebox.showinfo("Words Extracted", message)

            self.amountOfAddedWords = 0
            self.amountOfUnconsideredWords = 0
            self.amountOfDuplicates = 0


        else:
            # No file selected
            messagebox.showinfo("No file selected", "Please select a file.")

        #Clear user input
        self.entry.delete(0, "end")
        self.userInput = ""
        self.reloadList()

        # List empty?
        if not len(self.everyWord) > 1:
            self.checkListboxEmpty()

    def extractWordsFromFile(self, filePath):
        try:
            # Read file
            with open(filePath, 'r', encoding='utf-8') as file:
                content = file.read()

            # Regex -> commas, spaces, in quotes
            words = re.findall(r'"(.*?)"|(\b(?!\w*\d)\w+\b)', content)
            fileWordList = [word for sublist in words for word in sublist if word]

            for word in fileWordList:
                if word.lower() not in (existingWord.lower() for existingWord in self.everyWord):
                    if(self.checkIfWord(word)):
                        self.everyWord.append(word)
                        self.amountOfAddedWords += 1
                    else:
                        self.amountOfUnconsideredWords += 1
                else:
                    self.amountOfDuplicates += 1

            # Reload list
            self.reloadList()

            # Save new words in textfile
            self.saveWords(self.everyWord)

        except Exception as error:
            messagebox.showerror("Error", f"An error occurred while reading the file: {error}")

    def extractWordsFromPDF(self, filePath):
        try:
            # Read PDF file
            with open(filePath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                content = ""
                for page in range(len(reader.pages)):
                    content += reader.pages[page].extract_text()

            # Regex -> commas, spaces, in quotes
            words = re.findall(r'"(.*?)"|(\b(?!\w*\d)\w+\b)', content)
            fileWordList = [word for sublist in words for word in sublist if word]

            for word in fileWordList:
                if word.lower() not in (existingWord.lower() for existingWord in self.everyWord):
                    if (self.checkIfWord(word)):
                        self.everyWord.append(word)
                        self.amountOfAddedWords += 1
                    else:
                        self.amountOfUnconsideredWords += 1
                else:
                    self.amountOfDuplicates += 1

            # Reload list
            self.reloadList()

            # Save new words in textfile
            self.saveWords(self.everyWord)

        except Exception as error:
            messagebox.showerror("Error", f"An error occurred while reading the PDF file: {error}")

    def saveWords(self, newWords):
        # Save new words in loadwords.txt
        try:
            with open(self.loadFileName, "w") as file:
                for word in newWords:
                    # Add words
                    file.write("")
                    file.write(word + "\n")
        except Exception as error:
            messagebox.showerror("Error", f"An error occurred while saving the words: {error}")

    def checkIfWord(self, word):
        vowels = "aeiouäüöAEIOUäüö"
        if(len(word) > 1):
            return any(char in vowels for char in word)
        else:
            return False

    def updateListbox(self, words):
        self.wordListbox.delete(0, tk.END)
        for word in words:
            self.wordListbox.insert(tk.END, word)

        # Reload amount label
        self.updateRhymeCount()

    def updateRhymeCount(self):
        count = self.wordListbox.size()
        self.countValuesLabel.config(text=f"number entries: {count}")

    def getLastNCharacters(self, word, number):
        return word[-number:]

    def getAllExceptLastNCharacters(self, word, number):
        return word[:-number] if number != 0 else word

    def updateWordsInList(self, userWord, filteredWord):
        filteredList = []

        for word, filtered in zip(self.everyWord, self.everyWordFiltered):
            # if self.getLastNCharacters(filtered, len(filteredWord)) == filteredWord:
            if filtered == filteredWord:
                if (word.lower() != userWord.lower()):
                    # Remove whitespace
                    cleanedWord = word.replace(' ', '')
                    filteredList.append(cleanedWord)

        if self.withAdditionalwords.get():
            # Additional words
            additionalwords = self.allConstructFromWords(filteredWord, self.everyWordFiltered, self.everyWord)
            for word in additionalwords:
                if(word.lower() != userWord.lower()):
                    filteredList.append(word)

        return filteredList;

    def onComboSelected(self, event):
        self.selectedOption = self.combo.get()
        self.reloadList()

    def removeConsonants(self, inputString):
        resultString = []
        inputString = inputString.lower()
        print(inputString)
        # if consonant ending
        consonantEnding = ""
        if self.selectedOption == "Vowel rhyme + consonant ending" or self.selectedOption == "Classic rhyme":
            consonantEnding = self.getEndingConsonants(inputString)


        # Exeptions
        inputString = inputString.replace('team', 'i');
        inputString = inputString.replace('training', 'e.i')
        inputString = inputString.replace('ferien', 'e.i.e')
        #inputString = inputString.replace('computer', 'o.i.u.e')
        inputString = inputString.replace('fair', 'ä')

        # i = ie = j = y
        inputStringIE = inputString.replace('ie', 'i')
        inputStringJ = inputStringIE.replace('j', 'i')
        inputStringY = inputStringJ.replace('y', 'i')

        # eu = äu = 1
        inputStringEU = inputStringY.replace('eu', '1')
        inputStringAU = inputStringEU.replace('äu', '1')

        # au = 2
        inputStringAU2 = inputStringAU.replace('au', '2')

        # ei = 3
        inputStringEI = inputStringAU2.replace('ei', '3')

        # English addition
        # ea = ä
        #inputStringEA = inputStringAA.replace('ea', 'ä')

        # ä = e
        inputStringEAE = inputStringEI.replace('ä', 'e')

        #aa = a | ee = e
        inputStringAA = inputStringEAE.replace('aa', 'a')
        inputStringEE = inputStringAA.replace('ee', 'e')

        # ee = e
        inputStringOU = inputStringEE.replace('ou', 'u')

        # er ending = a
        inputStringER = inputStringOU
        #if len(inputStringER) >= 2:
        #    erEnding = inputStringER[-2:]
        #    if(erEnding == "er"):
        #        inputStringER = inputStringER[:-2] + "a"
    #
        lastString = inputStringER

        # Remove consonants
        inputString = lastString

        for char in inputString:
            if char in self.charsToAdd:
                if resultString:
                    resultString.append('.')
                resultString.append(char)

        filteredString = ''.join(resultString)


        # Vowel rhyme | Vowel rhyme + consonant ending
        if self.selectedOption == "Vowel rhyme + consonant ending":
            filteredString += consonantEnding

        # Classic rhyme | Only last vowel + consonant ending
        if self.selectedOption == "Classic rhyme":
            secondLastChar = ''
            if(len(filteredString) > 1):
                secondLastChar = filteredString[-3]

            classicString = secondLastChar + filteredString[-1] + consonantEnding;
            filteredString = classicString;

        # Checkbox checked?
        if not self.isPerfectRhyme.get():
            # Not perfect means i=e, o=u
            # ia = a
            step1 = filteredString.replace('ia', 'a')

            # io = o
            step2 = step1.replace('io', 'o')

            # iu = u
            step3 = step2.replace('iu', 'u')

            step4 = step3.replace('i', 'e')
            step5 = step4.replace('o', 'u')

            filteredString = step5
        print(filteredString)
        return filteredString

    def getConsonantsBetweenLastTwoVowels(self, word):
        # Find all vowels in the last syllable
        vowels = [match.start() for match in re.finditer(r'[aeiouäü]', word, flags=re.IGNORECASE)]

        # Check if there are at least two vowels
        if len(vowels) >= 2:
            # Get the substring between the last two vowels
            consonants = word[vowels[-2] + 1: vowels[-1]]
            # Remove any vowels that may be in this substring
            consonants = re.sub(r'[aeiouäü]', '', consonants, flags=re.IGNORECASE)
            return consonants

        # Return an empty string if there are not enough vowels
        return ''

    def reloadList(self):
        #Delete button off when additional words is selected
        self.checkWordSelection();
        self.deleteWordButton.config(state='normal')
        if self.withAdditionalwords.get():
            self.deleteWordButton.config(state='disabled')


        # Reload every filtered word
        self.everyWord = sorted(self.everyWord, key=str.lower)
        self.wordsInList = self.everyWord
        self.everyWordFiltered = []
        for word in self.everyWord:
            self.everyWordFiltered.append(self.removeConsonants(word))

        # Reload user Input
        self.userInput = self.entry.get()
        if any(char in self.charsToAdd for char in self.userInput):
            self.filteredInput = self.removeConsonants(self.userInput)
            self.updateListbox(self.updateWordsInList(self.userInput, self.filteredInput))
        else:
            self.updateListbox(self.wordsInList)

        # List empty?
        if (self.everyWord == []):
            self.checkListboxEmpty()

        # Settings
        self.saveSettings()

    def toggleLightmodeImage(self):
        # Toggle buttonimg based on state
        if self.isLightModeOn.get():
            self.lightmodeButton.config(image=self.imgSun)
        else:
            self.lightmodeButton.config(image=self.imgMoon)

    def onKeyreleased(self, event):
        # Cancel the previous timer if it exists
        if self.keypressTimer is not None:
            self.after_cancel(self.keypressTimer)

        # Set a new timer to call the function after a delay
        self.keypressTimer = self.after(500, self.onKeypressed)  # 500 milliseconds = 0.5 seconds


    def onKeypressed(self):
        # Everytime when key gets hit
        self.selectedOption = self.combo.get()
        self.reloadList();

    def loadWords(self):
        if os.path.exists(self.loadFileName):
            try:
                with open(self.loadFileName, "r") as file:
                    self.everyWord = [line.strip() for line in file.readlines()]
            except Exception as error:
                messagebox.showerror("Error", f"An error occurred while loading the words: {error}")

    def extractLastSyllable(self, word):
        # Find last syllable
        match = re.search(r'[aeiouäü]+[^aeiouäü]*$', word, re.IGNORECASE)
        if match:
            return match.group()
        return word

    def getEndingConsonants(self, word):
        # Get last syllable
        lastSyllable = self.extractLastSyllable(word)

        # Remove vowels
        consonants = re.sub(r'[aeiouäü]', '', lastSyllable, flags=re.IGNORECASE)
        return consonants


    def updateColors(self):
        # Colors
        if (self.isLightModeOn.get()):
            self.labelColor = "black"
            self.buttonColor = "gray85"
            self.backgroundColor = "gray95"
            self.textboxColor = "white"
            self.comboboxColor = "white"
            self.listboxColor = "white"
            self.checkboxColor = "black"
        else:
            self.labelColor = "gray95"
            self.buttonColor = "gray15"
            self.backgroundColor = "gray20"
            self.textboxColor = "gray35"
            self.comboboxColor = "gray35"
            self.listboxColor = "gray35"
            self.checkboxColor = "gray"

        # Apply colors to widgets
        self.configure(bg=self.backgroundColor)
        self.titleLabel.config(fg=self.labelColor, bg=self.backgroundColor)
        self.copyrightLabel.config(fg=self.labelColor, bg=self.backgroundColor)
        self.entry.config(bg=self.textboxColor, fg=self.labelColor)
        self.checkPerfectRhyme.config(fg=self.checkboxColor, bg=self.backgroundColor, activebackground=self.buttonColor, activeforeground=self.labelColor)
        self.checkWithAdditionalwords.config(fg=self.checkboxColor, bg=self.backgroundColor, activebackground=self.buttonColor, activeforeground=self.labelColor)
        self.chooseFileButton.config(fg=self.labelColor, bg=self.buttonColor)
        self.lightmodeButton.config(fg=self.labelColor, bg=self.buttonColor)
        self.deleteListButton.config(fg=self.labelColor, bg=self.buttonColor)
        self.deleteWordButton.config(fg=self.labelColor, bg=self.buttonColor)
        self.wordListbox.config(bg=self.listboxColor, fg=self.labelColor)
        self.countValuesLabel.config(bg=self.listboxColor, fg=self.labelColor)

if __name__ == "__main__":
    app = gui()
    app.mainloop()
