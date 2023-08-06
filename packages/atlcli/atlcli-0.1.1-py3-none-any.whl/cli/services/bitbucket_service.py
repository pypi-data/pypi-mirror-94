import json
import re
import semantic_version
import requests
from atlassian import Bitbucket
from atlassian import Jira
from cli.utils import ConfigurationManager

import pprint36 as pprint


class BitbucketService:

    # bitbucketInstance = None
    confManager = ConfigurationManager()

    def __init__(self, skipssl):
        self.config = self.confManager.load_config()
        self.skipssl = skipssl

        if self.config is not None:
            self.bitbucketInstance = Bitbucket(
                url=self.config["bitbucket-url"],
                username=self.config["credentials"]["username"],
                password=self.config["credentials"]["password"])

    def get_release(self, product_name, component_name, version):

        result = self.bitbucketInstance.get_project_tags(product_name,
                                                         component_name, version)
        tags = result["values"]
        target_tag = next(
            filter(lambda x: x["displayId"] == version, tags), None)

        previous_tag = self.getPreviousMajorRelease(tags, target_tag)
        changelog = self.get_tasks_between_tags(
            previous_tag["displayId"], target_tag["displayId"])

        return changelog

    def get_tasks_between_tags(self, since_tag, until_tag):
        jira_tickets = []
        endpoint_url = "{0}rest/api/1.0/projects/HABITATION-ACHAT/repos/web-spa/commits".format(
            self.config["bitbucket-url"])

        querystring = {
            "since": since_tag,
            "until": until_tag,
            "merges": "include",
            "limit": "1000"
        }

        payload = ""
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic {0}".format(self.config["credentials"]["base64"])
        }

        response = requests.request(
            "GET", endpoint_url, data=payload, headers=headers, params=querystring, verify=self.skipssl)
        result = json.loads(response.text)

        for t in result["values"]:
            for j in t["properties"]["jira-key"]:
                if j not in jira_tickets:
                    jira_tickets.append(j)

        return jira_tickets

    def filterMajorReleases(self, tags):
        filtered_tags = []
        pattern = re.compile(
            r"^([0-9]+)\.([0-9]+)\.([0-9]+)$")
        filtered_tags = list(
            filter(lambda x: pattern.match(x["displayId"]) is not None, tags))

        return filtered_tags

    def getPreviousMajorRelease(self, tags, version):
        filtered_tags = self.filterMajorReleases(tags)
        previous_release = None
        position = filtered_tags.index(version)

        if position > 0 and (position+1) < len(filtered_tags):
            previous_release = filtered_tags[position+1]
            return previous_release
        else:
            return version
