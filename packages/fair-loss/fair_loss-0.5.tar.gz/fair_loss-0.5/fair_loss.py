# SPDX-License-Identifier: GPL-3.0-only
# SPDX-FileCopyrightText: 2020 Vincent Lequertier <vi.le@autistici.org>

import torch
from typing import Callable, Union


class FairLoss(torch.nn.Module):
    def __init__(
        self,
        loss_fun: torch.nn.Module,
        unique_attr: torch.Tensor,
        fairness_score: Union[
            str, Callable[[torch.Tensor, torch.Tensor], torch.Tensor]
        ],
    ) -> None:
        """
        Add a fairness measure to the regular loss

        fairness_score is applied to input and target for each value of
        unique_attr. Then the results are sumed up, divided by the minimum and
        added to the regular loss function.


        .. math::
           loss + \\lambda{{\\sum_{i=0}^{k} w_i f_i(input, target)} \\over \\min\\limits_{ \\forall i\\in [0,k[} f_i(input, target)}

        where:

        - :math:`k` is the number of values of ``protected_attr``
        - :math:`f` is the ``fairness_score`` function


        Args:
            loss_fun (torch.nn.Module): A loss function
            unique_attr (torch.Tensor): Possible values of a sensitive attribute
            fairness_score (Union[str, Callable[[torch.Tensor, torch.Tensor], torch.Tensor]]): A function that takes input and target as arguments and return a score. Or one of 'accuracy', 'fpr', 'tpr', 'tnr', 'fnr', 'ppv', 'npv', 'accuracy'

        Examples:
            >>> model = Model()
            >>> data = torch.randint(0, 5, (100, 5), dtype=torch.float, requires_grad=True)
            >>> target = torch.randint(0, 5, (100, 1), dtype=torch.float)
            >>> input = model(data)
            >>> # The sensitive attribute is the second column
            >>> dim = 1
            >>> criterion = FairLoss(torch.nn.MSELoss(), data[:, dim].detach().unique(), 'accuracy')
            >>> loss = criterion(data[:, dim], y_pred, y_true)
        """

        super().__init__()
        self.loss = loss_fun
        self.unique_attr = unique_attr
        self.fairness_score = (
            self.get_fairness_score(fairness_score)
            if isinstance(fairness_score, str)
            else fairness_score
        )

    def forward(
        self, protected_attr: torch.Tensor, input: torch.Tensor, target: torch.Tensor
    ):
        """
        Compute the fair loss

        Shape:
            - protected_attr: :math:`(N,)`
            - input: :math:`(N, 1)`
            - target: :math:`(N, 1)`

        Returns:
            torch.Tensor: The fair loss value
        """
        scores = torch.FloatTensor(
            [
                # Apply the fairness score for each possible value
                self.fairness_score(
                    input[torch.where(protected_attr == val)],
                    target[torch.where(protected_attr == val)],
                )
                for val in self.unique_attr
            ]
        )

        # Sum up and divide by the minimum. Then add to the regular loss
        return torch.add(self.loss(input, target), scores.sum() / (scores.min() + 1e-7))

    def get_fairness_score(
        self,
        fairness_score: str,
    ) -> Callable[[torch.Tensor, torch.Tensor], torch.Tensor]:
        """
        Return one of the fairness scores that are built-in

        Args:
            fairness_score (str): The fairness score

        Returns:
            Callable[[torch.Tensor, torch.Tensor], torch.Tensor]: The fairness score function
        """
        if hasattr(self, fairness_score):
            return getattr(self, fairness_score)
        else:
            raise ValueError(
                'The fairness score "{}" is unavailable'.format(fairness_score)
            )

    @staticmethod
    def fpr(input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        False Positive Rate

        .. math::
           {FPR} = {FP \\over FP + TN}

        where:

        - :math:`FP` is the number of False Positive
        - :math:`TN` is the number of True Negative

        Args:
            input (torch.Tensor): Predicted values
            target (torch.Tensor): Ground truth

        Shape:
            - input: :math:`(N, 1)`
            - target: :math:`(N, 1)`

        Returns:
            torch.Tensor: False Positive Rate

        Examples:
            >>> input = np.random.randint(2, size=(10, 1)).astype("float")
            >>> input = torch.tensor(input)
            >>> target = np.random.randint(2, size=(10, 1)).astype("float")
            >>> target = torch.tensor(target)
            >>> fpr(input, target)
        """
        fp = sum((input == True) & (target == False))
        tn = sum((input == False) & (target == False))
        return torch.true_divide(fp, fp + tn)

    @staticmethod
    def tpr(input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        True Positive Rate

        .. math::
           {TPR} = {TP \\over TP + FN}

        where:

        - :math:`TP` is the number of True Positive
        - :math:`FN` is the number of False Negative

        Args:
            input (torch.Tensor): Predicted values
            target (torch.Tensor): Ground truth

        Shape:
            - input: :math:`(N, 1)`
            - target: :math:`(N, 1)`

        Returns:
            torch.Tensor: True Positive Rate

        Examples:
            >>> input = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> target = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> tpr(input, target)
        """
        fn = sum((input == False) & (target == True))
        tp = sum((input == True) & (target == True))
        return torch.true_divide(tp, tp + fn)

    @staticmethod
    def tnr(input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        True Negative Rate

        .. math::
           {TNR} = {TN \\over TN + FP}

        where:

        - :math:`TN` is the number of True Negative
        - :math:`FP` is the number of False Positive

        Args:
            input (torch.Tensor): Predicted values
            target (torch.Tensor): Ground truth

        Shape:
            - input: :math:`(N, 1)`
            - target: :math:`(N, 1)`

        Returns:
            torch.Tensor: True Negative Rate

        Examples:
            >>> input = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> target = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> tnr(input, target)
        """
        fp = sum((input == True) & (target == False))
        tn = sum((input == False) & (target == False))
        return torch.true_divide(tn, tn + fp)

    @staticmethod
    def fnr(input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        False Negative Rate

        .. math::
           {FNR} = {FN \\over FN + TP}

        where:

        - :math:`FN` is the number of False Negative
        - :math:`TP` is the number of True Positive

        Args:
            input (torch.Tensor): Predicted values
            target (torch.Tensor): Ground truth

        Shape:
            - input: :math:`(N, 1)`
            - target: :math:`(N, 1)`

        Returns:
            torch.Tensor: False Negative Rate

        Examples:
            >>> input = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> target = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> fnr(input, target)
        """
        fn = sum((input == False) & (target == True))
        tp = sum((input == True) & (target == True))
        return torch.true_divide(fn, fn + tp)

    @staticmethod
    def ppv(input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        Positive Predicted Value

        .. math::
           {PPV} = {TP \\over TP + FP}

        where:

        - :math:`TP` is the number of True Positive
        - :math:`FP` is the number of False Positive

        Args:
            input (torch.Tensor): Predicted values
            target (torch.Tensor): Ground truth

        Shape:
            - input: :math:`(N, 1)`
            - target: :math:`(N, 1)`

        Returns:
            torch.Tensor: Positive Predicted Value

        Examples:
            >>> input = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> target = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> ppv(input, target)
        """
        tp = sum((input == True) & (target == True))
        fp = sum((input == True) & (target == False))
        return torch.true_divide(tp, tp + fp)

    @staticmethod
    def npv(input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        Negative Predicted Value

        .. math::
           {NPV} = {TN \\over TN + FN}

        where:

        - :math:`TN` is the number of True Negative
        - :math:`FN` is the number of False Negative

        Args:
            input (torch.Tensor): Predicted values
            target (torch.Tensor): Ground truth

        Shape:
            - input: :math:`(N, 1)`
            - target: :math:`(N, 1)`

        Returns:
            torch.Tensor: Negative Predicted Value

        Examples:
            >>> input = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> target = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> npv(input, target)
        """
        tn = sum((input == False) & (target == False))
        fn = sum((input == False) & (target == True))
        return torch.true_divide(tn, tn + fn)

    @staticmethod
    def accuracy(input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        Accuracy

        Args:
            input (torch.Tensor): Predicted values
            target (torch.Tensor): Ground truth

        Shape:
            - input: :math:`(N, 1)`
            - target: :math:`(N, 1)`

        Returns:
            torch.Tensor: Accuracy

        Examples:
            >>> input = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> target = torch.randint(0, 2, (10, 1), dtype=torch.float)
            >>> accuracy(input, target)
        """
        return torch.true_divide((input == target).sum(), input.shape[0])
