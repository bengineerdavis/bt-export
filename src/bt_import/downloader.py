import logging
import os
from pathlib import Path

import pandas as pd
from braintrust_api import Braintrust

logger = logging.getLogger(__name__)


class Config:
    """Abstracts configuration management and passes environment variables
    to other objects, methods, and functions
    """

    def __init__(self, api_key=None, client=None):
        self.api_key = (
            os.environ.get("BRAINTRUST_API_KEY") if api_key is None else api_key
        )
        self.client = Braintrust(api_key=self.api_key) if client is None else client


class ProjectDownloader:
    """Object to abstract calls and cache data for one project on a user's
    Braintrust account via the Braintrust Python API SDK
    """

    config = Config()
    client = config.client
    projects = client.projects
    project_ids = {project.name: project.id for project in projects.list()}

    def __init__(self, id, output_dir=None):
        self.id = id
        self.name = ProjectDownloader.projects.retrieve(self.id).name
        self.output_dir = (
            Path(".").home()
            / Path("braintrust_downloads")
            / f"{'-'.join(self.name)}_project"
            if output_dir is None
            else output_dir
        )

        # internal instance variables
        self._project = ProjectDownloader.client.projects.retrieve(project_id=self.id)
        self._entries = {
            "experiments": ProjectDownloader.client.experiments,
            "datasets": ProjectDownloader.client.datasets,
        }

    def retrieve(self, category: str) -> pd.DataFrame:
        """Pull a categorical/columnal subset of the available project data"""
        # local variables
        try:
            entries = self._entries[category]

        except:  # noqa: E722
            _keys = [key for key in self._entries.keys()]
            msg = [
                f"The {category} key not be found in self._entries ... \n",
                f"Please select from one of the available categories: {', '.join(_keys)}",
            ]

            print(" ".join(msg))

        pulled = [e for e in entries.list() if self._project.id == self.id]
        df = pd.DataFrame()

        # write all experiments events for the given project into a dataframe
        print(f"Pulling all {category} data ... ")
        for item in pulled:
            fetched = entries.fetch(item.id)
            events = [event.to_dict() for event in fetched.events]
            df = pd.concat([df, pd.DataFrame.from_records(events)], ignore_index=True)

        print(f"Returning all found {category} data ... ")
        print(df)
        return df

    def retrieve_all(self) -> dict:
        """Pulls all experiment data for a given project id

        returns a dictionary of labeled dataframes with extracted data"""

        sub_entries_dict = {}

        names = [key for key in self._entries.keys()]
        print(
            f"Pulling all the stored {' & '.join(names)} entries from the {self.name} project ... "
        )
        for category in self._entries.keys():
            sub_entries_dict.update({category: self.retrieve(category=category)})

        print("All entries have been successfully returned!")

        return sub_entries_dict

    def download(self, output_dir=None):
        """Download and write all experiments and datasets to the local filesystem."""
        # self._output_dir = (
        #     Path(output_dir) if output_dir is not None else self._output_dir
        # )

        # Set the output directory
        if output_dir is not None:
            self.output_dir = Path(output_dir)

        # Make sure the directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        data_dict = self.retrieve_all()
        for category, data in data_dict.items():
            data.to_csv(self.output_dir / f"{category}.csv", index=False)
            print(
                f"{self.name}'s data for {category} has been written to {self.output_dir}"
            )


if __name__ == "__main__":
    # Test the ProjectImporter class
    project_importer = ProjectDownloader(id="f3c708a5-c794-4b3f-b67c-5426ca1c4386")
    data = project_importer.retrieve(category="experiments")
    print(f"Experiments Data: {data}")
    print(data)
    # project_importer.retrieve_all()
