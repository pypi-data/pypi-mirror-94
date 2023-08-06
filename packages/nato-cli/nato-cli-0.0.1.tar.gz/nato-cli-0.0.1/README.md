
# nato-cli
Allows quick translation of a string to its letters in NATO form.

# Installation
`pip install nato-cli`

# Usage

    > nato Sampath
    s       Sierra
	a       Alpha
	m       Mike
	p       Papa
	a       Alpha
	t       Tango
	h       Hotel


Alternatively, with no arguments:

    > nato
    Enter a String to be converted into the NATO Alphabet, or type exit:
    Sampath
    s       Sierra
	a       Alpha
	m       Mike
	p       Papa
	a       Alpha
	t       Tango
	h       Hotel
	Enter a String to be converted into the NATO Alphabet, or type exit:
	exit
    

By default, running the program will prompt for a value (in console), which will then be spelled out in NATO letters. You can also pass an argument and it will spell it out automatically, then resume prompting for values. Type `exit`  to exit.

I made this package because I wanted a quick way to convert something to the NATO alphabet when I was on the phone, and time was of the essence. If you're on Windows, the quickest way to run this is by opening the Run Dialog, (Win+R) and typing in `nato phrase`, where it will display your phrase in a new window. That's also the reason why it constantly prompts for a new string - unless the program is waiting for user input, anything launched from the Run dialog will close as soon as execution is finished. 
