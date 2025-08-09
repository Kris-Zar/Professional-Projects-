import pandas as pd
import matplotlib.pyplot as plt


primeDf = pd.read_csv("Prime.csv")
netflixDf = pd.read_csv("Netflix.csv")


movies = [netflixDf[netflixDf["type"] == "Movie"], primeDf[primeDf["type"] == "Movie"]]
tvShows = [netflixDf[netflixDf["type"] == "TV Show"], primeDf[primeDf["type"] == "TV Show"]]

print("*" * 43, "Welcome to Netflix Vs Amazon Prime Content Analysis", "*" * 43)
print("For Following Analysis Enter Code:" )
print(
    "Code: Operations\n",
    "1. Show Content Distribution\n",
    "2. Show Content Details\n",
    "3. Show Rating Distribution\n",
    "4. Show Yearly Release Trends\n"
)

choice = int(input("Enter Code: "))

if choice == 1:
   
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    axs[0].pie([len(movies[0]), len(tvShows[0])], labels=["Movies", "TV Shows"], autopct="%1.1f%%")
    axs[1].pie([len(movies[1]), len(tvShows[1])], labels=["Movies", "TV Shows"], autopct="%1.1f%%")

    axs[0].set_title("Netflix")
    axs[1].set_title("Amazon Prime")
    fig.suptitle("Content Type Distribution")
    plt.show()

elif choice == 2:
   
    print("Netflix:")
    print(netflixDf[["title", "type", "release_year", "rating"]])
    print("\nAmazon Prime:")
    print(primeDf[["title", "type", "release_year", "rating"]])

elif choice == 3:

    netflix_rating_counts = netflixDf["rating"].value_counts().sort_values(ascending=False)
    prime_rating_counts = primeDf["rating"].value_counts().sort_values(ascending=False)

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    axs[0].bar(netflix_rating_counts.index, netflix_rating_counts.values, color='skyblue', alpha=0.7)
    axs[1].bar(prime_rating_counts.index, prime_rating_counts.values, color='lightgreen', alpha=0.7)

    axs[0].set_title("Netflix Rating Distribution")
    axs[1].set_title("Amazon Prime Rating Distribution")

    for ax in axs:
        ax.set_xlabel("Rating")
        ax.set_ylabel("Number of Titles")
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

elif choice == 4:

    netflix_year_counts = netflixDf["release_year"].value_counts().sort_index()
    prime_year_counts = primeDf["release_year"].value_counts().sort_index()

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    axs[0].plot(netflix_year_counts.index, netflix_year_counts.values, marker='o', color='skyblue', label="Netflix")
    axs[1].plot(prime_year_counts.index, prime_year_counts.values, marker='o', color='lightgreen', label="Amazon Prime")

    axs[0].set_title("Netflix Yearly Release Trend")
    axs[1].set_title("Amazon Prime Yearly Release Trend")

    for ax in axs:
        ax.set_xlabel("Release Year")
        ax.set_ylabel("Number of Titles")
        ax.legend()

    plt.tight_layout()
    plt.show()

else:
    print("Invalid Code")
