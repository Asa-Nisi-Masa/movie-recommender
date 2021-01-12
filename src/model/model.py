import torch
from src.movie_model import MovieModel


class Model(torch.nn.Module):

    def __init__(self, movie_model: MovieModel):
        super(Model, self).__init__()

        embedding_dim = 32
        num_movies = movie_model.get_number_of_movies()

        self.device = torch.device("cpu")
        self.__movie_encodings_pretrained = movie_model.get_movie_encodings().to(self.device)

        self.movie_embeddings = torch.nn.Embedding(num_movies, embedding_dim, sparse=True)
        self.one_user_embedding = torch.nn.Embedding(1, embedding_dim, sparse=True)

    def setup_user_trainer(self) -> None:
        with torch.no_grad():
            self.movie_embeddings.weight.copy_(self.__movie_encodings_pretrained)

        self.movie_embeddings.weight.requires_grad = False
        self = self.to(self.device)
        self.eval()

    def forward(self, users: torch.Tensor, movies: torch.Tensor) -> torch.Tensor:
        w = self.one_user_embedding(users).unsqueeze(0)
        v = self.movie_embeddings(movies)

        return torch.sum(w * v, dim=1)

    def get_ratings_matrix(self) -> torch.Tensor:
        return torch.mm(self.one_user_embedding.weight, self.movie_embeddings.weight.T)
