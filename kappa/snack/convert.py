import json
import click
import os
from pprint import pprint


@click.command()
@click.argument("json_file", type=click.Path(exists=True), required=True)
def snack(json_file: str) -> None:

    # TODO: check if the tool hsddl exists

    # generate a filename `log-timestamp`

    # get the json file and the data
    click.echo(f"Loading... {json_file}")

    with open(json_file, "r") as f:
        data = json.load(f)

    downloaded_videos: list[str] = list()
    
    for obj in data:
        pprint(obj)

        # generate the filename
        # download the hdsl using hsddl and adding .ts
        # log the download
        # store the video file name in `downloaded_videos`

    # for every video in downloaded file
        # start the converting using `ts_to_mp4` or copy the command and run it using
        # ts_to_mp4 = "the command"
        # output = subprocess.run(['ls', '-l'], capture_output=True, text=True)
        # click.echo(output.stdout)
        # log the conversion
    
    # Print the result
    return

