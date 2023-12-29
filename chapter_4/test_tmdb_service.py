import semantic_kernel as sk
from skills.Movies.tmdb import TMDbService


async def main():
    # Initialize the kernel
    kernel = sk.Kernel()
    # Add a text or chat completion service using either:
    # kernel.add_text_completion_service()
    # kernel.add_chat_service()

    # Import the MovieOracle.
    tmdb_service = kernel.import_skill(TMDbService(), skill_name="TMDbService")

    # Test the function with the inputs.
    result = await kernel.run_async(
        #uncomment the line to test the function
        #tmdb_service["get_movie_genre_id"],
        #tmdb_service["get_tv_show_genre_id"],
        #tmdb_service["get_top_movies_by_genre"],
        tmdb_service["get_top_tv_shows_by_genre"],
        #tmdb_service["get_movie_genres"],
        #tmdb_service["get_tv_show_genres"],
        input_str="action",
    )

    print(result)

# Run the main function
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())