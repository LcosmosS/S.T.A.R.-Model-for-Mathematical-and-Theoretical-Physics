from src.physics.mcmc_joint_pipeline import JointMCMCPipeline
from src.pipeline.paper_figures_pipeline import PaperFiguresPipeline

def run_full_inference(config):
    # Build likelihood
    planck = eval(config["datasets"]["planck"])
    bao = eval(config["datasets"]["bao"])
    cc = eval(config["datasets"]["cc"])

    joint = build_joint_likelihood(planck)

    # Run MCMC
    mcmc = JointMCMCPipeline(
        config["model"]["H_expr"],
        config["model"]["param_names"],
        config["priors"],
        config["proposal_widths"],
        joint
    )

    chain = mcmc.run(
        theta0=config["mcmc"]["theta0"],
        nsteps=config["mcmc"]["nsteps"]
    )

    # Figures
    fig = PaperFiguresPipeline(
        chain,
        config["model"]["param_names"],
        config["model"]["H_expr"],
        data_paths={
            "planck": planck,
            "bao": bao,
            "cc": cc
        }
    )

    constraints = fig.run(config["output_dir"])
    return constraints
