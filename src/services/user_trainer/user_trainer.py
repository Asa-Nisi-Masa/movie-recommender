import torch
from tqdm import tqdm

from src.model import Model


class UserTrainer:

    def __init__(self, model: Model):
        self.__model = model

    def get_predicted_ratings(self, ids: torch.Tensor, ratings: torch.Tensor) -> torch.Tensor:
        self.__model.setup_user_trainer()
        self.__train(ids, ratings)

        return self.__model.get_ratings_matrix()

    def __train(self, ids: torch.Tensor, ratings: torch.Tensor) -> None:
        criterion = torch.nn.MSELoss()
        optimizer = torch.optim.SparseAdam(list(self.__model.parameters()), lr=5e-2)

        user = torch.tensor(0).to(self.__model.device)
        ids = ids.to(self.__model.device)
        ratings = ratings.to(self.__model.device)

        for _ in tqdm(range(500)):
            predicted_ratings = self.__model.forward(user, ids)

            loss = criterion(predicted_ratings, ratings)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
