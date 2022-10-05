import arcade
SCREEN_WIDTH = 900             #setting the dimensions of screen
SCREEN_HEIGHT = 600
COLUMN_SPACING = 60
ROW_SPACING = 60                #dimension of each square of grid i.e 60*60
SCREEN_TITLE = "SNAIL GAME"
MOVE_STEP = 60                  #an increment in dimensions when a step is performed

class MainView(arcade.View):         #setting the main view of game
    def __init__(self):
        super().__init__()                
        self.width, self.height = self.window.get_size()
        self.window.set_viewport(0, self.width, 0, self.height)
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        backgound = arcade.load_texture("main.jpg")
        scale = self.height/800
        arcade.draw_scaled_texture_rectangle(self.width/2, self.height/2, backgound, scale, 0)
        arcade.draw_text("Snail Game", self.width/2, self.height/2,
                         arcade.color.WHITE, font_size=50, anchor_x="center",font_name="Algerian")
        arcade.draw_text("!!Halloween Addition!!", self.width/2, self.height/2-35,
                         arcade.color.CADET, font_size=20, anchor_x="center",font_name="Chiller")
        arcade.draw_text("Click to advance", self.width/2, self.height/2-100,
                         arcade.color.GAINSBORO, font_size=40, anchor_x="center",font_name="Freestyle Script")

    def on_key_press(self, key, modifiers): #to change screen to full and vice versa
        if key == arcade.key.F:
                # User hits f. Flip between full and not full screen.
                self.window.set_fullscreen(not self.window.fullscreen)

                # Get the window coordinates. Match viewport to window coordinates
                # so there is a one-to-one mapping.
                self.width, self.height = self.window.get_size()
                self.window.set_viewport(0, self.width, 0, self.height)

    def on_mouse_press(self, _x, _y, _button, _modifiers):  #transition from strat scrren to instruction screen through mouse press
        game_view = InstructionView()
        self.window.show_view(game_view)
        
class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.width, self.height = self.window.get_size()   #width and height will be set to what the current window has
        self.window.set_viewport(0, self.width, 0, self.height)

    def on_show(self):
        arcade.set_background_color(arcade.color.ARSENIC)

    def on_draw(self):
        arcade.start_render()
        backgound = arcade.load_texture("instruct.jpg")
        scale = self.height/350
        arcade.draw_scaled_texture_rectangle(self.width/2, self.height/2, backgound, scale, 0)
        arcade.draw_text("Instructions", self.width/2, self.height/2+120,
                         arcade.color.YELLOW, font_size=30, anchor_x="center",font_name="Algerian")
        arcade.draw_text("1.There are two players namelt Human and Bot.", (self.width/3)-110, self.height/2+50,
                         arcade.color.WHITE,font_name="Candara", font_size=15)
        arcade.draw_text("2. A player can play only one move at a time.", (self.width/3)-110, self.height/2+10,
                         arcade.color.WHITE,font_name="Candara", font_size=15)
        arcade.draw_text("3. Result will be generated on the basis of current grid count", (self.width/3)-110, self.height/2-30,
                         arcade.color.WHITE,font_name="Candara", font_size=15)  
        arcade.draw_text("   current grid count.", (self.width/3)-100, self.height/2-45,
                         arcade.color.WHITE,font_name="Candara", font_size=15)  
        arcade.draw_text("4. While moving on splash player can slip over it.", (self.width/3)-110, self.height/2-70,
                         arcade.color.WHITE,font_name="Candara", font_size=15)
        arcade.draw_text("5. When the score of both player combine exceed from 60 ", (self.width/3)-110, self.height/2-110,
                         arcade.color.WHITE,font_name="Candara", font_size=15)     
        arcade.draw_text("    there start a timer of 1 minute.", (self.width/3)-110, self.height/2-125,
                         arcade.color.WHITE,font_name="Candara", font_size=15)                      
        arcade.draw_text("Click to advance", self.width/2, self.height/2-175,
                         arcade.color.RED_ORANGE, font_size=40, anchor_x="center",font_name="Freestyle Script")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
                # User hits f. Flip between full and not full screen.
                self.window.set_fullscreen(not self.window.fullscreen)

                # Get the window coordinates. Match viewport to window coordinates
                # so there is a one-to-one mapping.
                self.width, self.height = self.window.get_size()
                self.window.set_viewport(0, self.width, 0, self.height)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()          #calling the actual game view after mouse press on instruction view
        self.window.show_view(game_view)
class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        self.width, self.height = self.window.get_size()
        self.window.set_viewport(0, self.width, 0, self.height)
        self.timer = 60                                      #setting timer to 60 seconds for each game period
        self.snail_list = arcade.SpriteList()                #creating lists of sprite
        self.splash_list = arcade.SpriteList()
        self.snail_player1 = None
        self.snail_player2 = None
        self.score_player1 = 0                                #initial scores are zero for both players
        self.score_player2 = 0
        self.player_switch = 1                              #players switch after each turn
        self.player1_cord = (0,0)                           #grid placement of each player at start
        self.player2_cord = (9,9)  
        self.isDown = True
        self.isLeft = False               
        self.board=[[1,0,0,0,0,0,0,0,0,0],                  #backend grid where 1 represents palyer 1 and 2 rrepresents player 2
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,2]]
        self.setup()                       #calling the setup function
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)
    def setup(self):
        self.snail_player1 = arcade.Sprite("player1.png", 0.15)      #setting up the sprites 
        self.snail_player1.center_x = ROW_SPACING/2
        self.snail_player1.center_y = COLUMN_SPACING/2
        self.snail_list.append(self.snail_player1)
        self.snail_player2 = arcade.Sprite("player2.png", 0.18)
        self.snail_player2.center_x =(SCREEN_HEIGHT)-(ROW_SPACING/2)
        self.snail_player2.center_y =(SCREEN_HEIGHT)-(COLUMN_SPACING/2)
        self.snail_list.append(self.snail_player2)



    def on_draw(self):
        arcade.start_render()
        backgound = arcade.load_texture("back.jpg")
        scale = self.height/800
        arcade.draw_scaled_texture_rectangle(450, 300, backgound, scale, 0)
        for x in range(0, 601, ROW_SPACING):         #this draws vertical lines
            arcade.draw_line(x, 0, x, 600, arcade.color.WHITE, 2)
        for y in range(0, 601, COLUMN_SPACING):          #this draws horizontal lines
            arcade.draw_line(0, y, 600, y, arcade.color.WHITE, 2)
        self.snail_list.draw()
        self.splash_list.draw()
        timer = f"Timer: {int(self.timer)}"     #rounding off the screen time to 2 digits
        arcade.draw_text(timer, self.width-(self.width//4.7), 100, arcade.color.DARK_PASTEL_BLUE, 30,anchor_x='center',font_name="Harlow Solid Italic")  #text to display on screen
        arcade.draw_text("Human", self.width-(self.width//4.7), 400, arcade.color.YELLOW_ORANGE, 40,font_name="Showcard Gothic",anchor_x='center')
        arcade.draw_text("VS", self.width-(self.width//4.7), 300, arcade.color.YELLOW_ROSE, 40,font_name="Matura MT Script Capitals",anchor_x='center')
        arcade.draw_text("AI", self.width-(self.width//4.7), 200, arcade.color.YELLOW_ORANGE, 40,font_name="Showcard Gothic",anchor_x="center")
    

    def slide_on_splash(self,player_splash,x,y,isLeft,isRight,isUp,isDown):
        if isLeft:
            while (y>0):
                if self.board[x][y-1] != player_splash:
                    break
                y -=1
            return x,y
        if isRight:
            while (y<9):
                if self.board[x][y+1] != player_splash:
                    break
                y +=1
            return x,y
        if isUp:
            while (x<9):
                if self.board[x+1][y] != player_splash:
                    break
                x +=1
            return x,y
        if isDown:
            while (x>0):
                if self.board[x-1][y] != player_splash:
                    break
                x -=1
            return x,y
            
   #draw splash for player 2
    def on_update(self, delta_time):
        self.score_player1 = 0
        self.score_player2 = 0
        for x in range(10):
            for y in range(10):
                if self.board[x][y]==100:      #updating score of players each time they make a move
                    self.score_player1 +=1
                elif self.board[x][y]==200:
                    self.score_player2 +=1
        if self.score_player1+self.score_player2<60:
            delta_time=0
        self.timer -= delta_time
        if self.player_switch==2:
            if self.score_player2<6:
                if self.isDown:
                    x,y = self.get_player2_cord()     #getting the xordinates where player 1 stands
                    self.player_switch = 1
                    self.board[x][y]=200
                    self.board[x-1][y]=2
                    self.isDown=False
                    self.isLeft=True
                else:
                    x,y = self.get_player2_cord()     #getting the xordinates where player 1 stands
                    self.player_switch = 1
                    self.board[x][y]=200
                    self.board[x][y-1]=2
                    self.isDown=True
                    self.isLeft=False
            else:
                x,y = self.get_player2_cord()     #getting the xordinates where player 1 stands
                self.player_switch = 1
                best_move = self.findBestMove(self.board,True,(x,y))
                self.board[x][y]=200
                self.board[best_move[0]][best_move[1]]=2
        if self.score_player1>=50 or self.score_player2>=50 or self.timer<0:          #winning criteria, if any player scores more than 50 he won or if time has ended
            game_over_view = GameOverView()
            game_over_view.score1 = self.score_player1
            game_over_view.score2 = self.score_player2
            self.window.show_view(game_over_view)           #calling the last view
        if len(self.splash_list) >0:
            splash_hit_list1 = arcade.check_for_collision_with_list(self.snail_player1,self.splash_list)
            splash_hit_list2 = arcade.check_for_collision_with_list(self.snail_player2,self.splash_list)
            for splash in splash_hit_list1:
                splash.remove_from_sprite_lists()
            for splash in splash_hit_list2:
                splash.remove_from_sprite_lists()
        for i in range(10):
            for j in range(10):
                x,y = (60*(j+1)-30),(60*(i+1)-30) #on which x,y to draw splash for player 
                if self.board[i][j]==100:
                    self.splash_sprite1 = arcade.Sprite("splashF.png", ROW_SPACING/100)
                    self.splash_sprite1.center_x = x
                    self.splash_sprite1.center_y = y
                    if self.splash_sprite1 not in self.splash_list:
                        self.splash_list.append(self.splash_sprite1)
                elif self.board[i][j]==200: 
                    self.splash_sprite2 = arcade.Sprite("splashS.png", ROW_SPACING/100)
                    self.splash_sprite2.center_x = x
                    self.splash_sprite2.center_y = y
                    if self.splash_sprite2 not in self.splash_list:
                        self.splash_list.append(self.splash_sprite2)
                elif self.board[i][j]==1:
                    self.snail_player1.center_x,self.snail_player1.center_y=x,y
                elif self.board[i][j]==2:
                    self.snail_player2.center_x,self.snail_player2.center_y=x,y
        self.splash_list.update()
        self.snail_list.update()

    def get_player1_cord(self):
        for x in range(10):
            for y in range(10):
                if self.board[x][y] == 1:
                    return x,y
    def get_player2_cord(self):
        for x in range(10):
            for y in range(10):
                if self.board[x][y] == 2:
                    return x,y
    def isLegalMove(self,newi,newj,currenti,currentj):
        if (newi+1==currenti and newj==currentj) or (newi-1==currenti and newj==currentj) or (newi==currenti and newj+1==currentj) or (newi==currenti and newj-1==currentj):
            return True
        else:
            return False
        
    def isMovesLeft(self,board):
        check = False
        for i in range(len(board)):
            for j in range(len(board)):
                if (board[i][j] == 0):
                    return True
        return False

    def evaluate(self,board):
        count_p1 = 0
        count_p2 = 0
        for row in range(len(board)):	
            for col in range(len(board)):
                if board[row][col]==100:
                    count_p1+=1
                elif board[row][col]==200:
                    count_p2+=2
        if count_p1>count_p2 and self.timer!=60:
            return 10
        elif count_p2>count_p1 and self.timer!=60:
            return -10
        # Else if none of them have won then return 0
        return 0
    def heuristic(self, board,i,j,player_splash):
        winningChances = 0

        # First Condition
        for x in range(10):
            for y in range(10):
                if self.board[x][y]==player_splash:      #updating score of players each time they make a move
                    winningChances +=1

        # 2nd Condition
        currentRow, currentCol = i,j 

        # If below box is empty
        if currentRow+1 < len(board):
            if board[currentRow+1][currentCol] == 0:
                winningChances += 1  

        # If above box is empty
        if currentRow-1 > 0:
            if board[currentRow-1][currentCol] == 0:
                winningChances += 1
        # If left box is empty
        if currentCol-1 > 0:  
            if board[currentRow][currentCol-1] == 0:
                winningChances += 1
        # If right box is empty
        if currentCol+1 < len(board):  
            if board[currentRow][currentCol+1] == 0:
                winningChances += 1


        # 3rd Condition  
        rangeMin = (len(board)//2) - 3
        rangeMax = (len(board)//2) + 3

        if [rangeMin,rangeMin] <= [currentRow, currentCol] <= [rangeMax,rangeMax]:
            winningChances += 10 


        return winningChances
    def minimax(self, board, depth, isMax,i,j,alpha,beta):
        score = self.evaluate(board)
        # # If Maximizer has won the game return his/her
        # evaluated score
        if (self.isMovesLeft(board) == False or depth==0) :
            if isMax:
                score += self.heuristic(board,i,j,200)
                return -score
            else:
                score += self.heuristic(board,i,j,100)
                return score
        # If there are no more moves and no winner then
        # it is a tie
        

        # If this maximizer's move
        if (isMax) :	
            best = -1000
            out = False          
            previous_move = self.get_player2_cord()
            # Traverse all cells
            for i in range(len(board)) :		
                for j in range(len(board)) :
                    if self.isLegalMove(i,j,previous_move[0],previous_move[1]):
                    # Check if cell is empty
                        if (board[i][j]==0) :
                            board[previous_move[0]][previous_move[1]]=200
                            # Make the move
                            board[i][j] = 2

                            # Call minimax recursively and choose
                            # the maximum value
                            best = max( best, self.minimax(board,depth - 1,not isMax, i, j,alpha,beta))
                            # Undo the move
                            board[i][j] = 0
                            board[previous_move[0]][previous_move[1]]=2
                            alpha = max(alpha, best)
                            if beta<=alpha:
                                out=True
                                break

                        elif (board[i][j] == 200):
                            board[previous_move[0]][previous_move[1]]=200
                            if previous_move[0]+1==i:
                                newMove= self.slide_on_splash(200,previous_move[0],previous_move[1],False,False,True,False)
                            elif previous_move[0]-1==i:
                                newMove= self.slide_on_splash(200,previous_move[0],previous_move[1],False,False,False,True)
                            elif previous_move[1]+1==j:
                                newMove= self.slide_on_splash(200,previous_move[0],previous_move[1],False,True,False,False)
                            elif previous_move[1]-1==j:
                                newMove= self.slide_on_splash(200,previous_move[0],previous_move[1],True,False,False,False)
                            # Make the move
                            i,j = newMove[0],newMove[1]
                            board[i][j] = 2

                            # Call minimax recursively and choose
                            # the minimum value
                            best = max(best, self.minimax(board, depth - 1, not isMax, i, j,alpha,beta))

                            # Undo the move
                            board[i][j] = 200
                            board[previous_move[0]][previous_move[1]]=2
                            alpha = max(alpha, best)
                            if beta<=alpha:
                                out=True
                                break

                if out:
                    break
            return best

        # If this minimizer's move
        else :
            best = 1000
            out = False
            previous_move = self.get_player1_cord()
            # Traverse all cells
            for i in range(len(board)) :		
                for j in range(len(board)) :
                    if self.isLegalMove(i,j,previous_move[0],previous_move[1]):
                        # Check if cell is empty
                        if (board[i][j] == 0):
                            board[previous_move[0]][previous_move[1]]=100
                            # Make the move
                            board[i][j] = 1

                            # Call minimax recursively and choose
                            # the minimum value
                            best = min(best, self.minimax(board, depth - 1, not isMax, i, j,alpha,beta))

                            # Undo the move
                            board[i][j] = 0
                            board[previous_move[0]][previous_move[1]]=1
                            beta = min(beta, best)
                            if beta<=alpha:
                                out=True
                                break
                        elif (board[i][j] == 100):
                            board[previous_move[0]][previous_move[1]]=100
                            if previous_move[0]+1==i:
                                newMove= self.slide_on_splash(100,previous_move[0],previous_move[1],False,False,True,False)
                            elif previous_move[0]-1==i:
                                newMove= self.slide_on_splash(100,previous_move[0],previous_move[1],False,False,False,True)
                            elif previous_move[1]+1==j:
                                newMove= self.slide_on_splash(100,previous_move[0],previous_move[1],False,True,False,False)
                            elif previous_move[1]-1==j:
                                newMove= self.slide_on_splash(100,previous_move[0],previous_move[1],True,False,False,False)
                            # Make the move
                            i,j = newMove[0],newMove[1]
                            board[i][j] = 1

                            # Call minimax recursively and choose
                            # the minimum value
                            best = min(best, self.minimax(board, depth - 1, not isMax, i, j,alpha,beta))

                            # Undo the move
                            board[i][j] = 100
                            board[previous_move[0]][previous_move[1]]=1
                            beta = min(beta, best)
                            if beta<=alpha:
                                out=True
                                break
                if out:
                    break
            return best

# This will return the best possible move for the player
    def findBestMove(self,board,ismax,last_max) :
        bestVal = -1000
        moveVal=  -1000
        bestMove = (-1, -1)

	# Traverse all cells, evaluate minimax function for
	# all empty cells. And return the cell with optimal
	# value.
        for i in range(len(board)) :	
            for j in range(len(board)) :
                if self.isLegalMove(i,j,last_max[0],last_max[1]):

                # Check if cell is empty
                    if (board[i][j] == 0):
                    # Make the move
                        board[last_max[0]][last_max[1]]=200
                        board[i][j] = 2

                        # compute evaluation function for this
                        # move.
                        moveVal = self.minimax(board, 8, ismax,last_max[0],last_max[1],-1000,1000)

                        # Undo the move
                        board[i][j] = 0
                        board[last_max[0]][last_max[1]]=2
                        # If the value of the current ]move is
                        # more than the best value, then update
                        # best/
                    if (moveVal > bestVal) :			
                        bestMove = (i, j)
                        bestVal = moveVal
        if bestMove !=(-1,-1):
            return bestMove
        else:
            for i in range(len(board)) :	
                for j in range(len(board)) :
                    if self.isLegalMove(i,j,last_max[0],last_max[1]):
                        if (board[i][j] == 200):
                        # Make the move
                            board[last_max[0]][last_max[1]]=200
                            board[i][j] = 2

                            # compute evaluation function for this
                            # move.
                            moveVal = self.minimax(board, 8, ismax,last_max[0],last_max[1],-1000,1000)

                            # Undo the move
                            board[i][j] = 200
                            board[last_max[0]][last_max[1]]=2
                        if (moveVal > bestVal):			
                            bestMove = (i, j)
                            bestVal = moveVal
            if last_max[0]+1==bestMove[0]:
                newMove= self.slide_on_splash(200,last_max[0],last_max[1],False,False,True,False)
            elif last_max[0]-1==bestMove[0]:
                newMove= self.slide_on_splash(200,last_max[0],last_max[1],False,False,False,True)
            elif last_max[1]+1==bestMove[1]:
                newMove= self.slide_on_splash(200,last_max[0],last_max[1],False,True,False,False)
            elif last_max[1]-1==bestMove[1]:
                newMove= self.slide_on_splash(200,last_max[0],last_max[1],True,False,False,False)
            return newMove
    def on_mouse_press(self, x, y, _button, _modifiers):   #mouse press functionality, how the game will proceed with each press of mouse button
        column = int(x//(COLUMN_SPACING+2))     #+2 indicates including width og border
        row = int(y//(ROW_SPACING+2))
        if self.player_switch == 1: #if player1 has played its turn switvh to player2 else switch to player1
            x,y = self.get_player1_cord()     #getting the xordinates where player 1 stands
            if x==row:       #if the player has moved vertically
                if y > column and y-1==column:  #if the player has moved in downward direction
                    if self.board[x][y-1]==100:
                        self.board[x][y]=100
                        x,y = self.slide_on_splash(100,x,y,True,False,False,False)
                        self.board[x][y]=1
                    elif(y>0 and (self.board[x][y-1]!=2 and self.board[x][y-1]!=200)):
                        self.board[x][y-1]=1
                        self.board[x][y]=100
                    self.player_switch = 2
                    
                elif y < column and y+1==column:  #if the player has moved in upward direction
                    if self.board[x][y+1]==100:
                        self.board[x][y]=100
                        x,y = self.slide_on_splash(100,x,y,False,True,False,False)
                        self.board[x][y]=1
                    elif(y<9 and (self.board[x][y+1]!=2 and self.board[x][y+1]!=200)):
                        self.board[x][y+1]=1
                        self.board[x][y]=100
                    self.player_switch = 2
                
            elif y==column: #if the player has moved horizontally then the column will remain same
                if x > row and x-1==row: #if the player has moved in left direction
                    if self.board[x-1][y]==100:
                        self.board[x][y]=100
                        x,y = self.slide_on_splash(100,x,y,False,False,False,True)
                        self.board[x][y]=1
                    elif(x>0 and (self.board[x-1][y]!=2 and self.board[x-1][y]!=200)):
                        self.board[x-1][y]=1
                        self.board[x][y]=100
                    self.player_switch = 2
                    

                elif x < row and x+1==row: #if the player has moved in right direction
                    if self.board[x+1][y]==100:
                        self.board[x][y]=100
                        x,y = self.slide_on_splash(100,x,y,False,False,True,False)
                        self.board[x][y]=1
                    elif(x<9 and (self.board[x+1][y]!=2 and self.board[x+1][y]!=200)):
                        self.board[x+1][y]=1
                        self.board[x][y]=100
                    self.player_switch = 2
             #if its turn of player 1 then a splash is drwan at the area he moved to
            
            
    
    def on_key_press(self, key, modifiers): #functionality for keyboard
        if key == arcade.key.F:
                # User hits f. Flip between full and not full screen.
                self.window.set_fullscreen(not self.window.fullscreen)

                # Get the window coordinates. Match viewport to window coordinates
                # so there is a one-to-one mapping.
                self.width, self.height = self.window.get_size()
                self.window.set_viewport(0, self.width, 0, self.height)
                
        if self.player_switch == 1:  #if the recent move is made by player 1
            x,y = self.get_player1_cord()     #getting the xordinates where player 1 stands
            if key==arcade.key.UP:
                if self.board[x+1][y]==100:
                    self.board[x][y]=100
                    x,y = self.slide_on_splash(100,x,y,False,False,True,False)
                    self.board[x][y]=1
                elif(x<9 and (self.board[x+1][y]!=2 and self.board[x+1][y]!=200)):
                    self.board[x+1][y]=1
                    self.board[x][y]=100
                self.player_switch = 2
                    
            if key==arcade.key.DOWN:
                if self.board[x-1][y]==100:
                    self.board[x][y]=100
                    x,y = self.slide_on_splash(100,x,y,False,False,False,True)
                    self.board[x][y]=1

                elif(x>0 and (self.board[x-1][y]!=2 and self.board[x-1][y]!=200)):
                    self.board[x-1][y]=1
                    self.board[x][y]=100
                self.player_switch = 2
                    
            if key==arcade.key.LEFT:
                if self.board[x][y-1]==100:
                    self.board[x][y]=100
                    x,y = self.slide_on_splash(100,x,y,True,False,False,False)
                    self.board[x][y]=1
                elif(y>0 and (self.board[x][y-1]!=2 and self.board[x][y-1]!=200)):
                    self.board[x][y-1]=1
                    self.board[x][y]=100
                self.player_switch = 2
                    
            if key==arcade.key.RIGHT:
                if self.board[x][y+1]==100:
                    self.board[x][y]=100
                    x,y = self.slide_on_splash(100,x,y,False,True,False,False)
                    self.board[x][y]=1
                elif(y<9 and (self.board[x][y+1]!=2 and self.board[x][y+1]!=200)):
                    self.board[x][y+1]=1
                    self.board[x][y]=100 
                self.player_switch = 2
            
            
        

class GameOverView(arcade.View):  #last view of game 
    def __init__(self):
        super().__init__()
        self.score1 = 0
        self.score2 = 0
        self.width, self.height = self.window.get_size()
        self.window.set_viewport(0,  self.width, 0, self.height)
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
    def on_draw(self):
        arcade.start_render()
        backgound = arcade.load_texture("over.jpg")
        scale = self.height/1800
        arcade.draw_scaled_texture_rectangle(self.width/2, self.height/2, backgound, scale, 0)
        arcade.draw_text("Game Over", self.width/2, self.height/2+175,
                         arcade.color.WHITE, font_size=50, anchor_x="center",font_name="Showcard Gothic")
        result = f"Human Scrores:{self.score1}  AI Scores:{self.score2}"  #presenting final scores of each player
        arcade.draw_text(result, self.width/2, self.height/2+100,
                         arcade.color.WHITE, font_size=30, anchor_x="center",font_name="Chiller")
        if self.score1>self.score2:       #decides who win between two players
            arcade.draw_text("Human Wins", self.width/2, self.height/2+10,
                         arcade.color.WHITE, font_size=30, anchor_x="center",font_name="Showcard Gothic")
        elif self.score1<self.score2:
            arcade.draw_text("AI wins", self.width/2, self.height/2+10,
                         arcade.color.WHITE, font_size=30, anchor_x="center",font_name="Showcard Gothic")
        else:
            arcade.draw_text("!!Draw!!", self.width/2, self.height/2+10,
                         arcade.color.WHITE, font_size=30, anchor_x="center",font_name="Showcard Gothic")
        arcade.draw_text("Click to restart", self.width/2, self.height/2-175,   #a restart option at the end of game
                         arcade.color.WHITE, font_size=40, anchor_x="center",font_name="Freestyle Script")
    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
                # User hits f. Flip between full and not full screen.         #this window view can also be flip between full and viceversa
                self.window.set_fullscreen(not self.window.fullscreen)

                # Get the window coordinates. Match viewport to window coordinates
                # so there is a one-to-one mapping.
                self.width, self.height = self.window.get_size()
                self.window.set_viewport(0, self.width, 0, self.height)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView() #if mouse is pressed for restarting the game the game gets back to game view
        self.window.show_view(game_view)
# Main code; program execution strats from here
if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)   #creating an arcade window where views change accordingly
    game = MainView()
    window.show_view(game)
    arcade.run()