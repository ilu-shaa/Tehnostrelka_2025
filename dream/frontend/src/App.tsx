import React, { useState } from 'react';
import axios from 'axios';
import { Container, TextField, Button, Typography, Card, CardMedia, CardContent } from '@mui/material';

function App() {
  const [query, setQuery] = useState("");
  const [movies, setMovies] = useState<any[]>([]);
  const [k, setK] = useState(5);

  const handleSearch = async () => {
    try {
      // Django-бэкенд по умолчанию на 8000 порту
      const url = "http://localhost:8000/api/search/";
      const body = { query, k };
      const response = await axios.post(url, body);
      setMovies(response.data);
    } catch (error) {
      console.error("Search error:", error);
    }
  };

  return (
    <Container maxWidth="md" style={{ marginTop: '40px' }}>
      <Typography variant="h4">Movie Recommender (Django)</Typography>
      <TextField
        label="Поиск по описанию/тегам"
        variant="outlined"
        fullWidth
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ margin: '20px 0' }}
      />
      <TextField
        label="Количество результатов (k)"
        variant="outlined"
        type="number"
        value={k}
        onChange={(e) => setK(parseInt(e.target.value))}
        style={{ marginBottom: '20px' }}
      />
      <Button variant="contained" color="primary" onClick={handleSearch}>
        Найти
      </Button>

      <div style={{ marginTop: '40px' }}>
        {movies.map((movie, index) => (
          <Card key={index} style={{ marginBottom: '20px' }}>
            {/* Предполагается, что папка posters доступна или через public/posters,
                или через http://localhost:8000/posters/<filename> */}
            <CardMedia
              component="img"
              image={`/posters/${movie.poster}`}
              alt={movie.title}
              height="300"
            />
            <CardContent>
              <Typography variant="h6">{movie.title} ({movie.year})</Typography>
              <Typography variant="body2" color="text.secondary">
                {movie.plot}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Автор: {movie.author}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Рейтинг поиска: {movie.score?.toFixed(2)}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </div>
    </Container>
  );
}

export default App;