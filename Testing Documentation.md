**CA326 Test Documentation**

**Test Plan**

For our project there are three main areas that must be tested in order to ensure that the overall program is working to the best of its ability.

These three main sections are:

- The game logic
- The game UI/ UI Interaction
- The AI computations

For this these test cases there will be multiple assumptions held in regards to the user and program. Firstly, it is assumed that the user will be running the program on a monitor screen with a large enough resolution to display the graphics of the program optimally. It is also assumed that the user has the ability to use a physical mouse for UI interaction within the game.

Below is a list of features that are to be tested within the program.

- User testing the running application
- Varying resolutions in the main menu.
- Varying resolutions in the options menu
- Varying resolutions of the in-game board
- Changing resolution mid-game
- Testing hand drawing functionality for the player
- Testing land drawing function for both players
- Testing battlefield drawing function for both players
- Testing player data values being updated to screen during gameplay
- Reading card data from file using pickle
- Writing card data to file using pickle
- Deck creation functionality
- GUI interaction for the main menu
- GUI interaction for the options menu
- GUI interaction within all of the game-phases
- Testing mana calculations
- Testing card effects
- Testing combat damage calculations
- Testing AI move calculation for red decks
- Testing AI move calculation for blue decks
- Testing AI move calculation for green decks
- Testing AI move calculation for white decks
- Testing AI move calculation for black decks
- Testing UI icon display feature
- Testing card display feature at all phases of the game



For testing the program we will use three main methods to ensure that the program is working as intended.

- User testing to ensure that the GUI is intuitive and that the game can be played.
- In game testing to test UI features/
- Unit testing for game functions within the logic

**Testing Varying Resolutions**

It is important to ensure that the game screens are both in proportion and are viewable at all resolutions available in the game. The game supports four popular resolutions to accomodate for screens of varying size, 1024x768, 1440x900, 1600x900 and 1920x1080.
The game was tested at these varying resoloutions during end user testing for the applications. before a game had begin and through the functionality provided by the change resoloution button within the options menu of the game.
While in all of these resolpoutions the proportions of all the display sections and card sprites were examined for any abnormalitires in positioning and display. We found that through these end user tests that the game code for displaying sections has been defined correctly
through the usage of ratios rather than hard coded values. This was by far the most important functionality that needed to be tested for the game as it was crucial that our game was functional at any of the provided resoloutions.


**Testing Sprite Drawing Functionality**

The second core feature that we had to test was the functions which calculated the dimensions and textures for the sprites in the the player&#39;s hand, both players&#39; land sections and both players&#39;  battlefield sections. Each of these sections would be drawn to the screen at varying resolutions during the end user testing phases. Predefined card decks were passed to these functions as to test a variety of scenarios on the board.

We tested these functions as displaying these fields to the screen is crucial for the player to be able to interface with the game and respond appropriately. This testing helped us develop working properly functioning processes which would calculate and adapt the positions of the sprites properly according to screen resolution. Initially cards were drawn in accordance to a single resolution size but upon testing through unit tests it was clear updates to the calculations were needed.  This testing also allowed us to confirm that crucial aspects to the game such as tapping and attacking were working as intended. Also upon testing these display functions with users it was clear that the sprite positions had to be centralised on the screen. Initially sprites were drawn from left to right but users provided feedback in which they explained that it was hard to keep track of all the information using this method.

**Testing Player Data Values**

Player data values represent important information to be known by a player during the game such as player life totals, the size of each players deck, hand, and graveyard. Similarly we utilised in-game testing with multiple resolutions with multiple font sizes to ensure the the text displayed onto the screen was both readable and within the intended parameters we assigned for it. Testing these initially showed there to be no issues regarding this functionality and as a result ensured that there was no logical or graphical issues to be addressed with this functionality. All the text contained within these sections was clearly displayed and no user tests prooved otherwise.

**Testing Card Reading/Writing Using Pickle**
within the application the pickle module is used to write card objects to and from files. We wrote a test deck within our code directory which would read all information form a predefined deck_List of card objects and would test in-game to see if the deck attributes and carfd attributes were accurate. Once we were happy with this process decks for each colour were written and read utilising pickle and these decks were futher tested within the application to ensure that game mechanics worked as intended.

**GUI Interactions**

All GUI interactions within the game could only be tested during end user testing and in-game testing. We knew that it was crucial that there would be no points in the game functionality where a break in GUI logic or in-game calculations would break the game. As previously stated our decks were rigourously tested in game to ensure that no implemented Creature or Spell effects would cause a crash in the game upon interactions via the GUI. During our GUI testing of the game it was clear that more feedback was needed upon playing cards. This lead us to redesigning the UI to become clearer for the player and we also then included new combat phase animations, phase animations, turn indications, and spell target icons.

**Testing Mana Calculations**

Mana testing was split between both unit testing and in-game testing. Unit tests were carried out on the game and ai calculations functions for adding mana and casting cards. We ensured that all values were logically as intended and that all values and cards sprites played via mana casting were displayed properly on the screen. Testing these functions sghowed us that there were logical errors within the ai functions for calculating mana which when fixed made that AI more responsive and played cards for the correct cost. This was an extremely important issue that was caught and then fixed.

**Testing Card Interactions**

Card interactions were tested through multiple test runs in-game. Each deck was played against each other deck multiple times in varying combinations. Each time an error occuered or a crash occuered it was noted and then quicly remedied. These functions are the core of how players intersct with each other in-game. It was a goal to attempt to fix all of these bugs through testing before any end-user testing had occuered. Ultimately this testing proved to be the most time consuming and rigorous as not only would logic need need to be fixed for the player but also for the AI opponent. Unit testing was not an option for this sections so this proved to be quite time consuming.

**Calculating AI logic**

AI logic could be tested easier via unit testing approaches as ther AI logic was calculated internally through data structures rather than through a GUI with the player. Testing these functions were fairly simple most of the time as predefined paramters were small and predictable but once combinations and permutations incorporated into the functions for the AI unit testing seemed to be quite out of hand. Instead, printing to output was utilised to test combinations and calculated values by the AI's functions. These helped us ensure thst the Ai was properly reading in combinations and applying all the appropriate clacultions.

**Review of Testing**

Overall it was difficult to test all of the functions effectively for this program due to the fact that so much of the games logic and functions depended on user input via GUI interactions. If we were to begin testing this again we would opt for futher simplifiying logic in the game into more simpler functions so unit testing could be carried out further. We found that while the end-user testing was very insightful and gave us back feedback that we had originally overlooked, many of the times when we got feedback through hese tests it proved to be quite challenging to rmedy either the bugs or unwanted features due to the fact that our code was not  refsctored to the optimal extent for unit testing to occur to a wider extent.