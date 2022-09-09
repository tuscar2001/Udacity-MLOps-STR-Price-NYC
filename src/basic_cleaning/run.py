#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info("Downloading and reading the artifact")
    data_path = run.use_artifact(args.input_artifact)
    local_path = artifact.file()

    logger.info("Dropping the outliers")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    
    logger.info("Convert last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])


    logger.info("Saving the results")
    outfile = args.output_artifact
    df.to_csv(outfile, index=False)

    artifact = wandb.Artifact(
        name = args.output_artifact,
        type = args.output_type,
        description = args.output_description
    )

    artifact.add_file(outfile)
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic cleaning")


    parser.add_argument(
        "--input_artifact", 
        type = str,
        help = "Name of the input artifact"
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type = str
        help= "Name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type = str
        help = "Type of the artifact"
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type = str 
        help= "Description of the output"
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type = float
        help = "Minimum Price" 
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type = float
        help = "Maximum Price"
        required=True
    )


    args = parser.parse_args()

    go(args)
