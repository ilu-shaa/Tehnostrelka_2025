import omdb
import csv
import time
import requests
import os

API_KEY = "14dd4770"
omdb.set_default('apikey', API_KEY)

OUTPUT_FILE = "movies.csv"
IMAGE_FOLDER = "posters"
MOVIE_TITLES = ['Logan', 'The Adventures of Tintin', 'Hercules', 'The Hunchback of Notre Dame', 'Coraline', 'The Divergent Series: Insurgent', 
 'Watchmen', 'The Iron Giant', '12 Years a Slave', 'Annabelle: Creation', 'The Godfather Part II', 'Puss in Boots', 'Mulan', 'Signs', 
 'Pacific Rim', 'Mean Girls', 'Hereditary', 'The Matrix Revolutions', 'Twelve Years a Slave', 'Rio', 'Cruella', '10 Things I Hate About You', 
 'Ant-Man', 'The Shawshank Redemption', 'Fantastic Four: Rise of the Silver Surfer', 'The Blair Witch Project', 'Ratatouille', 'New Moon', 'Doctor Strange', 
 'The Princess and the Frog', 'Avengers: Age of Ultron', 'The Last Jedi', 'Spider-Man 3', 'The Big Lebowski', 'Fantastic Beasts and Where to Find Them', 
 'Lady and the Tramp II', 'Whiplash', 'Rango', 'Madagascar: Escape 2 Africa', 'The Social Network', 'Snow White and the Seven Dwarfs', 'A Quiet Place Part II',
 'A Beautiful Mind', 'Epic', 'The Dark Knight Rises', 'Re-Animator', 'The Evil Dead', 'The Conjuring 2', 'The Texas Chainsaw Massacre', 'Wonder Woman',
 'The Terminator', "The World's End", 'Shawshank Redemption', 'Bambi', 'The Strangers', 'The Aristocats', 'The Prince of Egypt', 'Blade II', 'The Amazing Spider-Man 2',
 "The King's Speech", 'The Village', 'Legally Blonde', 'The Secret Life of Pets 2', 'The Hills Have Eyes', 'Ice Age: Continental Drift', 'Toy Story 3',
 'How to Train Your Dragon: The Hidden World', 'Get Out', 'The Revenant', 'Heat', 'Kung Fu Panda 2', 'Breaking Dawn - Part 2', 'Donnie Darko', 'Moonlight', 'Prisoners',
 'Misery', 'Evil Dead', 'Sinister', 'The Wedding Planner', 'Despicable Me', 'A Goofy Movie', 'Zombieland', 'It: Chapter Two', 'The Invisible Man', 'The Pursuit of Happyness',
 'The Artist', 'Despicable Me 2', 'La La Land', 'The Lorax', 'Bird Box', 'The Lion Guard', 'Over the Hedge', 'Erin Brockovich', 'The Exorcist', 'Dirty Dancing',
 'Blade', 'Pirates of the Caribbean: On Stranger Tides', 'Robin Hood', 'A Nightmare on Elm Street', 'The Incredibles', 'It Follows', 'Frozen II', 'Thor: Ragnarok',
 'Terminator 2: Judgment Day', 'National Treasure', 'A Clockwork Orange', 'The Grudge', 'Breaking Dawn - Part 1', 'Alice in Wonderland', 'The Truman Show',
 'The SpongeBob SquarePants Movie', 'The Great Gatsby', 'An Extremely Goofy Movie', 'Pocahontas', 'Amadeus', 'Captain America: Civil War', '28 Weeks Later',
 'Jumanji: Welcome to the Jungle', 'Baby Driver', 'Tarzan', 'Pinocchio', 'Madagascar', 'Zootopia', 'Notting Hill', 'Finding Dory', 'Scream',
 'Ice Age: Collision Course', "Schindler's List", 'Midsommar', '12 Angry Men', 'X-Men: Days of Future Past', 'National Treasure: Book of Secrets',
 'The Fifth Element', 'The Breakfast Club', 'The Aviator', 'Mulan II', 'Hidden Figures', 'The Shining', 'Hotel Transylvania', 'The Hunger Games',
 'Fantastic Four (2015)', 'Us', 'The Great Mouse Detective', 'Christine', 'X-Men', 'Nightmare on Elm Street', 'Hush', 'Ice Age: The Meltdown', 'X-Men: Apocalypse', 
 'The Wolverine', 'Titanic', 'Antz', 'Dallas Buyers Club', 'The Town', 'The Holiday', 'The Silence of the Lambs', 'Peter Rabbit', 'Les Misérables', 'The Bee Movie', 
 'Knock Knock', 'Stand by Me', 'Allegiant', 'The Sandlot', 'The Invitation', 'Jurassic World', 'Fight Club', 'The Hunger Games: Mockingjay - Part 1', 'The Happening',
 'The Fox and the Hound', 'Luca', 'The Road to El Dorado', 'Julie and Julia', 'Treasure Planet', 'Shrek 2', 'Pocahontas II', '28 Days Later', 'The Fox and the Hound 2',
 'Grease', 'Goodfellas', 'The Devil Wears Prada', 'Coco', 'The Incredibles 2', 'Pirates of the Caribbean: The Curse of the Black Pearl', 'Inglourious Basterds', 'Ice Age',
 'The Cabin in the Woods', 'Megamind', 'Cars 2', 'The Intern', 'Cloudy with a Chance of Meatballs', 'The Lego Movie 2', 'Scarface', 'Deadpool', 'Kill Bill', 'Flashdance',
 'Aquaman','The Big Short', 'Back to the Future', 'Blade: Trinity', "A Bug's Life", 'Evil Dead II', 'The Book of Life', 'American History X', 'The Irishman',
 'The Greatest Showman', 'Guardians of the Galaxy', 'Captain America: The Winter Soldier', 'Captain America: The First Avenger', 'Twilight', 'Spider-Man: No Way Home',
 'The Killing', 'A Shaun the Sheep Movie', 'Wonder Woman 1984', 'Finding Nemo', 'The Proposal', 'Star Wars: The Force Awakens', 'The Prestige', 'Wreck-It Ralph',
 'The Dark Knight', 'Avengers: Infinity War', 'The Purge', 'Carrie', "Pirates of the Caribbean: At World's End", 'Chicken Little', 'Sleeping Beauty',
 'The Little Prince', 'Ring 2', 'The Polar Express', 'Guardians of the Galaxy Vol. 2', 'Back to the Future Part II', 'The Emoji Movie', 'ParaNorman', 
 'The Descent', 'How to Train Your Dragon', 'Avengers: Endgame', 'The Godfather Part III', 'Godzilla', 'The Wolf of Wall Street', 'Pulp Fiction',
 'The Godfather', 'The Nun', 'Thor', 'Peter Pan II', 'The BFG', 'The Dark Knight Returns', 'Superbad', 'Moana', 'The Croods', 'The Twilight Saga: Eclipse', 
 'The Karate Kid', 'Tangled', 'V for Vendetta', 'Captain Marvel', 'Lilo & Stitch', 'The Matrix Reloaded', 'My Big Fat Greek Wedding', 'Sing', 
 'Inside Out', 'The Outsiders', 'Cinderella', 'Catch Me If You Can', 'SpongeBob SquarePants: Sponge Out of Water', 'Spider-Man: Homecoming', 
 'The Hateful Eight', 'Up', 'The Sword in the Stone', 'Cinderella II', 'The Borrowers', 'Her', 'Madagascar 3', 'Sing 2', 'Divergent', 'Annabelle', 
 'Elektra', 'Insidious: The Last Key', 'Memento', 'Crazy, Stupid, Love', "You've Got Mail", 'The Secret Life of Walter Mitty', 
 'The Hunger Games: Mockingjay - Part 2', 'Sixteen Candles', 'Army of Darkness', 'The Orphanage', 'Wreck-It Ralph 2', 'X-Men: First Class', 
 'The Lion King', 'The Goonies', 'Mystic River', 'The Machinist', 'King Kong', 'Beauty and the Beast', 'Terminator Salvation', 'Insidious: Chapter 2',
 'The Count of Monte Cristo', "Ferris Bueller's Day Off", 'The Rise of Skywalker', 'The Usual Suspects', 'The Thing', 'The Lion King II',
 'Pirates of the Caribbean: Dead Men Tell No Tales', 'E.T. the Extra-Terrestrial', 'The Conjuring: The Devil Made Me Do It', 'Home on the Range', 
 'Star Wars: The Empire Strikes Back', 'The Departed', 'The Maze Runner', 'Jurassic World: Fallen Kingdom', 'The Conjuring', 'Drive',
 'Maze Runner: The Scorch Trials', 'Love Actually', 'Black Swan', 'Inception', 'The Mist', 'Shrek the Third', 'Shrek', 'American Sniper',
 'The Shape of Water', 'Shazam!', 'Reservoir Dogs', 'The Amazing Spider-Man', 'Moneyball', 'The Lego Batman Movie', 'Joseph: King of Dreams',
 'The Sixth Sense', 'Silver Linings Playbook', 'Justice League', 'Shrek Forever After', 'The Lord of the Rings: The Return of the King', 
 'Jurassic Park', 'Aardvark', 'The Walking Dead', 'It Comes at Night', 'Shutter Island', 'Toy Story 2', 'Sin City', 'Tucker & Dale vs. Evil', 
 'The Theory of Everything', 'Star Wars: The Rise of Skywalker', 'Elf', 'The Avengers', 
 'Iron Man 3', 'The Green Mile', 'Spider-Man 2', 'Dumbo', 'Paranormal Activity', 'Iron Man', 'The Grand Budapest Hotel', 'X-Men: The Last Stand',
 'Wallace & Gromit: The Curse of the Were-Rabbit', 'The Babadook', 'Hot Fuzz', 'Hellraiser', 'Cars 3', 'The Hunger Games: Catching Fire', 'The Others',
 'Sleepless in Seattle', "Rosemary's Baby", 'Aladdin', 'Forrest Gump','Interstellar', 'Lady and the Tramp', 'The Matrix', 'The Brave Little Toaster',
 'The Black Stallion', 'Insurgent', 'Pretty Woman', 'The Simpsons Movie', 'World War Z', "Bridget Jones's Diary", 'Pet Sematary', 'Mad Max: Fury Road', 
 'The Terminal', 'Mamma Mia!', 'The Return of Jafar', 'Donnie Brasco', 'Spider-Man: Into the Spider-Verse', 'The Pianist', 'The Jungle Book II', 'Trolls', 
 'House of 1000 Corpses', 'Jumanji', 'The Evil Dead (2013)', 'Django Unchained', 'I Am Legend', 'The Black Cauldron', 'Monsters, Inc.', 'Back to the Future Part III',
 'The Angry Birds Movie', "Pirates of the Caribbean: Dead Man's Chest", 'The Lego Ninjago Movie', 'Shark Tale', 'Suicide Squad', 'Sinister 2', 'Madagascar 2',
 'Halloween', 'Birdman', 'Star Wars: A New Hope', 'Wall-E', 'Se7en', 'Cloudy with a Chance of Meatballs 2', 'The Fighter', 'Toy Story 4', 'Tiana', 'Kung Fu Panda', 
 'Robin Hood II', 'Home Alone', 'The Hangover', 'Bohemian Rhapsody', 'Black Panther', 'The Texas Chain Saw Massacre', 'Peter Pan', 'Aladdin II', 'Fantastic Four',
 'Monsters vs. Aliens', 'Rocketman', 'Trolls World Tour', 'Brave', 'Hotel Transylvania 2', 'A Quiet Place', 'The Blind Side', "Gerald's Game", 'The Wrestler', 
 "The Devil's Rejects", 'Ant-Man and The Wasp', 'Friday the 13th', 'Minions', 'Kung Fu Panda 3', 'Terminator Genisys', 'The Suicide Squad', 'The Boondock Saints',
 'Unbreakable', 'Avatar', "You're Next", 'Monsters University', 'The Little Mermaid', 'Deadpool 2', 'The Little Mermaid II', "The Emperor's New Groove",
 'The Ring', 'The 40-Year-Old Virgin', 'The Lion King 2', 'Space Jam', 'Spider-Man', 'Winnie the Pooh', 'The Jungle Book', 'The Shallows', 'Frozen',
 'A Star Is Born', 'Toy Story', 'The Princess Bride', "Don't Breathe", 'The Witch', 'Atlantis: The Lost Empire', 'Shaun of the Dead', 
 'Ice Age: Dawn of the Dinosaurs', 'The Help', 'Maze Runner: The Death Cure', 'Insidious: Chapter 3', 'Julie & Julia', 'Black Widow', 'Gone Baby Gone', 
 'Captain Underpants: The First Epic Movie', 'WALL-E', 'The Lego Movie', 'Insidious', 'The Autopsy of Jane Doe', 'It', 'The Secret Life of Pets', 'The Rescuers', 
 'Frankenweenie', 'Annabelle Comes Home', 'Footloose', 'Soul', 'The Good Dinosaur', 'Cars', 'The Peanuts Movie', 'Gladiator', 'Casino', 'Maleficent', 
 'Fantastic Mr. Fox', 'Dawn of the Dead', 'Big Hero 6', 'Trainspotting', 'The Fly', 'The Divergent Series: Allegiant', 'When Harry Met Sally', 'Bolt', 
 'King Kong vs. Godzilla', 'Oliver & Company', 'Joker', "Charlotte's Web", 'Star Wars: The Last Jedi', 'Gangs of New York', 'Stuart Little', 
 'Once Upon a Time in Hollywood', 'Terminator 3: Rise of the Machines', 'American Psycho', 'Bee Movie', 'The Imitation Game', 'Clueless', 'Zombieland: Double Tap',
 'X2: X-Men United', 'The Incredible Hulk', 'Spider-Man: Far From Home', 'Jumanji: The Next Level', 'Cujo', 'Requiem for a Dream', 'Daredevil', 'Eclipse',
 ]
# Создание папки для обложек
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def download_image(url, filename):
    """Скачивает изображение и сохраняет его в папке IMAGE_FOLDER"""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            image_path = os.path.join(IMAGE_FOLDER, filename)
            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Saved poster: {filename}")
        else:
            print(f"Failed to download image: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def fetch_movies():
    movies = []
    
    for title in MOVIE_TITLES:
        print(f"Fetching details for: {title}")
        details = omdb.get(title=title)

        if details and details.get("response") == "True":
            poster_url = details.get("poster", "N/A")
            filename = f"{title.replace(' ', '_')}.jpg"

            if poster_url and poster_url != "N/A":
                download_image(poster_url, filename)

            movies.append({
                "title": details.get("title", "N/A"),
                "year": details.get("year", "N/A"),
                "user_tags": details.get("genre", "N/A"),
                "reviews": details.get("ratings", []),
                "author": details.get('director', 'N/A'),
                "plot": details.get('plot', 'N/A'),
                "poster": filename if poster_url != "N/A" else "N/A"
            })
        else:
            print(f"Failed to fetch: {title}")
        
        time.sleep(0.5)  # Чтобы не упереться в лимиты API
    
    return movies

def save_to_csv(movies):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "year", "user_tags", "reviews", "author", "plot", "poster"])
        writer.writeheader()
        for movie in movies:
            writer.writerow(movie)

def main():
    movies = fetch_movies()
    save_to_csv(movies)
    print(f"Saved {len(movies)} movies and posters to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()


 

