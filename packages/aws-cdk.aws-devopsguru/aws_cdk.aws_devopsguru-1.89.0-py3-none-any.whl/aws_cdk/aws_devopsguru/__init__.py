"""
# AWS::DevOpsGuru Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_devopsguru as devopsguru
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnNotificationChannel(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-devopsguru.CfnNotificationChannel",
):
    """A CloudFormation ``AWS::DevOpsGuru::NotificationChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html
    :cloudformationResource: AWS::DevOpsGuru::NotificationChannel
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        config: typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", aws_cdk.core.IResolvable],
    ) -> None:
        """Create a new ``AWS::DevOpsGuru::NotificationChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param config: ``AWS::DevOpsGuru::NotificationChannel.Config``.
        """
        props = CfnNotificationChannelProps(config=config)

        jsii.create(CfnNotificationChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        """
        :cloudformationAttribute: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", aws_cdk.core.IResolvable]:
        """``AWS::DevOpsGuru::NotificationChannel.Config``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html#cfn-devopsguru-notificationchannel-config
        """
        return jsii.get(self, "config")

    @config.setter # type: ignore
    def config(
        self,
        value: typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "config", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-devopsguru.CfnNotificationChannel.NotificationChannelConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"sns": "sns"},
    )
    class NotificationChannelConfigProperty:
        def __init__(
            self,
            *,
            sns: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnNotificationChannel.SnsChannelConfigProperty"]] = None,
        ) -> None:
            """
            :param sns: ``CfnNotificationChannel.NotificationChannelConfigProperty.Sns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationchannelconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if sns is not None:
                self._values["sns"] = sns

        @builtins.property
        def sns(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnNotificationChannel.SnsChannelConfigProperty"]]:
            """``CfnNotificationChannel.NotificationChannelConfigProperty.Sns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationchannelconfig.html#cfn-devopsguru-notificationchannel-notificationchannelconfig-sns
            """
            result = self._values.get("sns")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationChannelConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-devopsguru.CfnNotificationChannel.SnsChannelConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_arn": "topicArn"},
    )
    class SnsChannelConfigProperty:
        def __init__(self, *, topic_arn: typing.Optional[builtins.str] = None) -> None:
            """
            :param topic_arn: ``CfnNotificationChannel.SnsChannelConfigProperty.TopicArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-snschannelconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            """``CfnNotificationChannel.SnsChannelConfigProperty.TopicArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-snschannelconfig.html#cfn-devopsguru-notificationchannel-snschannelconfig-topicarn
            """
            result = self._values.get("topic_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsChannelConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-devopsguru.CfnNotificationChannelProps",
    jsii_struct_bases=[],
    name_mapping={"config": "config"},
)
class CfnNotificationChannelProps:
    def __init__(
        self,
        *,
        config: typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, aws_cdk.core.IResolvable],
    ) -> None:
        """Properties for defining a ``AWS::DevOpsGuru::NotificationChannel``.

        :param config: ``AWS::DevOpsGuru::NotificationChannel.Config``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "config": config,
        }

    @builtins.property
    def config(
        self,
    ) -> typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, aws_cdk.core.IResolvable]:
        """``AWS::DevOpsGuru::NotificationChannel.Config``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html#cfn-devopsguru-notificationchannel-config
        """
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnResourceCollection(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-devopsguru.CfnResourceCollection",
):
    """A CloudFormation ``AWS::DevOpsGuru::ResourceCollection``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html
    :cloudformationResource: AWS::DevOpsGuru::ResourceCollection
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        resource_collection_filter: typing.Union[aws_cdk.core.IResolvable, "CfnResourceCollection.ResourceCollectionFilterProperty"],
    ) -> None:
        """Create a new ``AWS::DevOpsGuru::ResourceCollection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_collection_filter: ``AWS::DevOpsGuru::ResourceCollection.ResourceCollectionFilter``.
        """
        props = CfnResourceCollectionProps(
            resource_collection_filter=resource_collection_filter
        )

        jsii.create(CfnResourceCollection, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrResourceCollectionType")
    def attr_resource_collection_type(self) -> builtins.str:
        """
        :cloudformationAttribute: ResourceCollectionType
        """
        return jsii.get(self, "attrResourceCollectionType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resourceCollectionFilter")
    def resource_collection_filter(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnResourceCollection.ResourceCollectionFilterProperty"]:
        """``AWS::DevOpsGuru::ResourceCollection.ResourceCollectionFilter``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter
        """
        return jsii.get(self, "resourceCollectionFilter")

    @resource_collection_filter.setter # type: ignore
    def resource_collection_filter(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnResourceCollection.ResourceCollectionFilterProperty"],
    ) -> None:
        jsii.set(self, "resourceCollectionFilter", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-devopsguru.CfnResourceCollection.CloudFormationCollectionFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"stack_names": "stackNames"},
    )
    class CloudFormationCollectionFilterProperty:
        def __init__(
            self,
            *,
            stack_names: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param stack_names: ``CfnResourceCollection.CloudFormationCollectionFilterProperty.StackNames``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-cloudformationcollectionfilter.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if stack_names is not None:
                self._values["stack_names"] = stack_names

        @builtins.property
        def stack_names(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnResourceCollection.CloudFormationCollectionFilterProperty.StackNames``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-cloudformationcollectionfilter.html#cfn-devopsguru-resourcecollection-cloudformationcollectionfilter-stacknames
            """
            result = self._values.get("stack_names")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudFormationCollectionFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-devopsguru.CfnResourceCollection.ResourceCollectionFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_formation": "cloudFormation"},
    )
    class ResourceCollectionFilterProperty:
        def __init__(
            self,
            *,
            cloud_formation: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceCollection.CloudFormationCollectionFilterProperty"]] = None,
        ) -> None:
            """
            :param cloud_formation: ``CfnResourceCollection.ResourceCollectionFilterProperty.CloudFormation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-resourcecollectionfilter.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if cloud_formation is not None:
                self._values["cloud_formation"] = cloud_formation

        @builtins.property
        def cloud_formation(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnResourceCollection.CloudFormationCollectionFilterProperty"]]:
            """``CfnResourceCollection.ResourceCollectionFilterProperty.CloudFormation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-resourcecollectionfilter.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter-cloudformation
            """
            result = self._values.get("cloud_formation")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceCollectionFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-devopsguru.CfnResourceCollectionProps",
    jsii_struct_bases=[],
    name_mapping={"resource_collection_filter": "resourceCollectionFilter"},
)
class CfnResourceCollectionProps:
    def __init__(
        self,
        *,
        resource_collection_filter: typing.Union[aws_cdk.core.IResolvable, CfnResourceCollection.ResourceCollectionFilterProperty],
    ) -> None:
        """Properties for defining a ``AWS::DevOpsGuru::ResourceCollection``.

        :param resource_collection_filter: ``AWS::DevOpsGuru::ResourceCollection.ResourceCollectionFilter``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "resource_collection_filter": resource_collection_filter,
        }

    @builtins.property
    def resource_collection_filter(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnResourceCollection.ResourceCollectionFilterProperty]:
        """``AWS::DevOpsGuru::ResourceCollection.ResourceCollectionFilter``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter
        """
        result = self._values.get("resource_collection_filter")
        assert result is not None, "Required property 'resource_collection_filter' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceCollectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnNotificationChannel",
    "CfnNotificationChannelProps",
    "CfnResourceCollection",
    "CfnResourceCollectionProps",
]

publication.publish()
