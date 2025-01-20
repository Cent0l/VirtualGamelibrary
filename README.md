# Steam Game Library API

Aplikacja umożliwia użytkownikowi wyszukiwanie gier w API Steam, dodawanie gier do biblioteki, przeglądanie biblioteki oraz generowanie rekomendacji gier.

---

## **Funkcjonalności**

- **Pobieranie listy dostępnych gier** z API Steam.
- **Wyszukiwanie gier** na podstawie nazwy lub `appid`.
- **Dodawanie gier do biblioteki**:
  - Istniejących gier z API Steam.
  - Własnych „customowych” gier podanych przez użytkownika.
- **Wyświetlanie zawartości biblioteki użytkownika**.
- **Usuwanie gier z biblioteki**.
- **Generowanie rekomendacji gier** na podstawie podobieństwa nazw.
- **Pobieranie szczegółowych informacji o grach**.
- **Pobieranie wiadomości o grach** z API Steam.

---

## **Dostępne endpointy**

| Metoda  | Endpoint                            | Opis |
|---------|-------------------------------------|------|
| `GET`   | `/games`                            | Pobranie listy wszystkich gier |
| `GET`   | `/games/{appid}`                    | Wyszukiwanie gry po `appid` |
| `GET`   | `/game/search?name=<nazwa>`         | Wyszukiwanie gier po nazwie |
| `GET`   | `/games/{appid}/details`            | Pobranie szczegółowych informacji o grze |
| `GET`   | `/games/{appid}/news`               | Pobranie newsów o grze |
| `GET`   | `/games/{appid}/recommendations`    | Rekomendacje podobnych gier |
| `POST`  | `/library/existing`                 | Dodanie istniejącej gry do biblioteki |
| `POST`  | `/library/custom`                   | Dodanie własnej gry do biblioteki |
| `DELETE`| `/library/{appid}`                  | Usunięcie gry z biblioteki |
| `GET`   | `/library`                          | Pobranie listy gier w bibliotece |

