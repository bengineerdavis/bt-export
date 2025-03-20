"""
Command-line interface for the Braintrust Downloader.
This module serves as the entry point for the bt_import package.
"""

import logging
import sys

import click

from bt_import.downloader import ProjectDownloader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Download Braintrust experiments and datasets as CSVs."""
    pass


@cli.command()
@click.option(
    "--output",
    "-o",
    default=None,
    help="Output directory for downloaded files",
)
@click.argument("project-id", required=True)
def download(output, project_id):
    """Download experiments and datasets from Braintrust.

    'bt-export download PROJECT-ID --output <OUTPUT-DIR>'

    A project ID is required to download data. Use the list-projects command to
    see available projects.
    """
    try:
        downloader = ProjectDownloader(id=project_id, output_dir=output)

        logger.info(f"Downloading data for project {downloader.name}")
        downloader.download()

    except Exception as e:
        logger.error(f"Error during download process: {e}")
        sys.exit(1)

    logger.info("Download process completed")


@cli.command()
def list_projects():
    """List all available Braintrust projects."""
    try:
        total_projects = [proj for proj in ProjectDownloader.projects.list()]

        if len(total_projects) == 0:
            click.echo("No projects found.")
            return

        click.echo(f"Found {len(total_projects)} projects:")
        for idx, project in enumerate(total_projects, 1):
            click.echo(f"{idx}. {project.name} " f"(ID: {project.id})")

    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
