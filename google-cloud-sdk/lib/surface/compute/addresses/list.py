# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command for listing addresses."""
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import lister
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute.addresses import flags


class List(base.ListCommand):
  """List addresses."""

  @staticmethod
  def Args(parser):
    parser.display_info.AddFormat("""\
        table(
          name,
          region.basename(),
          address,
          status
        )""")
    lister.AddMultiScopeListerFlags(parser, regional=True, global_=True)
    parser.display_info.AddCacheUpdater(flags.AddressesCompleter)

  def Run(self, args):
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client

    request_data = lister.ParseMultiScopeFlags(args, holder.resources)

    list_implementation = lister.MultiScopeLister(
        client,
        regional_service=client.apitools_client.addresses,
        global_service=client.apitools_client.globalAddresses,
        aggregation_service=client.apitools_client.addresses)

    return lister.Invoke(request_data, list_implementation)


List.detailed_help = {
    'brief': 'List addresses',
    'DESCRIPTION': """\
        *{command}* lists summary information of addresses in a project. The
        *--uri* option can be used to display URIs instead. Users who want to
        see more data should use `gcloud compute addresses describe`.

        By default, global addresses and addresses from all regions are listed.
        The results can be narrowed down by providing the *--regions* or
        *--global* flag.
        """,
    'EXAMPLES': """\
        To list all addresses in a project in table form, run:

          $ {command}

        To list the URIs of all addresses in a project, run:

          $ {command} --uri

        To list all of the global addresses in a project, run:

          $ {command} --global

        To list all of the regional addresses in a project, run:

          $ {command} --regions

        To list all of the addresses from the ``us-central1'' and the
        ``europe-west1'' regions, run:

          $ {command} --regions us-central1,europe-west1
        """,

}
