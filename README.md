# source of guess-word-bot ( https://t.me/guess_word_bot )

## a telegram bot to play guess word game 🤓

When you start the game, the bot picks up a random word (via random-word-api) and gives you extra lives to guess the word by typing letters.  

Count of extra lives (❤️ emojis) = count of unique letters in the hidden word

When you type a letter, if the letter is contained in the word, it will be shown up. Elsewise, you will lose one life.  

if you need a hint,  `/letter` will show up random letter for you (costs one life)

If the word is really hard to guess - you can use `/help` command (costs one life) to get the meaning of the word.  
(I used oxford dictionary api to get definitions)

Screenshot from game:
![Screenshot](sample_screenshot.png?raw=true "Screenshot")
