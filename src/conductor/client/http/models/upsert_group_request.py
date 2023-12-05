import pprint
import re  # noqa: F401

import six

class UpsertGroupRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'description': 'str',
        'roles': 'list[str]'
    }

    attribute_map = {
        'description': 'description',
        'roles': 'roles'
    }

    def __init__(self, description=None, roles=None):  # noqa: E501
        """UpsertGroupRequest - a model defined in Swagger"""  # noqa: E501
        self._description = None
        self._roles = None
        self.discriminator = None
        self.description = description
        if roles is not None:
            self.roles = roles

    @property
    def description(self):
        """Gets the description of this UpsertGroupRequest.  # noqa: E501

        A general description of the group  # noqa: E501

        :return: The description of this UpsertGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpsertGroupRequest.

        A general description of the group  # noqa: E501

        :param description: The description of this UpsertGroupRequest.  # noqa: E501
        :type: str
        """
        self._description = description

    @property
    def roles(self):
        """Gets the roles of this UpsertGroupRequest.  # noqa: E501


        :return: The roles of this UpsertGroupRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this UpsertGroupRequest.


        :param roles: The roles of this UpsertGroupRequest.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["ADMIN", "USER", "WORKER", "METADATA_MANAGER", "WORKFLOW_MANAGER"]  # noqa: E501
        if not set(roles).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `roles` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(roles) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._roles = roles

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(UpsertGroupRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpsertGroupRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
