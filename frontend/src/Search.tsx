import React, { useState } from 'react';
import axios from 'axios';

const Search = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<any[]>([]);
    const [selectedMovie, setSelectedMovie] = useState<any>(null);

    const handleSearch = async () => {
        try {
            const response = await axios.post('http://localhost:8000/search', { query });
            setResults(response.data);
        } catch (error) {
            console.error('Search error:', error);
        }
    };

    const fetchMovieDetails = async (title: string) => {
        try {
            const response = await axios.get(`http://localhost:8000/movie/${title}`);
            setSelectedMovie(response.data);
        } catch (error) {
            console.error('Fetch error:', error);
        }
    };

    return (
        <div className="container">
            <div className="search-box">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search movies..."
                />
                <button onClick={handleSearch}>Search</button>
            </div>

            <div className="results">
                {results.map((movie) => (
                    <div 
                        key={movie.title} 
                        className="movie-card"
                        onClick={() => fetchMovieDetails(movie.title)}
                    >
                        <img 
                            src={`/posters/${movie.poster}`} 
                            alt={movie.title}
                            onError={(e) => {
                                (e.target as HTMLImageElement).src = '/posters/placeholder.jpg';
                            }}
                        />
                        <h3>{movie.title} ({movie.year})</h3>
                    </div>
                ))}
            </div>

            {selectedMovie && (
                <div className="movie-details">
                    <h2>{selectedMovie.title}</h2>
                    <p>Director: {selectedMovie.author}</p>
                    <p>Plot: {selectedMovie.plot}</p>
                    <div className="reviews">
                        <h4>Ratings:</h4>
                        {selectedMovie.reviews.map((review: any, index: number) => (
                            <div key={index}>
                                <strong>{review.source}:</strong> {review.value}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Search;