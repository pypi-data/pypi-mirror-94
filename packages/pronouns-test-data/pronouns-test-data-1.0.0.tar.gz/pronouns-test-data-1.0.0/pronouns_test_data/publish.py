from enum import Enum
from typing import NoReturn, cast

import requests
import json
import sys
import os

import typer

from pronouns_test_data.models import GeneratedTestData, PronounTestCase

CERT_FILE = "/usr/local/lib/subman/certs/wmango.cert"
KEY_FILE = "/usr/local/lib/subman/certs/wmango.key"


class IRWSEndpoint(Enum):
    eval = "eval"
    prod = "prod"

    def get_url_for_netid(self, netid: str) -> str:
        return f"{self.url}/v3/entity.profile/uwnetid={netid}?-reflect"

    @property
    def url(self):
        return _ENDPOINTS[self]


_ENDPOINTS = {
    IRWSEndpoint.eval: "https://mango-eval.u.washington.edu:646/registry-eval",
    IRWSEndpoint.prod: "https://mango.u.washington.edu:646/registry",
}


class PronounsClient:
    def __init__(
        self,
        endpoint: IRWSEndpoint,
        cert_path: str,
        key_path: str,
        dry_run: bool = True,
    ):
        self.endpoint = endpoint
        self.cert_path = cert_path
        self.key_path = key_path
        self.dry_run = dry_run

    @staticmethod
    def get_payload(pronoun: str) -> str:
        """Gets the valid IRWS put payload for the given pronoun."""
        return json.dumps({"entity.profile": [{"pronoun": pronoun}]})

    def _publish_update(self, url: str, payload: str) -> NoReturn:
        if self.dry_run:
            typer.echo(f"{url} => {payload}")
            return

        response = requests.put(
            url,
            data=payload,
            cert=(self.cert_path, self.key_path),
            headers={"Content-type": "application/json", "Accept": "application/json"},
        )
        response.raise_for_status()

    def update_test_case(self, case: PronounTestCase) -> NoReturn:
        url = self.endpoint.get_url_for_netid(case.uwnetid)
        payload = self.get_payload(case.pronoun)
        self._publish_update(url, payload)


def app(
    input_file: str = typer.Option(
        ..., "--in", "-i", help="The JSON file containing the test data."
    ),
    cert_file: str = typer.Option(
        ...,
        "--cert",
        "-c",
        help="The path to the cert file you want to use for the connection.",
    ),
    key_file: str = typer.Option(
        ...,
        "--key",
        "-k",
        help="The path to the key file that goes with the cert file.",
    ),
    target_endpoint: IRWSEndpoint = typer.Option(
        IRWSEndpoint.eval.value, "--target", "-t", help="The IRWS api endpoint to use."
    ),
    dry_run: bool = typer.Option(
        True,
        "--publish",
        "-p",
        help="This runs in dry-run mode by default. Use this option to actually push data.",
    ),
):
    abort = False
    if not os.path.exists(input_file):
        typer.echo(f"Input file '{input_file}' does not exist!", color=typer.colors.RED)
        abort = not dry_run
    if not os.path.exists(cert_file):
        typer.echo(
            f"SSL cert file '{cert_file}' does not exist", color=typer.colors.RED
        )
        abort = not dry_run
    if not os.path.exists(key_file):
        typer.echo(f"SSL key file '{key_file}' does not exist", color=typer.colors.RED)
        abort = not dry_run

    if abort:
        typer.Exit()

    client = PronounsClient(target_endpoint, cert_file, key_file, dry_run)
    test_data = GeneratedTestData.parse_file(input_file)
    for profile in test_data.test_cases:
        typer.echo(
            f"Setting pronoun for UW NetID '{profile.uwnetid}' to {profile.pronoun}"
        )
        try:
            client.update_test_case(profile)
        except requests.HTTPError as e:
            response = cast(requests.Response, e.response)
            message = (
                f'FAILED: [{response.status_code}] {response.content.decode("UTF-8")}'
            )
            typer.echo(message, color=typer.colors.RED)


if __name__ == "__main__":
    typer.run(app)
