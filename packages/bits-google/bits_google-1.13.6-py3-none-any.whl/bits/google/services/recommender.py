# -*- coding: utf-8 -*-
"""Recommender API class file."""

from bits.google.services.base import Base
from google.auth.transport.requests import AuthorizedSession


class Recommender(Base):
    """Recommender class."""

    def __init__(self, credentials):
        """Initialize a class instance."""
        api_base_url = "https://recommender.googleapis.com"
        api_version = "v1beta1"
        self.base_url = f"{api_base_url}/{api_version}"
        self.credentials = credentials
        self.requests = AuthorizedSession(self.credentials)

    #
    # Insights
    #
    def get_insights(self, resource, zone, recommender):
        """Return a list of insights."""
        url = "%s/%s/locations/%s/insightTypes/%s/insights" % (
            self.base_url,
            resource,
            zone,
            recommender,
        )
        response = self.requests.get(url)

        # check for error
        response.raise_for_status()

        # return list
        return response.json().get("insights", [])

    # Compute Commitments
    def get_commited_use_discount_insights(self, resource, zone):
        """Return committed use discount insights for a resource."""
        recommender = "google.compute.commitment.UsageCommitmentInsight"
        return self.get_insights(resource, zone, recommender)

    # Compute Machine Types
    def get_instance_machine_type_insights(self, resource, zone):
        """Return instance rightsizing insights for a resource."""
        recommender = "google.compute.instance.MachineTypeInsight"
        return self.get_insights(resource, zone, recommender)

    def get_instance_group_machine_type_insights(self, resource, zone):
        """Return instance group rightsizing insights for a resource."""
        recommender = "google.compute.instanceGroupManager.MachineTypeInsight"
        return self.get_insights(resource, zone, recommender)

    # Compute Resources
    def get_address_idle_resource_insights(self, resource, zone):
        """Return idle address insights for a resource."""
        recommender = "google.compute.address.IdleResourceInsight"
        return self.get_insights(resource, zone, recommender)

    def get_disk_idle_resource_insights(self, resource, zone):
        """Return idle disk insights for a resource."""
        recommender = "google.compute.disk.IdleResourceInsight"
        return self.get_insights(resource, zone, recommender)

    def get_image_idle_resource_insights(self, resource, zone):
        """Return idle image insights for a resource."""
        recommender = "google.compute.image.IdleResourceInsight"
        return self.get_insights(resource, zone, recommender)

    def get_instance_idle_resource_insights(self, resource, zone):
        """Return idle instance insights for a resource."""
        recommender = "google.compute.instance.IdleResourceInsight"
        return self.get_insights(resource, zone, recommender)

    # IAM
    def get_iam_policy_insights(self, resource):
        """Return IAM policy insights for a resource."""
        recommender = "google.iam.policy.Insight"
        return self.get_insights(resource, "global", recommender)

    # Product Suggestions
    def get_logging_container_insights(self, resource, zone):
        """Return IAM policy insights for a resource."""
        recommender = "google.logging.productSuggestion.ContainerInsight"
        return self.get_insights(resource, zone, recommender)

    def get_monitoring_compute_insights(self, resource, zone):
        """Return IAM policy insights for a resource."""
        recommender = "google.monitoring.productSuggestion.ComputeInsight"
        return self.get_insights(resource, zone, recommender)

    # Resource Manager
    def get_unattended_projects_insights(self, resource):
        """Return IAM policy insights for a resource."""
        recommender = "google.resourcemanager.projectUtilization.Insight"
        return self.get_insights(resource, "global", recommender)

    #
    # Recommendations
    #
    def get_recommendations(self, resource, zone, recommender):
        """Return a list of recommendations."""
        url = "%s/%s/locations/%s/recommenders/%s/recommendations" % (
            self.base_url,
            resource,
            zone,
            recommender,
        )
        response = self.requests.get(url)

        # check for error
        response.raise_for_status()

        # return list
        return response.json().get("recommendations", [])

    # Compute Commitments
    def get_commited_use_discount_recommendations(self, resource, zone):
        """Return committed use discount recommendations for a resource."""
        recommender = "google.compute.commitment.UsageCommitmentRecommender"
        return self.get_recommendations(resource, zone, recommender)

    # Compute Machine Types
    def get_instance_machine_type_recommendations(self, resource, zone):
        """Return instance rightsizing recommendations for a resource."""
        recommender = "google.compute.instance.MachineTypeRecommender"
        return self.get_recommendations(resource, zone, recommender)

    def get_instance_group_machine_type_recommendations(self, resource, zone):
        """Return instance group rightsizing recommendations for a resource."""
        recommender = "google.compute.instanceGroupManager.MachineTypeRecommender"
        return self.get_recommendations(resource, zone, recommender)

    # Compute Resources
    def get_address_idle_resource_recommendations(self, resource, zone):
        """Return idle address recommendations for a resource."""
        recommender = "google.compute.address.IdleResourceRecommender"
        return self.get_recommendations(resource, zone, recommender)

    def get_disk_idle_resource_recommendations(self, resource, zone):
        """Return idle disk recommendations for a resource."""
        recommender = "google.compute.disk.IdleResourceRecommender"
        return self.get_recommendations(resource, zone, recommender)

    def get_image_idle_resource_recommendations(self, resource, zone):
        """Return idle image recommendations for a resource."""
        recommender = "google.compute.image.IdleResourceRecommender"
        return self.get_recommendations(resource, zone, recommender)

    def get_instance_idle_resource_recommendations(self, resource, zone):
        """Return idle instance recommendations for a resource."""
        recommender = "google.compute.instance.IdleResourceRecommender"
        return self.get_recommendations(resource, zone, recommender)

    # IAM
    def get_iam_policy_recommendations(self, resource):
        """Return IAM policy recommendations for a resource."""
        recommender = "google.iam.policy.Recommender"
        return self.get_recommendations(resource, "global", recommender)

    # Product Suggestions
    def get_logging_container_recommendations(self, resource, zone):
        """Return IAM policy recommendations for a resource."""
        recommender = "google.logging.productSuggestion.ContainerRecommender"
        return self.get_recommendations(resource, zone, recommender)

    def get_monitoring_compute_recommendations(self, resource, zone):
        """Return IAM policy recommendations for a resource."""
        recommender = "google.monitoring.productSuggestion.ComputeRecommender"
        return self.get_recommendations(resource, zone, recommender)

    # Resource Manager
    def get_unattended_projects_recommendations(self, resource):
        """Return IAM policy recommendations for a resource."""
        recommender = "google.resourcemanager.projectUtilization.Recommender"
        return self.get_recommendations(resource, "global", recommender)
