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
            print(f"| Friends                    3|")
            print(f"| Account settings           4|")
            print(f"| Exit                       5|")
            print(f"|----------          ---------|")
            action = int(input(f": "))

            match action:
                case 1:
                  store_menu(current_session)  
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    break
                case _:
                    raise KeyError(f"There's no such option")
        except ValueError:
            print(f"Enter a valid option")
        except KeyError as e:
            print(f"{e}")
    
def store_menu(current_session):
    while True:
        try:
            clear_terminal()
            game_list = []
            query = "SELECT * FROM `store`"
            cursor.execute(query)
            games = cursor.fetchall()   
            print(f"Available games: ")
            for i in games:
                separador()
                game_name, game_size, game_price, game_info, game_id = i
                game_in_store = Game(game_name, game_size, game_price, game_info, game_id)
                game_in_store.show_in_store()
                game_list.append(game_in_store)
            print(f"         Watcha wanna do?")
            print(f"|----------          ---------|")
            print(f"| Add to wishlist            1|")
            print(f"| Buy a game                 2|")
            print(f"| Return                     3|")
            print(f"|----------          ---------|")
  
            action = int(input(f": "))
            match action:
                case 1:
                    game_selected = select_game(game_list)
                    current_session.add_to_wishlist(game_selected)
                case 2:
                    pass
                case 3:
                    break
                case _:
                    raise KeyError(f"There's no such option")
        except ValueError:
                print(f"Enter a valid option")
        except KeyError as e:
                print(f"{e}")


# def add_to_wishlist(game_selected, current_session):
#     query = "INSERT INTO `wishlist`(`juego`, `jugador`) VALUES (%s, %s)"
#     try:
#         cursor.execute(query, (game_selected.game_id, current_session.id))
#         conexion.commit()
#         print(f"{game_selected.game_name} added to wishlist")
#         pause()
#     except Exception as e:
#         print(f"An error occured: {e}")         

def select_game(game_list):
    clear_terminal()
    print(f"Choose the game:")
    for idx, game in enumerate(game_list):
        print(f"| {game.game_name} - {idx}|")
        print(f"|----------          ---------|")
    game_index = int(input(f": "))
    game_selected = game_list[game_index]
    return game_selected

def ask_user_pass():
    clear_terminal()
    user = str(input(f"Enter your username: "))
    password = str(input(f"Enter your password: "))
    return user, password

def sign_up(user, password):
    
    crear_acc = "INSERT INTO `cuentas` (`nombre`, `contraseña`) VALUES (%s, %s)"
    try:
        cursor.execute(crear_acc, (user, password))
        conexion.commit()
        print(f"Account created successfully!")
        pause()
    except Exception as e:
        print(f"An error occured: {e}") 

def crear_tabla():
 crear_tabla = """
 CREATE TABLE IF NOT EXISTS cuentas (
     id INT AUTO_INCREMENT PRIMARY KEY,
     nombre VARCHAR(100),
     info VARCHAR(100),
     contraseña VARCHAR(50)
 )
 """
 cursor.execute(crear_tabla)

def consulta_login(usuario, contraseña):
    buscar_acc = f"SELECT * FROM `cuentas` WHERE nombre = '{usuario}' AND contraseña = '{contraseña}'"
    cursor.execute(buscar_acc)
    datos = cursor.fetchone()
    if datos:
        identificador, nombre_obtenido, info_obtenida, contra_obtenida = datos
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

    def add_to_wishlist(self, game_selected):
        query = "INSERT INTO `wishlist`(`juego`, `jugador`) VALUES (%s, %s)"
        try:
            cursor.execute(query, (game_selected.game_id, self.id))
            conexion.commit()
            print(f"{game_selected.game_name} added to {self.nickname}'s wishlist")
            pause()
        except Exception as e:
            print(f"An error occured: {e}")
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

def login():
    user, password = ask_user_pass()
    sesión = consulta_login(user, password)
    return sesión

def separador():
    print(f"---------------------")

main()

#if cuenta:
#    print(f"Sesión iniciada correctamente")
#    print(f"Usuario: {cuenta.nombre}")
#    print(f"Datos: {cuenta.info}")