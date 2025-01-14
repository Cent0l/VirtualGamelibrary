# Steam Game Library API

Aplikacja umożliwia użytkownikowi wyszukiwanie gier w API Steam, dodawanie gier do biblioteki, przeglądanie biblioteki oraz generowanie rekomendacji gier. Aplikacja została zbudowana w Pythonie z użyciem **FastAPI** i może być uruchamiana w kontenerze Docker.

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

## **Wymagania**

- Python 3.12+
- Docker (opcjonalnie, jeśli chcesz używać kontenerów)
- FastAPI
- Uvicorn
- Aiohttp

## **Instalacja**

1. **Sklonuj repozytorium:**

   ```bash
   git clone https://github.com/username/steam-library-api.git
   cd steam-library-api
