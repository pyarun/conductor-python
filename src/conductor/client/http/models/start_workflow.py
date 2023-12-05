import pprint
import re  # noqa: F401

import six

class StartWorkflow(object):
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
        'name': 'str',
        'version': 'int',
        'correlation_id': 'str',
        'input': 'dict(str, object)',
        'task_to_domain': 'dict(str, str)'
    }

    attribute_map = {
        'name': 'name',
        'version': 'version',
        'correlation_id': 'correlationId',
        'input': 'input',
        'task_to_domain': 'taskToDomain'
    }

    def __init__(self, name=None, version=None, correlation_id=None, input=None, task_to_domain=None):  # noqa: E501
        """StartWorkflow - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._version = None
        self._correlation_id = None
        self._input = None
        self._task_to_domain = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if version is not None:
            self.version = version
        if correlation_id is not None:
            self.correlation_id = correlation_id
        if input is not None:
            self.input = input
        if task_to_domain is not None:
            self.task_to_domain = task_to_domain

    @property
    def name(self):
        """Gets the name of this StartWorkflow.  # noqa: E501


        :return: The name of this StartWorkflow.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this StartWorkflow.


        :param name: The name of this StartWorkflow.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def version(self):
        """Gets the version of this StartWorkflow.  # noqa: E501


        :return: The version of this StartWorkflow.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this StartWorkflow.


        :param version: The version of this StartWorkflow.  # noqa: E501
        :type: int
        """

        self._version = version

    @property
    def correlation_id(self):
        """Gets the correlation_id of this StartWorkflow.  # noqa: E501


        :return: The correlation_id of this StartWorkflow.  # noqa: E501
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """Sets the correlation_id of this StartWorkflow.


        :param correlation_id: The correlation_id of this StartWorkflow.  # noqa: E501
        :type: str
        """

        self._correlation_id = correlation_id

    @property
    def input(self):
        """Gets the input of this StartWorkflow.  # noqa: E501


        :return: The input of this StartWorkflow.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this StartWorkflow.


        :param input: The input of this StartWorkflow.  # noqa: E501
        :type: dict(str, object)
        """

        self._input = input

    @property
    def task_to_domain(self):
        """Gets the task_to_domain of this StartWorkflow.  # noqa: E501


        :return: The task_to_domain of this StartWorkflow.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._task_to_domain

    @task_to_domain.setter
    def task_to_domain(self, task_to_domain):
        """Sets the task_to_domain of this StartWorkflow.


        :param task_to_domain: The task_to_domain of this StartWorkflow.  # noqa: E501
        :type: dict(str, str)
        """

        self._task_to_domain = task_to_domain

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
        if issubclass(StartWorkflow, dict):
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
        if not isinstance(other, StartWorkflow):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
