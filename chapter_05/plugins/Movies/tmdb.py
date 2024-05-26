import inspect

import requests
from semantic_kernel.functions import kernel_function


# use for debugging, a regular decorator did not work
def print_function_call():
    # Retrieve the current frame
    frame = inspect.currentframe()

    # Get the calling frame (one level up)
    calling_frame = frame.f_back

    # Extract the function name and arguments
    func_name = calling_frame.f_code.co_name
    args, _, _, values = inspect.getargvalues(calling_frame)

    # Print function details
    print(f"Function name: {func_name}")
    print("Arguments:")
    for arg in args:
        if arg != "self":
            print(f"  {arg} = {values[arg]}")


class TMDbService:
    def __init__(self):
        # enter your TMDb API key here
        self.api_key = "7d7718ef8b5101ba4c1bb6a0f3e127ba"
        pass

    @kernel_function(
        description="Gets the movie genre ID for a given genre name",
        name="get_movie_genre_id",
        # input_description="The movie genre name of the genre_id to get",
    )
    def get_movie_genre_id(self, genre_name: str) -> str:
        """
        Function to get the genre ID for a given genre name from TMDb.

        Parameters:
        - api_key: Your TMDb API key.
        - genre_name: The name of the genre for which you want the ID.

        Returns:
        - The ID of the genre or None if the genre is not found.
        """
        print_function_call()
        base_url = "https://api.themoviedb.org/3"
        endpoint = f"{base_url}/genre/movie/list?api_key={self.api_key}&language=en-US"

        response = requests.get(endpoint)
        if response.status_code == 200:
            genres = response.json()["genres"]
            for genre in genres:
                if genre_name.lower() in genre["name"].lower():
                    return str(genre["id"])
        return None

    @kernel_function(
        description="Gets the TV show genre ID for a given genre name",
        name="get_tv_show_genre_id",
        # input_description="The TV show genre name of the genre_id to get",
    )
    def get_tv_show_genre_id(self, genre_name: str) -> str:
        """
        Function to get the genre ID for a given genre name from TMDb.

        Parameters:
        - api_key: Your TMDb API key.
        - genre_name: The name of the genre for which you want the ID.

        Returns:
        - The ID of the genre or None if the genre is not found.
        """
        print_function_call()
        base_url = "https://api.themoviedb.org/3"
        endpoint = f"{base_url}/genre/tv/list?api_key={self.api_key}&language=en-US"

        response = requests.get(endpoint)
        if response.status_code == 200:
            genres = response.json()["genres"]
            for genre in genres:
                if genre_name.lower() in genre["name"].lower():
                    return str(genre["id"])
        return None

    @kernel_function(
        description="Gets a list of currently playing movies for a given genre",
        name="get_top_movies_by_genre",
        # input_description="The genre name of the movies to get",
    )
    def get_top_movies_by_genre(self, genre_name: str) -> str:
        print_function_call()
        genre_id = self.get_movie_genre_id(genre_name)
        if genre_id:
            base_url = "https://api.themoviedb.org/3"
            # Step 1: Fetch currently playing movies
            playing_movies_endpoint = (
                f"{base_url}/movie/now_playing?api_key={self.api_key}&language=en-US"
            )
            response = requests.get(playing_movies_endpoint)
            if response.status_code != 200:
                return ""

            playing_movies = response.json()["results"]

            # Step 2: Filter movies by the specified genre
            for movie in playing_movies:
                movie["genre_ids"] = [str(genre_id) for genre_id in movie["genre_ids"]]
            filtered_movies = [
                movie for movie in playing_movies if genre_id in movie["genre_ids"]
            ][:10]
            results = ", ".join([movie["title"] for movie in filtered_movies])
            return results
        else:
            return ""

    @kernel_function(
        description="Gets a list of top tv shows for a given genre",
        name="get_top_tv_shows_by_genre",
        # input_description="The genre name of the tv shows to get",
    )
    def get_top_tv_shows_by_genre(self, genre_name: str) -> str:
        print_function_call()
        genre_id = self.get_tv_show_genre_id(genre_name)
        if genre_id:
            base_url = "https://api.themoviedb.org/3"
            # Step 1: Fetch top-rated TV shows
            top_rated_shows_endpoint = (
                f"{base_url}/tv/top_rated?api_key={self.api_key}&language=en-US"
            )
            response = requests.get(top_rated_shows_endpoint)
            if response.status_code != 200:
                return ""

            top_rated_shows = response.json()["results"]

            # Step 2: Filter shows by the specified genre
            for show in top_rated_shows:
                show["genre_ids"] = [str(genre_id) for genre_id in show["genre_ids"]]
            filtered_shows = [
                show for show in top_rated_shows if genre_id in show["genre_ids"]
            ]
            results = ", ".join([show["name"] for show in filtered_shows])
            return results
        else:
            return ""

    @kernel_function(
        description="Gets a list of movie genres",
        name="get_movie_genres",
    )
    def get_movie_genres(self) -> str:
        print_function_call()
        base_url = "https://api.themoviedb.org/3"
        endpoint = f"{base_url}/genre/movie/list?api_key={self.api_key}&language=en-US"

        response = requests.get(endpoint)
        if response.status_code == 200:
            genres = response.json()["genres"]
            results = ", ".join([genre["name"] for genre in genres])
            return results
        return ""

    @kernel_function(
        description="Gets a list of TV show genres",
        name="get_tv_show_genres",
    )
    def get_tv_show_genres(self) -> str:
        print_function_call()
        base_url = "https://api.themoviedb.org/3"
        endpoint = f"{base_url}/genre/tv/list?api_key={self.api_key}&language=en-US"

        response = requests.get(endpoint)
        if response.status_code == 200:
            genres = response.json()["genres"]
            results = ", ".join([genre["name"] for genre in genres])
            return results
        return ""
