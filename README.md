# source of guess-word-bot ( https://t.me/guess_word_bot )

## a telegram bot to play guess word game 🤓

When you start the game, bot picks up a random word (via random-word-api) and gives you chances to guess the word by typing letters.  

Count of chances (❤️ emojis) = count of unique letters in the hidden word)

When you type a letter, if the letter is contained in the word, it will be shown up. Elsewise, you will lose one chance.

If you need help - you can use `/help` command (only once) to get definition of the word.  
(I used oxford dictionary api to get definition)

Screenshot from game:
![Screenshot](sample_screenshot.png?raw=true "Screenshot")
