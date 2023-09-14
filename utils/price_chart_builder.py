import os.path

import matplotlib.pyplot as plt


class GraphBuilder:
    def __init__(self, title, exchange_rates: dict):
        self.title = title
        self.time_label = "Time"
        self.price_label = "Price"
        self.exchange_rates = exchange_rates

    def _plot_graph(self) -> None:
        times = list(self.exchange_rates.keys())
        prices = list(self.exchange_rates.values())

        plt.figure(figsize=(12, 6))
        plt.plot(times, prices, linestyle='-', color='#E27D60', label=self.title)
        plt.title(self.title)
        plt.xlabel(self.time_label)
        plt.ylabel(self.price_label)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.6)
        plt.legend()
        plt.tight_layout()

    def show_graph(self) -> None:
        self._plot_graph()
        plt.show()

    def save_graph(self, file_name: str) -> None:
        self._plot_graph()
        directory = 'currency_graphs/'
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file_name)
        plt.savefig(file_path)
        plt.close()
