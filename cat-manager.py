import requests
import json
import webbrowser
from pprint import pprint
from enum import IntEnum

header = {
        "x-api-key": "[YOUR API KEY]"
        }

Menu = IntEnum("Menu", "zaloguj dodaj ulubione usun")
usrId = ""

def get_random_cat():
    parameters = {
            "limit": 1
            }
    try:
        allCatsJson = requests.get("https://api.thecatapi.com/v1/images/search", parameters, headers = header).json()
    except json.decoder.JSONDecodeError:
        print("Niepoprawny format", allCatsJson.text)
    return allCatsJson

def add_to_favourites(catId, usrId):
    usrCatParameters = {
                "image_id": catId,
                "sub_id": usrId
                }
    try:
        addToFavourites = requests.post("https://api.thecatapi.com/v1/favourites", json = usrCatParameters, headers = header).json()
    except json.decoder.JSONDecodeError:
        print("Niepoprawny format", addToFavourites.text)
    print("Dodano do ulubionych")
    return addToFavourites

def view_favourites(usrId):
    parameters = {
                "limit": 100,
                "sub_id": usrId
                }
    try:
        FavouriteCatsJson = requests.get("https://api.thecatapi.com/v1/favourites", parameters, headers = header).json()
    except json.decoder.JSONDecodeError:
        print("Niepoprawny format", FavouriteCatsJson.text)
    return FavouriteCatsJson

def delete_favourite(usrId, favId):
    try:
        deleteFavourite = requests.delete("https://api.thecatapi.com/v1/favourites/" + favId, headers = header).json()
    except json.decoder.JSONDecodeError:
        print("Niepoprawny format", deleteFavourite.text)
    return deleteFavourite

def view_favourite_ids(view_favourites, usrId):
    favouriteCats = view_favourites(usrId)
    favouriteIds_dict = {cats["id"]: cats["image"]["url"]
                        for cats in favouriteCats
    }
    return favouriteIds_dict

while True:
    while True:
        if usrId != "":
            print("Witaj", usrId)
        try:
            print("Wybierz co chcesz zrobić:")
            if usrId != "":
                True
            else:
                print("1. Zaloguj się")   
            print("2. Wylosuj kota i dodaj do ulubionych")
            print("3. Pokaż ulubione")
            print("4. Usuń kota z listy ulubionych")
            menuChoice = int(input())
            if menuChoice == Menu.zaloguj or menuChoice == Menu.dodaj or menuChoice == Menu.ulubione or menuChoice == Menu.usun:
                break
            else:
                print("Nieprawidłowy wybór. Spróbuj ponownie wpisując samą cyfrę")
                print()
                continue
        except:
            print("Nieprawidłowy wybór. Spróbuj ponownie wpisując samą cyfrę")
            print()
            continue

    if menuChoice == Menu.zaloguj:
        usrId = input("Podaj swoje imię: ")
        print()
        continue

    if menuChoice == Menu.dodaj:
        #sprawdzamy czy użytkownik jest zalogowany
        if usrId == "":
            print("Musisz się najpierw zalogować")
            usrId = input("Podaj swoje imię: ")
        # pobieramy losowego kota
        allCatsJson = get_random_cat()
        catId = allCatsJson[0]["id"]
        catImgUrl = allCatsJson[0]["url"]
        # otwieramy kota w nowej zakładce
        webbrowser.open_new_tab(allCatsJson[0]["url"])
        print()
        #zalogowany użytkownik dodaje kotka do ulubionych
        addFavourite = input("Dodać do ulubionych? T/N: ").upper()
        if addFavourite == "T":
            add_to_favourites(catId, usrId)
        else:
            print("Trudno")
        print()
        continue

    #sprawdzamy ulubione
    if menuChoice == Menu.ulubione:
        #sprawdzamy czy użytkownik jest zalogowany
        if usrId == "":
            print("Musisz się najpierw zalogować")
            usrId = input("Podaj swoje imię: ")
        print("Poniżej ulubione koty użytkownika", usrId, "w formacie ID: URL")
        favouriteIds_dict = view_favourite_ids(view_favourites, usrId) 
        pprint(favouriteIds_dict)
        if favouriteIds_dict != {}:
            print()
            openInBrowser = input("Chcesz otworzyć koty w przeglądarce? T/N: ").upper()
            if openInBrowser == "T":
                for favIds in favouriteIds_dict:
                    webbrowser.open_new_tab(favouriteIds_dict[favIds])
                print()
                continue
            else:
                print()
                continue
        else:
            print()
            continue

    #usuwamy ulubione
    if menuChoice == Menu.usun:
        #sprawdzamy czy użytkownik jest zalogowany
        if usrId == "":
            print("Musisz się najpierw zalogować")
            usrId = input("Podaj swoje imię: ")
        deleteFavourites = input("Czy na pewno usuwać ulubione? T/N: ").upper()
        if deleteFavourites == "T":
            deleteAll = input("Czy chcesz usunąć wszystkie ulubione? T/N: ").upper()
            if deleteAll == "T":
                for favIds in view_favourite_ids(view_favourites, usrId):
                    delete_favourite(usrId, str(favIds))
                print("Usunięto wszystkie ulubione")
                print()
                continue
            else:
                favId = input("Podaj ID do usunięcia: ")
                delete_favourite(usrId, favId)
                print("Usunięto kota z ulubionych")
                print()
                continue
        else:
            print("Całe szczęście")
        print()
        continue