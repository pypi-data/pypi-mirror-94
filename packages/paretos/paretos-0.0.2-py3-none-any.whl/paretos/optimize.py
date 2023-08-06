from typing import List

from .client import SocratesAPIClient
from .config import config
from .database.database_handler import DB
from .environments import Environment
from .objects.analyzed_results import AnalyzedEvaluations
from .objects.evaluation import Evaluation, Evaluations
from .objects.optimization_problem import OptimizationProblem
from .terminators import BaseTerminator


def socrates(
    name: str,
    problem: OptimizationProblem,
    environment: Environment,
    terminators: List[BaseTerminator],
    n_parallel: int = 1,
    max_number_of_runs: int = 10000,
) -> AnalyzedEvaluations:
    """
    Main function the user calls when optimizing with socrates
    :param name: project name which will be added to database then!
    :param problem: hyper space definition of the problem
    :param environment: simulation environment to use for the execution
    :param terminators: list of all terminator functions which can lead to stop
    :param n_parallel: Number of parallel simulations that can be run on customer side
    :param max_number_of_runs: Absolute maximum to have hard stopping criteria
    """
    path = config.get_db_path()
    data_handler = DB(path)
    api_client = SocratesAPIClient(
        config.get_api_url(), config.get_customer_token().token
    )

    project_id = data_handler.add_project(name)

    data_handler.add_project_meta(project_id, problem)

    evaluations = Evaluations()

    progress = api_client.track_progress(problem, evaluations)

    nr_of_runs = 0

    while (
        not any([terminator.should_terminate(progress) for terminator in terminators])
        and nr_of_runs < max_number_of_runs
    ):
        nr_of_runs += 1

        designs = api_client.predict_design(problem, evaluations, n_parallel)

        for design in designs:
            simulation_id = data_handler.add_simulation_design(project_id, design)

            kpis = environment.simulate(design)

            data_handler.add_simulation_kpis(simulation_id, kpis)

            evaluation = Evaluation(
                id=str(simulation_id),
                design=design,
                kpis=kpis,
            )

            evaluations.add_evaluation(evaluation)

        progress = api_client.track_progress(problem, evaluations)

    analyzed_result = api_client.analyze_result(problem, evaluations)

    data_handler.update_pareto_state(analyzed_result)

    return analyzed_result
