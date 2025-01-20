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

## **Dostępne Endpointy**
| Metoda  | Endpoint                           | Opis |
|---------|------------------------------------|------|
| **GET** | `/games`                          | Pobiera listę wszystkich dostępnych gier z API Steam. |
| **GET** | `/games/{appid}`                   | Pobiera informacje o grze na podstawie `appid`. |
| **GET** | `/game/search?name={nazwa}`        | Wyszukuje gry na podstawie nazwy lub jej części. |
| **GET** | `/games/{appid}/details`           | Pobiera szczegółowe informacje o grze na podstawie `appid`. |
| **GET** | `/games/{appid}/news`              | Pobiera newsy dla gry na podstawie `appid`. |
| **GET** | `/games/{appid}/recommendations`   | Generuje rekomendacje gier na podstawie podobieństwa nazw. |
| **POST** | `/library/adde/{appid}`           | Dodaje istniejącą grę do biblioteki użytkownika na podstawie `appid`. |
| **POST** | `/library/addc/{name}`            | Dodaje własną (customową) grę do biblioteki użytkownika. |
| **DELETE** | `/library/delete/{appid}`       | Usuwa grę z biblioteki na podstawie `appid`. |
| **GET** | `/library`                         | Pobiera listę wszystkich gier w bibliotece użytkownika. |

