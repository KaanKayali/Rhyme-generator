# Rhyme-generator
This is Rhyme generator!<br>
It is made in python with the tkinter library.

It currently only works with german words.
That is because in German, words usually rhyme by following a simple pattern that works for most cases.
It is a little different in English, which is the reason I have not implemented it yet.

## How it works
Type a word, wordcombination or even a phrase into the top-left textbox to find a rhyme for it.
You will get as many rhymes as possible in the listbox at the right, based on your settings.

If you are using this program for the first time, <br>
you do not have any words yet that could rhyme with the word you typed.

#### Add words
Add a list of words by clicking on `Add a list (txt/PDF)` and selecting a text- or PDF file from your explorer. <br>
The file must contain words.

The file is not required to follow a certain pattern in order to identify the words. <br>
The program is able automatically identify the words.

#### Additional words
By activating `Additional Words`, you allow the program to find rhymes for your input <br>
that include multiple words linked together.

#### Rhyme-type
There are a few types/ways the program can find rhymes for your input.
- **Classic rhyme**: The endings of words that rhyme are identical
- **Vowel rhyme**: The words that rhyme both have the same vowels.
- **Vowel rhyme + consonant ending**: Words that rhyme both have the same vowels and the same endings.

The most popular one, which also is mostly used in poems, is the classic-type of rhyme.

#### Language
The language option currently only changes the text in the user interface. It can not find rhymes in English yet.

#### Perfect Rhyme
If the `Perfect rhyme` option is turned off, the program treats **e** and **i**, as well as **u** and **o**, as the same sounds when finding rhymes. <br>
This is useful in rap lyrics, where these differences are easy to overhear.

## How to use 
Try your hand at this program!

Thank you for using rhyme Generator :)
