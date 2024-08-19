import mysql.connector, os, time
config = {
    'user': 'root',      
    'password': '',    
    'host': 'localhost', 
    'database': 'probar' 
}

conexion = mysql.connector.connect(**config)

cursor = conexion.cursor()

def clear_terminal():
    os.system('cls')
def pause():
    time.sleep(3)

def main():
    current_session = welcome_menu()
    if isinstance(current_session, Sesion):
        logged_in_menu(current_session)

def welcome_menu():
    while True:
        try:    
            print(f"         Watcha wanna do?")
            print(f"|----------          ---------|")
            print(f"| Login                      1|")
            print(f"| Sign up                    2|")
            print(f"| Exit                       3|")
            print(f"|----------          ---------|")
            action = int(input(f": "))

            match action:
                case 1:
                    account = login()
                    if account:
                        print(f"Logged in successfully!")
                        pause()
                        return account
                case 2:
                    user, password = ask_user_pass()
                    sign_up(user, password)
                case 3:
                    break
                case _:
                    raise ValueError
        except ValueError:
            print(f"Enter a valid option")

def logged_in_menu(current_session):    
    clear_terminal()
    while True:
        try:    
            print(f"         Watcha wanna do?")
            print(f"|----------          ---------|")
            print(f"| Store                      1|")
            print(f"| Library                    2|")
            print(f"| Account settings           3|")
            print(f"| Exit                       4|")
            print(f"|----------          ---------|")
            action = get_in()

            match action:
                case 1:
                  store_menu(current_session)  
                case 2:
                    library_menu(current_session)
                case 3:
                    pass
                case 4:
                    break
                case _:
                    print(f"There's no such option")

        except KeyError as e:
            print(f"{e}")

def library_menu(current_session):
    while True:
        try:
            clear_terminal()
            games = current_session.go_to_library()
            
            print(f"         Watcha wanna do?")
            print(f"|----------          ---------|")
            print(f"| Play                       1|")
            print(f"| Remove game                2|")
            print(f"| Add from purchases         3|")
            print(f"| View game                  4|")
            print(f"| Return                     5|")
            print(f"|----------          ---------|")

            action = get_in()
            match action:
                case 1: #Play
                    game_selected = select_game(games)
                    current_session.play_game(game_selected)
                case 2: #Remove
                    game_selected = select_game(games)
                    current_session.remove_from_library(game_selected.game_id)
                    print(f"{game_selected.game_name} removed successfully!")
                case 3: #Add from purchases
                    games_but_libray = current_session.check_purchases_but_library()
                    if games_but_libray:
                        game_selected = select_game(games_but_libray)
                        current_session.add_to_library(game_selected)
                    else:
                        print(f"There're no games to add from purchases :c")
                case 4: #View game
                    pass
                case 5:
                    break
                case _:
                    print(f"There's no such option")

        except Exception as e:
            print(f"{e}")

def store_menu(current_session):
    while True:
        try:
            clear_terminal()
            query = "SELECT * FROM `store`"
            cursor.execute(query)
            games = cursor.fetchall()
            game_list = create_game_list(games)   
            print(f"Available games: ")
            for game in game_list:
                separador()
                game.show_in_store()

            print(f"         Watcha wanna do?")
            print(f"|----------          ---------|")
            print(f"| Add to wishlist            1|")
            print(f"| Buy a game                 2|")
            print(f"| Return                     3|")
            print(f"|----------          ---------|")
  
            action = get_in()
            match action:
                case 1:
                    game_selected = select_game(game_list)
                    current_session.add_to_wishlist(game_selected)
                case 2:
                    game_selected = select_game(game_list)
                    current_session.buy_game(game_selected)
                case 3:
                    break
                case _:
                    print(f"There's no such option")
        
        except Exception as e:
                print(f"{e}")     

def select_game(game_list):
    clear_terminal()
    print(f"Choose the game:")
    for idx, game in enumerate(game_list):
        print(f"| {game.game_name} - {idx}|")
        print(f"|----------          ---------|")
    game_index = get_in()
    game_selected = game_list[game_index]
    return game_selected

def ask_user_pass():
    clear_terminal()
    user = (input(f"Enter your username: "))
    password = (input(f"Enter your password: "))
    return user, password

def sign_up(user, password): 
    crear_acc = "INSERT INTO `cuentas` (`name`, `password`) VALUES (%s, %s)"
    try:
        cursor.execute(crear_acc, (user, password))
        conexion.commit()
        print(f"Account created successfully!")
        pause()
    except Exception as e:
        print(f"An error occured: {e}")
        pause() 

def consulta_login(user, password):
    search_acc = "SELECT * FROM `cuentas` WHERE name = %s AND password = %s"
    cursor.execute(search_acc, (user, password))
    data = cursor.fetchone()
    if data:
        identificador, nombre_obtenido, info_obtenida, contra_obtenida = data
        sesion_iniciado = Sesion(identificador, nombre_obtenido, info_obtenida, contra_obtenida)
        return sesion_iniciado
    else:
        print(f"Usario o contraseña incorrectos")
        return None

class Sesion:
    def __init__(self, id, nickname, info, password):
        self.id = id
        self.nickname = nickname
        self.info = info
        self.password = password
        self.library = Library(self.id)

    def add_to_wishlist(self, game_selected):
        check = "SELECT COUNT(*) FROM wishlist WHERE juego = %s AND jugador = %s"
        cursor.execute(check, (game_selected.game_id, self.id))
        result = cursor.fetchone()
        if result[0] > 0:
            print(f"{game_selected.game_name} is already added to {self.nickname}'s wishlist")
            pause()
        else:
            query = "INSERT INTO `wishlist`(`juego`, `jugador`) VALUES (%s, %s)"
            try:
                cursor.execute(query, (game_selected.game_id, self.id))
                conexion.commit()
                print(f"{game_selected.game_name} added to {self.nickname}'s wishlist")
                pause()
            except Exception as e:
                print(f"An error occured: {e}")
                pause()      
   
    def go_to_library(self):
        print(f"{self.nickname}' library: ")
        game_list = self.library.show_library()
        return game_list

    def buy_game(self, game_selected):
        purchase = Purchase(self.id, game_selected.game_id, game_selected.game_price, game_selected.game_name)
        purchase.record_purchase()
        self.library.add_game(game_selected)

    def play_game(self, game_selected):
        print(f"You played {game_selected.game_name}!")
        pause()
    
    def remove_from_library(self, game_id):
        self.library.remove_game(game_id)

    def check_purchases_but_library(self):
        games = self.library.not_in_library()
        return games
    
    def add_to_library(self, game):
        self.library.add_game(game)

class Purchase:
    def __init__(self, user_id, game_id, game_price, game_name):
        self.user_id = user_id
        self.game_id = game_id
        self.game_price = game_price
        self.game_name = game_name

    def record_purchase(self):
        check = "SELECT COUNT(*) from purchases WHERE user_id = %s AND game_id = %s"
        cursor.execute(check, (self.user_id, self.game_id))
        result = cursor.fetchone()
        if result[0] > 0:
            print(f"{self.game_name} has been already purchased")
            pause()
        else:
            query = "INSERT INTO purchases (game_id, user_id, price) VALUES (%s, %s, %s)"
            try:
                cursor.execute(query, (self.game_id, self.user_id, self.game_price))
                conexion.commit()
                print(f"{self.game_name} purchased successfully!")
                pause()
            except Exception as e:
                print(f"An error occurred: {e}")
                pause()

def get_in():
    while True:
        try:
            action = int(input(f": "))
            return action
        except ValueError:
            print(f"Enter a valid option")
        except Exception as e:
            print(f"Error: {e}")


def create_game_list(games):
    game_list = []
    for game in games:                
        game_name, game_size, game_price, game_info, game_id = game
        game_created = Game(game_name, game_size, game_price, game_info, game_id)
        game_list.append(game_created)
    return game_list

class Library:
    def __init__(self, user_id):
        self.user_id = user_id
        self.games = self.fetch_games_from_db() #No

    def fetch_games_from_db(self): #No usado
        query = "SELECT game_id FROM library WHERE user_id = %s"
        cursor.execute(query, (self.user_id,))
        return cursor.fetchall()
    
    def show_library(self):
        query = "SELECT store.* FROM library JOIN store ON library.game_id = store.game_id WHERE user_id = %s"
        cursor.execute(query, (self.user_id,))
        library = cursor.fetchall()
        
        if library:
            game_list = create_game_list(library)
            for game in game_list:
                game.show_in_library()
            return game_list
        
        else:
            print(f"Your library is empty :c")
        pause()

    def not_in_library(self):
        query = "SELECT store.* FROM purchases JOIN store ON purchases.game_id = store.game_id LEFT JOIN library ON purchases.game_id = library.game_id and purchases.user_id = library.user_id WHERE purchases.user_id = %s AND library.game_id IS NULL"
        cursor.execute(query, (self.user_id,))
        games_not_in_libray = cursor.fetchall()
        
        game_list = create_game_list(games_not_in_libray)
        return game_list

    def add_game(self, game):
        check = "SELECT COUNT(*) from library WHERE user_id = %s AND game_id = %s"
        cursor.execute(check, (self.user_id, game.game_id))
        result = cursor.fetchone()
        if result[0] > 0:
            print(f"{game.game_name} has been already added to the library")
            pause()
        else:
            query = "INSERT INTO library (game_id, user_id) VALUES (%s, %s)"
            try:
                cursor.execute(query, (game.game_id, self.user_id))
                conexion.commit()
                print(f"{game.game_name} added to the library.")
                pause()
            except Exception as e:
                print(f"An error occurred: {e}")
                pause()

    def remove_game(self, game_id):
        query = "DELETE FROM library WHERE user_id = %s AND game_id = %s"
        try:
            cursor.execute(query, (self.user_id, game_id))
            conexion.commit()
            print(f"Game with ID {game_id} removed from the library.")
        except Exception as e:
            print(f"An error occurred: {e}")
            pause()


class Game:
    def __init__(self, game_name, game_size, game_price, game_info, game_id):
        self.game_name = game_name
        self.game_size = game_size
        self.game_price = game_price
        self.game_info = game_info
        self.game_id = game_id
    
    def show_in_store(self):
        print(f"{self.game_name} | size: {self.game_size} gb | price {self.game_price} USD |")
        print(f"Info: {self.game_info}")

    def show_in_library(self):
        print(f"{self.game_name}")
        print(f"size: {self.game_size}")

    def show_in_purchases(self):
        print(f"{self.game_name}")
        print(f"size: {self.game_size}")


def login():
    user, password = ask_user_pass()
    sesión = consulta_login(user, password)
    return sesión

def separador():
    print(f"---------------------")

main()