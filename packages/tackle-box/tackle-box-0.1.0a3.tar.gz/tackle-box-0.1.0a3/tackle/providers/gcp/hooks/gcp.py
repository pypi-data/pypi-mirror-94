# -*- coding: utf-8 -*-

"""GCP hooks."""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from googleapiclient.discovery import build

from tackle.models import BaseHook

logger = logging.getLogger(__name__)


class GcpRegionsHook(BaseHook):
    """Hook retrieving GCP regions.

    :param gcp_project: String for project name in GCP to use.
    :return: List of regions
    """

    type: str = 'gcp_regions'
    gcp_project: str

    def execute(self):
        client = build('compute', 'v1')

        regions = [
            item['name']
            for item in client.regions().list(project=self.gcp_project).execute['items']
        ]

        return regions


class GcpAzsHook(BaseHook):
    """
    Hook for retrieving the availability zones in a given region.

    :param gcp_project: String for project to deploy into
    :param region: A region to search in
    :param regions: A list of regions to search in
    :return: A list of availability zones
    """

    type: str = 'gcp_azs'
    gcp_project: str
    region: str = None
    regions: list = None

    def execute(self):
        client = build('compute', 'v1')

        if self.region:
            azs = self._call_azs(client, self.region, self.gcp_project)
            azs.sort()
            return azs

        elif self.regions:
            output = {}
            for r in self.regions:
                azs = self._call_azs(client, r, self.gcp_project)
                azs.sort()
                output.update({r: azs})
            return output

    @staticmethod
    def _call_azs(client, region, project):
        region_uri_stub = (
            "\"https://www.googleapis.com/compute/v1/projects/" + project + "/regions/"
        )
        availability_zones = [
            item['name']
            for item in client.zones()
            .list(
                project=project,
                filter="region=" + region_uri_stub + region + "\" AND status=\"UP\"",
            )
            .execute['items']
        ]
        availability_zones.sort()
        return availability_zones


class GcpInstanceTypesHook(BaseHook):
    """
    Hook retrieving the available instance types in a zone.

    :param region: [Required] The zone to determine the instances in
    :param instance_families: A list of instance families, ie ['n1', 'e2']
    :return: A list of instance types
    """

    type: str = 'gcp_instance_types'
    gcp_project: str
    zone: str
    instance_families: list = None

    def execute(self):
        client = build('compute', 'v1')

        if not self.instance_families:
            instances = [
                item['name']
                for item in client.machineTypes()
                .list(project=self.gcp_project, zone=self.zone,)
                .execute['items']
            ]

        else:
            selected_family = [name + '-*' for name in self.instance_families]

            for i, name in enumerate(selected_family):
                if i == 0:
                    query = "name = \"" + name + "\""
                else:
                    query += " OR name = \"" + name + "\""

            instances = [
                item['name']
                for item in client.machineTypes()
                .list(project=self.gcp_project, zone=self.zone, filter=query,)
                .execute['items']
            ]

        instances.sort()

        instance_sizes = [
            'micro',
            'small',
            'medium',
            'standard',
            'highcpu',
            'highmem',
            'megamem',
            'ultramem',
        ]

        instance_sizes_set = []
        for _, x in enumerate(instances):
            if len(x.split('-')) == 2:
                instance_sizes_set.append(
                    (
                        x.split('-')[0],
                        x.split('-')[1],
                        None,
                        instance_sizes.index(x.split('-')[1]),
                    )
                )
            else:
                instance_sizes_set.append(
                    (
                        x.split('-')[0],
                        x.split('-')[1],
                        x.split('-')[2],
                        instance_sizes.index(x.split('-')[1]),
                    )
                )

        instance_sizes_set.sort(key=lambda x: x[3])

        instances = []
        for s in instance_sizes_set:
            if s[2]:
                instances.append('-'.join([s[0], s[1], s[2]]))
            else:
                instances.append('-'.join([s[0], s[1]]))

        return instances
