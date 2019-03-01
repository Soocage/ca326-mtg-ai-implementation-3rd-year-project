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

We utilised unit testing for these screens by utilising suites. Firstly, the screen was loaded into the default resolution then was paused for 5 seconds for observation. We then would cycle through each resolution in turn and would then perform the same commands.

Once one screen had finished displaying the next screen in the sequence would then be loaded and the the same processes would be carried through.

This testing phases proved to be quite useful more finding errors such as finding bugs where text would not display to the expected size and finding bugs where screen object dimensions where not altered upon changing the display size. This early testing lead us to creating a new file to store dimensional data which could be imported and updated at will, which in turn made our code more readable.  Another issue that this testing pointed out to us was at lower resolutions some text and cards were not as visible as we would have wished. Through releasing this we then used anti-aliasing features for text and smooth scaling images to ensure that everything was as visible as possible at any given resolution.

**Testing Sprite Drawing Functionality**

The second core feature that we had to test was the functions which calculated the dimensions and textures for the sprites in the the player&#39;s hand, both players&#39; land sections and both players&#39;  battlefield sections. Each of these sections would be drawn to the screen at varying resolutions. Predefined card objects were passed to these functions as to test a variety of scenarios on the board.  Unit testing and suites were used to test these screens in sequence.

We tested these functions as displaying these fields to the screen is crucial for the player to be able to interface with the game and respond appropriately. This testing helped us develop working properly functioning processes which would calculate and adapt the positions of the sprites properly according to screen resolution. Initially cards were drawn in accordance to a single resolution size but upon testing through unit tests it was clear updates to the calculations were needed.  This testing also allowed us to confirm that crucial aspects to the game such as tapping and attacking were working as intended.





**Testing Player Data Values**

Player data values represent important information to be known by a player during the game such as player life totals, the size of each players deck, hand, and graveyard. Similarly we utilised suite testing at multiple resolutions with multiple font sizes to ensure the the text displayed onto the screen was both readable and within the intended parameters we assigned for it. Testing these initially showed there to be no issues regarding this functionality and as a result ensured that there was no logical or graphical issues to be addressed with this functionality.

**Testing Card Reading/Writing Using Pickle**