# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Implementation of the 'aea generate' subcommand."""

import os

import click

from aea.cli.fingerprint import fingerprint_item
from aea.cli.utils.context import Context
from aea.cli.utils.decorators import check_aea_project, clean_after, pass_ctx
from aea.cli.utils.loggers import logger
from aea.configurations.base import ProtocolSpecificationParseError, PublicId
from aea.configurations.constants import DEFAULT_AEA_CONFIG_FILE, PROTOCOL
from aea.protocols.generator.base import ProtocolGenerator
from aea.protocols.generator.common import load_protocol_specification


@click.group()
@click.pass_context
@check_aea_project
def generate(
    click_context: click.core.Context,  # pylint: disable=unused-argument
) -> None:
    """Generate a package for the agent."""


@generate.command()
@click.argument("protocol_specification_path", type=str, required=True)
@pass_ctx
def protocol(ctx: Context, protocol_specification_path: str) -> None:
    """Generate a protocol based on a specification and add it to the configuration file and agent."""
    _generate_item(ctx, PROTOCOL, protocol_specification_path)


@clean_after
def _generate_item(ctx: Context, item_type: str, specification_path: str) -> None:
    """Generate an item based on a specification and add it to the configuration file and agent."""
    # Get existing items
    existing_id_list = getattr(ctx.agent_config, "{}s".format(item_type))
    existing_item_list = [public_id.name for public_id in existing_id_list]

    item_type_plural = item_type + "s"

    # Load item specification yaml file
    try:
        protocol_spec = load_protocol_specification(specification_path)
    except Exception as e:
        raise click.ClickException(str(e))

    protocol_directory_path = os.path.join(
        ctx.cwd, item_type_plural, protocol_spec.name
    )

    # Check if we already have an item with the same name in the agent config
    logger.debug(
        "{} already supported by the agent: {}".format(
            item_type_plural, existing_item_list
        )
    )
    if protocol_spec.name in existing_item_list:
        raise click.ClickException(
            "A {} with name '{}' already exists. Aborting...".format(
                item_type, protocol_spec.name
            )
        )
    # Check if we already have a directory with the same name in the resource directory (e.g. protocols) of the agent's directory
    if os.path.exists(protocol_directory_path):
        raise click.ClickException(
            "A directory with name '{}' already exists. Aborting...".format(
                protocol_spec.name
            )
        )

    ctx.clean_paths.append(protocol_directory_path)
    try:
        agent_name = ctx.agent_config.agent_name
        click.echo(
            "Generating {} '{}' and adding it to the agent '{}'...".format(
                item_type, protocol_spec.name, agent_name
            )
        )

        output_path = os.path.join(ctx.cwd, item_type_plural)
        protocol_generator = ProtocolGenerator(specification_path, output_path)
        warning_message = protocol_generator.generate()
        if warning_message is not None:
            click.echo(warning_message)

        # Add the item to the configurations
        logger.debug(
            "Registering the {} into {}".format(item_type, DEFAULT_AEA_CONFIG_FILE)
        )
        existing_id_list.add(
            PublicId(protocol_spec.author, protocol_spec.name, protocol_spec.version)
        )
        ctx.agent_loader.dump(
            ctx.agent_config, open(os.path.join(ctx.cwd, DEFAULT_AEA_CONFIG_FILE), "w")
        )
    except FileExistsError:
        raise click.ClickException(  # pragma: no cover
            "A {} with this name already exists. Please choose a different name and try again.".format(
                item_type
            )
        )
    except ProtocolSpecificationParseError as e:
        raise click.ClickException(  # pragma: no cover
            "The following error happened while parsing the protocol specification: "
            + str(e)
        )
    except Exception as e:
        raise click.ClickException(
            "Protocol is NOT generated. The following error happened while generating the protocol:\n"
            + str(e)
        )
    fingerprint_item(ctx, PROTOCOL, protocol_spec.public_id)
