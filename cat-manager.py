import requests
import json
import webbrowser
from pprint import pprint
from enum import IntEnum

header = {"x-api-key": "YOUR_API_KEY"}

Menu = IntEnum("Menu", "zaloguj dodaj ulubione usun")
usrId = ""


def get_random_cat():
    parameters = {"limit": 1}
    try:
        randomCatJson = requests.get(
            "https://api.thecatapi.com/v1/images/search", parameters, headers=header
        ).json()
    except json.decoder.JSONDecodeError:
        print("Niepoprawny format", randomCatJson.text)
    return randomCatJson[0]


def add_to_favorites(catId, usrId):

    headers = {
        'content-type': "application/json",
        'x-api-key': "a794cc6e-d62c-4ae9-8ac4-bd3cda7fea08"
    }

    usrCatParameters = {"image_id": catId, "sub_id": usrId}
    try:
        addToFavorites = requests.post("https://api.thecatapi.com/v1/favourites", data=json.dumps(
            {"image_id": str(catId), "sub_id": str(usrId)}), headers=headers).json()

    except json.decoder.JSONDecodeError:
        print("Niepoprawny format", addToFavorites.text)
    print("Dodano do ulubionych")
    return addToFavorites


def view_favorites(usrId):

    try:
        FavoriteCatsJson = requests.get(
            "https://api.thecatapi.com/v1/favourites", headers=header
        ).json()
    except json.decoder.JSONDecodeError:
        print("Niepoprawny format", FavoriteCatsJson.text)
    return FavoriteCatsJson


def delete_favorite(usrId, favId):
    try:
        deleteFavorite = requests.delete(
            "https://api.thecatapi.com/v1/favourites/" + favId, headers=header).json()
        print(deleteFavorite)
    except json.decoder.JSONDecodeError:
        print("Niepoprawny format", deleteFavorite.text)
    return deleteFavorite


def view_favorite_ids(view_favorites, usrId):
    favoriteCats = view_favorites(usrId)
    favoriteIds_dict = {cats["id"]: cats["image"]["url"]
                        for cats in favoriteCats}
    return favoriteIds_dict


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
            if (
                menuChoice == Menu.zaloguj
                or menuChoice == Menu.dodaj
                or menuChoice == Menu.ulubione
                or menuChoice == Menu.usun
            ):
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
        # sprawdzamy czy użytkownik jest zalogowany
        if usrId == "":
            print("Musisz się najpierw zalogować")
            usrId = input("Podaj swoje imię: ")
        # pobieramy losowego kota
        randomCatJson = get_random_cat()
        catId = randomCatJson["id"]
        catImgUrl = randomCatJson["url"]
        # otwieramy kota w nowej zakładce
        webbrowser.open_new_tab(randomCatJson["url"])
        print()
        # zalogowany użytkownik dodaje kotka do ulubionych
        addFavorite = input("Dodać do ulubionych? T/N: ").upper()
        if addFavorite == "T":
            add_to_favorites(catId, usrId)
        else:
            print("Trudno")
        print()
        continue

    # sprawdzamy ulubione
    if menuChoice == Menu.ulubione:
        # sprawdzamy czy użytkownik jest zalogowany
        if usrId == "":
            print("Musisz się najpierw zalogować")
            usrId = input("Podaj swoje imię: ")
        print("Poniżej ulubione koty użytkownika", usrId, "w formacie ID: URL")
        favoriteIds_dict = view_favorite_ids(view_favorites, usrId)
        pprint(favoriteIds_dict)
        if favoriteIds_dict != {}:
            print()
            openInBrowser = input(
                "Chcesz otworzyć koty w przeglądarce? T/N: ").upper()
            if openInBrowser == "T":
                for favIds in favoriteIds_dict:
                    webbrowser.open_new_tab(favoriteIds_dict[favIds])
                print()
                continue
            else:
                print()
                continue
        else:
            print()
            continue

    # usuwamy ulubione
    if menuChoice == Menu.usun:
        # sprawdzamy czy użytkownik jest zalogowany
        if usrId == "":
            print("Musisz się najpierw zalogować")
            usrId = input("Podaj swoje imię: ")
        deletefavorites = input("Czy na pewno usuwać ulubione? T/N: ").upper()
        if deletefavorites == "T":
            deleteAll = input(
                "Czy chcesz usunąć wszystkie ulubione? T/N: ").upper()
            if deleteAll == "T":
                for favIds in view_favorite_ids(view_favorites, usrId):
                    delete_favorite(usrId, str(favIds))
                print("Usunięto wszystkie ulubione")
                print()
                continue
            else:
                favId = input("Podaj ID do usunięcia: ")
                delete_favorite(usrId, favId)
                print("Usunięto kota z ulubionych")
                print()
                continue
        else:
            print("Całe szczęście")
        print()
        continue
