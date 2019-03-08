**Introduction**
This is a technical manual for the third year project Magic The Gathering (MTG) Ai Implementation. It will consist of a detailed descriptions of the functions used throughout the system. This system has been built using python 3.7.2 the newest release of the pygame library. This manual expects you to have read the user manual and expects you to be familiar with the rules of MTG.

**Introduction Screen**
This introduction screen consists of 4 buttons. Each button is constantly beings redraw at every frame of the program running. At each frame the system checks at what coordinates the mouse is. If the mouse ever crosses over one of the buttons the button will then be re-drawn using a lighter colour to signify that it is clickable.

Each button has an assigned action which will trigger a function call. That function will then redraw the screen based on which button has been pressed.

When you press the Quit button the program will run a quitting function that will close itself
![alt text][screen]
[screen]: https://gitlab.computing.dcu.ie/mccans32/2019-ca326-mccans32-mtg_ai_implementation/blob/master/technical_manual/images/intro_screen.png

**Options**
After clicking the options menu button you will be launched into the options menu screen. This menu consists of 3 sections.

**Screen resolution**
This is a simple system of buttons that work similarly to the buttons in the main menu. Upon clicking on one of the buttons above your current resolution will be changed and the screen will be redrawn.

**Volume**
This is a very simple ingame volume slider. The system has currently a background track that plays on a loop. By clicking the plus or minus buttons you will increase the volume 1.0 being the maximum and 0.0 being the minimum.

**Back**
The last button is a simple function call that returns you back to the main menu screen. The screen is yet again redrawn with the previous 3 buttons.

**Play vs Ai**
By clicking this button you will be launched into a deck selection screen. This screen will have the names of 5 pre-made decks. Information on these decks can be found in the user manual. By clicking one of these buttons you will load into the program a pre-set list of card objects and assign them as your deck. You will then be asked to the same for the opponent Ai. and with that the game begins

**The game Screen**
The game screen consists of 7 different sections

**Player Info Section**
The player info section stores all relevant information on the player and the opponent. It also contains a card display area which will display any card you hover over on with your mouse.
It also shows both players life totals, their current hand size, amount of cards in the enemy graveyard, and the amount of cards remaining in each players deck.
The last section is the multi-coloured box at the top and bottom. This Both players current mana. Whenever a player taps a land to generate mana it will assign the first letter of that colour ,or u if its blue , to the player or ai mana. Then a function will scan through that string and count all instances of the letters. It will then display the number of instances in the appropriate boxes.

**The Menu Buttons**
There are two buttons in this section. The first buttons allows you to access the same options menu has the one described in section 3. The other buttons allows the user concede a game and have him return back to the main menu. This is done by setting a quit flag within the game loop. When either player loses or if one of them chooses to concede that flag is turned on. The winner is then declared and the player is launched back into the main menu screen.

**The Players Hand section**
This section will show all cards the player currently has in his hands. These cards each have their own mana cost and abilities as described on the cards

**The Players play field and Ai play field**
Both of these act similarly. Whenever either play plays a card it will be added to their play field. Creatures will be centered towards the middle of the screen, while lands will be closer to each players hand fields. Instants and Sorceries will be automatically sent to the graveyard after being used.

**The Last Card Played display(LCPd)**
This is a simple section of the screen dedicated to the most recent card played. All instants and sorceries will be displayed there before their effects are executed.

**The Turn and phase indicators**
Just above the players hand field you will see the phase indicator. This indicator checks which phase you or the enemy ai are currently on and highlights it .
At the end of them you will have a pass button which will allow you to pass priority and move onto the next phase.
Above the pass button you will see a turn indicator. It will change colour and message depending on whose turn it is and what current state you are in.


Green : It&#39;s your turn you can play creatures, Sorceries and instants.

Red    : It&#39;s the enemies turn. Wait until he passes priority before you can do anything.

Blue   :It&#39;s your Response phase, the opponent has done something and now you can  try and respond by playing an Instant.

Orange: It&#39;s your enemies Response phase, wait until they either pass priority to continue playing.

Brown: Blocking , chose ally creatures to block enemy attacks with.

Grey : attacking, Choose ally creatures with which you would like to attack.

**The Mulligan**
This is a simple function which allows the player to redraw a new hand if they do not want to keep their current hand. However their next hand will have one fewer cards.

**Turn System**
Each turn is sub divided into 6 phases. The combat phase is subdivided into 3 more phases and after each phase the opponent has a chance to respond.

**Untap**
During the untap step the system scans through all the cards currently on the battlefield. It refreshes the combat state of each card, It sets each card back to being untapped and resets all temporary modifiers that each card had on it.(For more information please visit the User manual). This process is the same for each player.

**Draw**
During this step the player whose turn it is draws the top card of their deck. If a player would have 0 cards left in his deck and would be forced to draw they would automatically lose the game.

**Main 1**
This phases is different for the Player and the AI

**Player:**
During the players main phase he has the choice of playing any of the cards in their hand. Each card will have a mana cost that needs to be paid in order for them to be able to cast it(For more information please visit the user manual). Each card is played by simply dragging it off the player hand section. Depending on what card is played it will be centered on different points in the player&#39;s play field.(Shown in section 5.d)

**Ai :**
During the AI&#39;s turn depending on what coloured deck the AI is playing it will make different decisions. However the main goal for the Ai is to increase its board state, reduce your board state and lower you life total. As such the ai , After playing a land card if available, will look at its total available lands and calculate all possible permutations of cards it can play this turn. For each permutation it will calculate how close it will be to the ideal board state and decide on the most optimal cards it could play this turn.

After any card other than a land is played by either the Player or the Ai, the opposing player enters a response phase.

**Combat**
Combat phase is broken down into 3 sub phases

**Selecting Attacker**

**Player:**
The player select their attackers by left clicking on the card they wish to attack with. A clicked card enters a attacking combat state and it cannot be deselected. All creatures that are attacking are now tapped.(For more information please read User manual).

**Ai:**
Similarly to a player the Ai also chooses their attackers. It does so by yet again calculating all possible permutations of possible attacks and possible defenders from the opponent. It then calculates what set of defenders will lead the Player to sustain the last amount of damage to their life total while maintaining a lead in the board state. The Ai then compares each one of its permutations against this possible best case scenario and comes up with the most viable move that the player would make given some set of attackers. Given this information it then chooses its attackers and awaits blockers.

**Selecting Defenders/Blockers**

**Player:**

The Player selects from his battle field any number of creatures lower than or equal to the number of attackers to defend. They do so by clicking on an untapped creature on their play field and then clicking which attacker they wish to block. (For more information please read the user manual)

**Ai:**

The Ai selects his defenders by running calculations similar to the ones described before. The Ai compares a set of all possible permutations of blockers to a list of attacking creatures. This yields different results in terms of the board state. Depending on the colour of the Ai you&#39;re fighting against you can expect it to either try and destroy most of your attackers or keep their side of the field wider to attack you when your weakest

After the selection of attacker and defenders steps are done we enter the damage step. This step is the same for both the Ai and the Player. Each attacking creature power is compared to a defenders toughness and vice versa. When the power exceeds the toughness the creature with said toughness is dead.(For more information on combat please visit the user manual)

**Main Phase 2.**
This phase is the same exact logic as the Main phase one (Section 7.c)

**End Step**
This is the final step for either player. During this step the system will scan both playing fields and search for all creatures with any negative toughness and reset it to its original value, reset any and all temporary effects that any creature and/or player would have such as protection and it will be the last time the opponent player enters a response phase before their turn.