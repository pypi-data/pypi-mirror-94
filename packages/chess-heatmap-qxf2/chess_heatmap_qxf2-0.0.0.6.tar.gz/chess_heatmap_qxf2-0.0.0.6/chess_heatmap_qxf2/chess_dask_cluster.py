"""
This module is for parallelizing the calculation of power of each square (in a ply)
using dask tasks and parallelizing multiple games in PGNs
"""
import os
import errno
import yaml
from dask.distributed import LocalCluster
from dask.distributed import Client
from dask.distributed import worker_client
from distributed import wait
import coiled
from .chess_util import ChessUtil

class ChessDaskCluster:
    "Class for using dask tasks to parallelize calculation of power of each square"
    client: Client

    @staticmethod
    def get_game_data(result_list):
        "Preparing the data for all plies in all the games"

        gamedata_mapwhite = []
        gamedata_mapblack = []
        gamemax_controlwhite = 0
        gamemax_controlblack = 0
        ply_mapwhite = [[0 for x in range(8)] for y in range(8)]
        ply_mapblack = [[0 for x in range(8)] for y in range(8)]
        column_index = 0
        row = []
        row_index = 0
        ply_no = 0
        for result in result_list:
            square_index = result["square"]
            row = square_index//8
            column = square_index%8
            if result["white"] > gamemax_controlwhite:
                gamemax_controlwhite = result["white"]
            if result["black"] > gamemax_controlblack:
                gamemax_controlblack = result["black"]
            ply_mapwhite[7-row][column] = result["white"]
            ply_mapblack[7-row][column] = result["black"]
            row_index = row_index + 1
            if row_index == 8:
                row_index = 0
                column_index = column_index + 1
                if column_index == 8:
                    column_index = 0
                    gamedata_mapwhite.append(ply_mapwhite)
                    gamedata_mapblack.append(ply_mapblack)
                    ply_no = ply_no + 1
                    ply_mapwhite = [[0 for x in range(8)] for y in range(8)]
                    ply_mapblack = [[0 for x in range(8)] for y in range(8)]
        return {"white": gamedata_mapwhite, "black": gamedata_mapblack,
                "max_white_value": gamemax_controlwhite, "max_black_value": gamemax_controlblack}

    @staticmethod
    def run_in_parallel(game, game_no):
        """
        For the given game, for every ply, generate tasks to be run in parallel in a dask cluster.
        One task is created per square to find the control of both the sides. A worker client is
        used here because this method itself is run inside a worker
        """
        task_futures = []
        tasks_for_game = ChessUtil.generate_ply_info_list_for_game(game)
        with worker_client() as client:
            for game_task in tasks_for_game["ply_info_list"]:
                task_futures.append(
                    client.submit(ChessUtil.find_control_for_square, game_task))

        wait(task_futures)
        control_list_for_game = []
        for task_future in task_futures:
            control_list_for_game.append(task_future.result())
        game_data = ChessDaskCluster.get_game_data(control_list_for_game)
        game_data["filename"] = str(game_no) + " " + game.headers["Event"]
        return game_data

    def __init__(self):
        config_file = os.path.join(os.getcwd(), "config", "config.yaml")
        if not os.path.isfile(config_file):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), config_file)
        with open(config_file) as file:
            config_values = yaml.full_load(file)
        if config_values["cluster_name"] is None:
            config_values["cluster_name"] = "chess-cluster"
        if config_values["software_environment_name"] is None:
            config_values["software_environment_name"] = "chess-env"
        if config_values["n_workers"] is None:
            config_values["n_workers"] = 8
        if config_values["worker_cpu"] is None:
            config_values["worker_cpu"] = 4
        if config_values["worker_memory"] is None:
            config_values["worker_memory"] = 16
        if config_values["scheduler_memory"] is None:
            config_values["scheduler_memory"] = 16

        if config_values["use_local_cluster"]:
            cluster = LocalCluster(n_workers=config_values["n_workers"],
                                    threads_per_worker=1)
        else:
            coiled.create_software_environment(name=config_values["software_environment_name"],
                                                pip="requirements.txt")
            cluster = coiled.Cluster(name=config_values["cluster_name"],
                                    n_workers=config_values["n_workers"],
                                    worker_cpu=config_values["worker_cpu"],
                                    worker_memory=str(config_values["worker_memory"]) +"GiB",
                                    scheduler_memory=str(config_values["scheduler_memory"]) +"GiB",
                                    software=config_values["software_environment_name"])

        self.client = Client(cluster)

    def analyse_games_in_cluster(self, game_list):
        "Find control heatmap for all the games passed in parallel in a dask cluster"
        game_no = 0
        game_futures = []
        for game in game_list:
            game_futures.append(self.client.submit(ChessDaskCluster.run_in_parallel,
                                 *(game, game_no)))
            game_no = game_no + 1
        wait(game_futures)
        results = []
        for future in game_futures:
            results.append(future.result())
        return results
