import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnBroker(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amazonmq.CfnBroker",
):
    """A CloudFormation ``AWS::AmazonMQ::Broker``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html
    :cloudformationResource: AWS::AmazonMQ::Broker
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        auto_minor_version_upgrade: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        broker_name: builtins.str,
        deployment_mode: builtins.str,
        engine_type: builtins.str,
        engine_version: builtins.str,
        host_instance_type: builtins.str,
        publicly_accessible: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        users: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBroker.UserProperty", _IResolvable_a771d0ef]]],
        authentication_strategy: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union["CfnBroker.ConfigurationIdProperty", _IResolvable_a771d0ef]] = None,
        encryption_options: typing.Optional[typing.Union["CfnBroker.EncryptionOptionsProperty", _IResolvable_a771d0ef]] = None,
        ldap_server_metadata: typing.Optional[typing.Union["CfnBroker.LdapServerMetadataProperty", _IResolvable_a771d0ef]] = None,
        logs: typing.Optional[typing.Union["CfnBroker.LogListProperty", _IResolvable_a771d0ef]] = None,
        maintenance_window_start_time: typing.Optional[typing.Union["CfnBroker.MaintenanceWindowProperty", _IResolvable_a771d0ef]] = None,
        security_groups: typing.Optional[typing.List[builtins.str]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List["CfnBroker.TagsEntryProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::AmazonMQ::Broker``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auto_minor_version_upgrade: ``AWS::AmazonMQ::Broker.AutoMinorVersionUpgrade``.
        :param broker_name: ``AWS::AmazonMQ::Broker.BrokerName``.
        :param deployment_mode: ``AWS::AmazonMQ::Broker.DeploymentMode``.
        :param engine_type: ``AWS::AmazonMQ::Broker.EngineType``.
        :param engine_version: ``AWS::AmazonMQ::Broker.EngineVersion``.
        :param host_instance_type: ``AWS::AmazonMQ::Broker.HostInstanceType``.
        :param publicly_accessible: ``AWS::AmazonMQ::Broker.PubliclyAccessible``.
        :param users: ``AWS::AmazonMQ::Broker.Users``.
        :param authentication_strategy: ``AWS::AmazonMQ::Broker.AuthenticationStrategy``.
        :param configuration: ``AWS::AmazonMQ::Broker.Configuration``.
        :param encryption_options: ``AWS::AmazonMQ::Broker.EncryptionOptions``.
        :param ldap_server_metadata: ``AWS::AmazonMQ::Broker.LdapServerMetadata``.
        :param logs: ``AWS::AmazonMQ::Broker.Logs``.
        :param maintenance_window_start_time: ``AWS::AmazonMQ::Broker.MaintenanceWindowStartTime``.
        :param security_groups: ``AWS::AmazonMQ::Broker.SecurityGroups``.
        :param storage_type: ``AWS::AmazonMQ::Broker.StorageType``.
        :param subnet_ids: ``AWS::AmazonMQ::Broker.SubnetIds``.
        :param tags: ``AWS::AmazonMQ::Broker.Tags``.
        """
        props = CfnBrokerProps(
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            broker_name=broker_name,
            deployment_mode=deployment_mode,
            engine_type=engine_type,
            engine_version=engine_version,
            host_instance_type=host_instance_type,
            publicly_accessible=publicly_accessible,
            users=users,
            authentication_strategy=authentication_strategy,
            configuration=configuration,
            encryption_options=encryption_options,
            ldap_server_metadata=ldap_server_metadata,
            logs=logs,
            maintenance_window_start_time=maintenance_window_start_time,
            security_groups=security_groups,
            storage_type=storage_type,
            subnet_ids=subnet_ids,
            tags=tags,
        )

        jsii.create(CfnBroker, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
    @jsii.member(jsii_name="attrAmqpEndpoints")
    def attr_amqp_endpoints(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: AmqpEndpoints
        """
        return jsii.get(self, "attrAmqpEndpoints")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrConfigurationId")
    def attr_configuration_id(self) -> builtins.str:
        """
        :cloudformationAttribute: ConfigurationId
        """
        return jsii.get(self, "attrConfigurationId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrConfigurationRevision")
    def attr_configuration_revision(self) -> jsii.Number:
        """
        :cloudformationAttribute: ConfigurationRevision
        """
        return jsii.get(self, "attrConfigurationRevision")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrIpAddresses")
    def attr_ip_addresses(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: IpAddresses
        """
        return jsii.get(self, "attrIpAddresses")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrMqttEndpoints")
    def attr_mqtt_endpoints(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: MqttEndpoints
        """
        return jsii.get(self, "attrMqttEndpoints")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrOpenWireEndpoints")
    def attr_open_wire_endpoints(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: OpenWireEndpoints
        """
        return jsii.get(self, "attrOpenWireEndpoints")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrStompEndpoints")
    def attr_stomp_endpoints(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: StompEndpoints
        """
        return jsii.get(self, "attrStompEndpoints")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrWssEndpoints")
    def attr_wss_endpoints(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: WssEndpoints
        """
        return jsii.get(self, "attrWssEndpoints")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::AmazonMQ::Broker.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        """``AWS::AmazonMQ::Broker.AutoMinorVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-autominorversionupgrade
        """
        return jsii.get(self, "autoMinorVersionUpgrade")

    @auto_minor_version_upgrade.setter # type: ignore
    def auto_minor_version_upgrade(
        self,
        value: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="brokerName")
    def broker_name(self) -> builtins.str:
        """``AWS::AmazonMQ::Broker.BrokerName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-brokername
        """
        return jsii.get(self, "brokerName")

    @broker_name.setter # type: ignore
    def broker_name(self, value: builtins.str) -> None:
        jsii.set(self, "brokerName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deploymentMode")
    def deployment_mode(self) -> builtins.str:
        """``AWS::AmazonMQ::Broker.DeploymentMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-deploymentmode
        """
        return jsii.get(self, "deploymentMode")

    @deployment_mode.setter # type: ignore
    def deployment_mode(self, value: builtins.str) -> None:
        jsii.set(self, "deploymentMode", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> builtins.str:
        """``AWS::AmazonMQ::Broker.EngineType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-enginetype
        """
        return jsii.get(self, "engineType")

    @engine_type.setter # type: ignore
    def engine_type(self, value: builtins.str) -> None:
        jsii.set(self, "engineType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        """``AWS::AmazonMQ::Broker.EngineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter # type: ignore
    def engine_version(self, value: builtins.str) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="hostInstanceType")
    def host_instance_type(self) -> builtins.str:
        """``AWS::AmazonMQ::Broker.HostInstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-hostinstancetype
        """
        return jsii.get(self, "hostInstanceType")

    @host_instance_type.setter # type: ignore
    def host_instance_type(self, value: builtins.str) -> None:
        jsii.set(self, "hostInstanceType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="publiclyAccessible")
    def publicly_accessible(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        """``AWS::AmazonMQ::Broker.PubliclyAccessible``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-publiclyaccessible
        """
        return jsii.get(self, "publiclyAccessible")

    @publicly_accessible.setter # type: ignore
    def publicly_accessible(
        self,
        value: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "publiclyAccessible", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="users")
    def users(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBroker.UserProperty", _IResolvable_a771d0ef]]]:
        """``AWS::AmazonMQ::Broker.Users``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-users
        """
        return jsii.get(self, "users")

    @users.setter # type: ignore
    def users(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBroker.UserProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "users", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authenticationStrategy")
    def authentication_strategy(self) -> typing.Optional[builtins.str]:
        """``AWS::AmazonMQ::Broker.AuthenticationStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-authenticationstrategy
        """
        return jsii.get(self, "authenticationStrategy")

    @authentication_strategy.setter # type: ignore
    def authentication_strategy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "authenticationStrategy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBroker.ConfigurationIdProperty", _IResolvable_a771d0ef]]:
        """``AWS::AmazonMQ::Broker.Configuration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-configuration
        """
        return jsii.get(self, "configuration")

    @configuration.setter # type: ignore
    def configuration(
        self,
        value: typing.Optional[typing.Union["CfnBroker.ConfigurationIdProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "configuration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encryptionOptions")
    def encryption_options(
        self,
    ) -> typing.Optional[typing.Union["CfnBroker.EncryptionOptionsProperty", _IResolvable_a771d0ef]]:
        """``AWS::AmazonMQ::Broker.EncryptionOptions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-encryptionoptions
        """
        return jsii.get(self, "encryptionOptions")

    @encryption_options.setter # type: ignore
    def encryption_options(
        self,
        value: typing.Optional[typing.Union["CfnBroker.EncryptionOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "encryptionOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ldapServerMetadata")
    def ldap_server_metadata(
        self,
    ) -> typing.Optional[typing.Union["CfnBroker.LdapServerMetadataProperty", _IResolvable_a771d0ef]]:
        """``AWS::AmazonMQ::Broker.LdapServerMetadata``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-ldapservermetadata
        """
        return jsii.get(self, "ldapServerMetadata")

    @ldap_server_metadata.setter # type: ignore
    def ldap_server_metadata(
        self,
        value: typing.Optional[typing.Union["CfnBroker.LdapServerMetadataProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "ldapServerMetadata", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="logs")
    def logs(
        self,
    ) -> typing.Optional[typing.Union["CfnBroker.LogListProperty", _IResolvable_a771d0ef]]:
        """``AWS::AmazonMQ::Broker.Logs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-logs
        """
        return jsii.get(self, "logs")

    @logs.setter # type: ignore
    def logs(
        self,
        value: typing.Optional[typing.Union["CfnBroker.LogListProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "logs", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maintenanceWindowStartTime")
    def maintenance_window_start_time(
        self,
    ) -> typing.Optional[typing.Union["CfnBroker.MaintenanceWindowProperty", _IResolvable_a771d0ef]]:
        """``AWS::AmazonMQ::Broker.MaintenanceWindowStartTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-maintenancewindowstarttime
        """
        return jsii.get(self, "maintenanceWindowStartTime")

    @maintenance_window_start_time.setter # type: ignore
    def maintenance_window_start_time(
        self,
        value: typing.Optional[typing.Union["CfnBroker.MaintenanceWindowProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "maintenanceWindowStartTime", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AmazonMQ::Broker.SecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-securitygroups
        """
        return jsii.get(self, "securityGroups")

    @security_groups.setter # type: ignore
    def security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "securityGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AmazonMQ::Broker.StorageType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-storagetype
        """
        return jsii.get(self, "storageType")

    @storage_type.setter # type: ignore
    def storage_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "storageType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AmazonMQ::Broker.SubnetIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter # type: ignore
    def subnet_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "subnetIds", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_amazonmq.CfnBroker.ConfigurationIdProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "revision": "revision"},
    )
    class ConfigurationIdProperty:
        def __init__(self, *, id: builtins.str, revision: jsii.Number) -> None:
            """
            :param id: ``CfnBroker.ConfigurationIdProperty.Id``.
            :param revision: ``CfnBroker.ConfigurationIdProperty.Revision``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
                "revision": revision,
            }

        @builtins.property
        def id(self) -> builtins.str:
            """``CfnBroker.ConfigurationIdProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html#cfn-amazonmq-broker-configurationid-id
            """
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return result

        @builtins.property
        def revision(self) -> jsii.Number:
            """``CfnBroker.ConfigurationIdProperty.Revision``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html#cfn-amazonmq-broker-configurationid-revision
            """
            result = self._values.get("revision")
            assert result is not None, "Required property 'revision' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amazonmq.CfnBroker.EncryptionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"use_aws_owned_key": "useAwsOwnedKey", "kms_key_id": "kmsKeyId"},
    )
    class EncryptionOptionsProperty:
        def __init__(
            self,
            *,
            use_aws_owned_key: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param use_aws_owned_key: ``CfnBroker.EncryptionOptionsProperty.UseAwsOwnedKey``.
            :param kms_key_id: ``CfnBroker.EncryptionOptionsProperty.KmsKeyId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-encryptionoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "use_aws_owned_key": use_aws_owned_key,
            }
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def use_aws_owned_key(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            """``CfnBroker.EncryptionOptionsProperty.UseAwsOwnedKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-encryptionoptions.html#cfn-amazonmq-broker-encryptionoptions-useawsownedkey
            """
            result = self._values.get("use_aws_owned_key")
            assert result is not None, "Required property 'use_aws_owned_key' is missing"
            return result

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            """``CfnBroker.EncryptionOptionsProperty.KmsKeyId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-encryptionoptions.html#cfn-amazonmq-broker-encryptionoptions-kmskeyid
            """
            result = self._values.get("kms_key_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amazonmq.CfnBroker.LdapServerMetadataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hosts": "hosts",
            "role_base": "roleBase",
            "role_search_matching": "roleSearchMatching",
            "service_account_password": "serviceAccountPassword",
            "service_account_username": "serviceAccountUsername",
            "user_base": "userBase",
            "user_search_matching": "userSearchMatching",
            "role_name": "roleName",
            "role_search_subtree": "roleSearchSubtree",
            "user_role_name": "userRoleName",
            "user_search_subtree": "userSearchSubtree",
        },
    )
    class LdapServerMetadataProperty:
        def __init__(
            self,
            *,
            hosts: typing.List[builtins.str],
            role_base: builtins.str,
            role_search_matching: builtins.str,
            service_account_password: builtins.str,
            service_account_username: builtins.str,
            user_base: builtins.str,
            user_search_matching: builtins.str,
            role_name: typing.Optional[builtins.str] = None,
            role_search_subtree: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            user_role_name: typing.Optional[builtins.str] = None,
            user_search_subtree: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param hosts: ``CfnBroker.LdapServerMetadataProperty.Hosts``.
            :param role_base: ``CfnBroker.LdapServerMetadataProperty.RoleBase``.
            :param role_search_matching: ``CfnBroker.LdapServerMetadataProperty.RoleSearchMatching``.
            :param service_account_password: ``CfnBroker.LdapServerMetadataProperty.ServiceAccountPassword``.
            :param service_account_username: ``CfnBroker.LdapServerMetadataProperty.ServiceAccountUsername``.
            :param user_base: ``CfnBroker.LdapServerMetadataProperty.UserBase``.
            :param user_search_matching: ``CfnBroker.LdapServerMetadataProperty.UserSearchMatching``.
            :param role_name: ``CfnBroker.LdapServerMetadataProperty.RoleName``.
            :param role_search_subtree: ``CfnBroker.LdapServerMetadataProperty.RoleSearchSubtree``.
            :param user_role_name: ``CfnBroker.LdapServerMetadataProperty.UserRoleName``.
            :param user_search_subtree: ``CfnBroker.LdapServerMetadataProperty.UserSearchSubtree``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "hosts": hosts,
                "role_base": role_base,
                "role_search_matching": role_search_matching,
                "service_account_password": service_account_password,
                "service_account_username": service_account_username,
                "user_base": user_base,
                "user_search_matching": user_search_matching,
            }
            if role_name is not None:
                self._values["role_name"] = role_name
            if role_search_subtree is not None:
                self._values["role_search_subtree"] = role_search_subtree
            if user_role_name is not None:
                self._values["user_role_name"] = user_role_name
            if user_search_subtree is not None:
                self._values["user_search_subtree"] = user_search_subtree

        @builtins.property
        def hosts(self) -> typing.List[builtins.str]:
            """``CfnBroker.LdapServerMetadataProperty.Hosts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-hosts
            """
            result = self._values.get("hosts")
            assert result is not None, "Required property 'hosts' is missing"
            return result

        @builtins.property
        def role_base(self) -> builtins.str:
            """``CfnBroker.LdapServerMetadataProperty.RoleBase``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolebase
            """
            result = self._values.get("role_base")
            assert result is not None, "Required property 'role_base' is missing"
            return result

        @builtins.property
        def role_search_matching(self) -> builtins.str:
            """``CfnBroker.LdapServerMetadataProperty.RoleSearchMatching``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolesearchmatching
            """
            result = self._values.get("role_search_matching")
            assert result is not None, "Required property 'role_search_matching' is missing"
            return result

        @builtins.property
        def service_account_password(self) -> builtins.str:
            """``CfnBroker.LdapServerMetadataProperty.ServiceAccountPassword``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-serviceaccountpassword
            """
            result = self._values.get("service_account_password")
            assert result is not None, "Required property 'service_account_password' is missing"
            return result

        @builtins.property
        def service_account_username(self) -> builtins.str:
            """``CfnBroker.LdapServerMetadataProperty.ServiceAccountUsername``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-serviceaccountusername
            """
            result = self._values.get("service_account_username")
            assert result is not None, "Required property 'service_account_username' is missing"
            return result

        @builtins.property
        def user_base(self) -> builtins.str:
            """``CfnBroker.LdapServerMetadataProperty.UserBase``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-userbase
            """
            result = self._values.get("user_base")
            assert result is not None, "Required property 'user_base' is missing"
            return result

        @builtins.property
        def user_search_matching(self) -> builtins.str:
            """``CfnBroker.LdapServerMetadataProperty.UserSearchMatching``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-usersearchmatching
            """
            result = self._values.get("user_search_matching")
            assert result is not None, "Required property 'user_search_matching' is missing"
            return result

        @builtins.property
        def role_name(self) -> typing.Optional[builtins.str]:
            """``CfnBroker.LdapServerMetadataProperty.RoleName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolename
            """
            result = self._values.get("role_name")
            return result

        @builtins.property
        def role_search_subtree(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            """``CfnBroker.LdapServerMetadataProperty.RoleSearchSubtree``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-rolesearchsubtree
            """
            result = self._values.get("role_search_subtree")
            return result

        @builtins.property
        def user_role_name(self) -> typing.Optional[builtins.str]:
            """``CfnBroker.LdapServerMetadataProperty.UserRoleName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-userrolename
            """
            result = self._values.get("user_role_name")
            return result

        @builtins.property
        def user_search_subtree(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            """``CfnBroker.LdapServerMetadataProperty.UserSearchSubtree``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-ldapservermetadata.html#cfn-amazonmq-broker-ldapservermetadata-usersearchsubtree
            """
            result = self._values.get("user_search_subtree")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LdapServerMetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amazonmq.CfnBroker.LogListProperty",
        jsii_struct_bases=[],
        name_mapping={"audit": "audit", "general": "general"},
    )
    class LogListProperty:
        def __init__(
            self,
            *,
            audit: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            general: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param audit: ``CfnBroker.LogListProperty.Audit``.
            :param general: ``CfnBroker.LogListProperty.General``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if audit is not None:
                self._values["audit"] = audit
            if general is not None:
                self._values["general"] = general

        @builtins.property
        def audit(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            """``CfnBroker.LogListProperty.Audit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html#cfn-amazonmq-broker-loglist-audit
            """
            result = self._values.get("audit")
            return result

        @builtins.property
        def general(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            """``CfnBroker.LogListProperty.General``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html#cfn-amazonmq-broker-loglist-general
            """
            result = self._values.get("general")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amazonmq.CfnBroker.MaintenanceWindowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "day_of_week": "dayOfWeek",
            "time_of_day": "timeOfDay",
            "time_zone": "timeZone",
        },
    )
    class MaintenanceWindowProperty:
        def __init__(
            self,
            *,
            day_of_week: builtins.str,
            time_of_day: builtins.str,
            time_zone: builtins.str,
        ) -> None:
            """
            :param day_of_week: ``CfnBroker.MaintenanceWindowProperty.DayOfWeek``.
            :param time_of_day: ``CfnBroker.MaintenanceWindowProperty.TimeOfDay``.
            :param time_zone: ``CfnBroker.MaintenanceWindowProperty.TimeZone``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "day_of_week": day_of_week,
                "time_of_day": time_of_day,
                "time_zone": time_zone,
            }

        @builtins.property
        def day_of_week(self) -> builtins.str:
            """``CfnBroker.MaintenanceWindowProperty.DayOfWeek``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-dayofweek
            """
            result = self._values.get("day_of_week")
            assert result is not None, "Required property 'day_of_week' is missing"
            return result

        @builtins.property
        def time_of_day(self) -> builtins.str:
            """``CfnBroker.MaintenanceWindowProperty.TimeOfDay``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-timeofday
            """
            result = self._values.get("time_of_day")
            assert result is not None, "Required property 'time_of_day' is missing"
            return result

        @builtins.property
        def time_zone(self) -> builtins.str:
            """``CfnBroker.MaintenanceWindowProperty.TimeZone``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-timezone
            """
            result = self._values.get("time_zone")
            assert result is not None, "Required property 'time_zone' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amazonmq.CfnBroker.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            """
            :param key: ``CfnBroker.TagsEntryProperty.Key``.
            :param value: ``CfnBroker.TagsEntryProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnBroker.TagsEntryProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html#cfn-amazonmq-broker-tagsentry-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnBroker.TagsEntryProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html#cfn-amazonmq-broker-tagsentry-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amazonmq.CfnBroker.UserProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "username": "username",
            "console_access": "consoleAccess",
            "groups": "groups",
        },
    )
    class UserProperty:
        def __init__(
            self,
            *,
            password: builtins.str,
            username: builtins.str,
            console_access: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            groups: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param password: ``CfnBroker.UserProperty.Password``.
            :param username: ``CfnBroker.UserProperty.Username``.
            :param console_access: ``CfnBroker.UserProperty.ConsoleAccess``.
            :param groups: ``CfnBroker.UserProperty.Groups``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "password": password,
                "username": username,
            }
            if console_access is not None:
                self._values["console_access"] = console_access
            if groups is not None:
                self._values["groups"] = groups

        @builtins.property
        def password(self) -> builtins.str:
            """``CfnBroker.UserProperty.Password``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-password
            """
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return result

        @builtins.property
        def username(self) -> builtins.str:
            """``CfnBroker.UserProperty.Username``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-username
            """
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return result

        @builtins.property
        def console_access(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            """``CfnBroker.UserProperty.ConsoleAccess``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-consoleaccess
            """
            result = self._values.get("console_access")
            return result

        @builtins.property
        def groups(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnBroker.UserProperty.Groups``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-groups
            """
            result = self._values.get("groups")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_amazonmq.CfnBrokerProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "broker_name": "brokerName",
        "deployment_mode": "deploymentMode",
        "engine_type": "engineType",
        "engine_version": "engineVersion",
        "host_instance_type": "hostInstanceType",
        "publicly_accessible": "publiclyAccessible",
        "users": "users",
        "authentication_strategy": "authenticationStrategy",
        "configuration": "configuration",
        "encryption_options": "encryptionOptions",
        "ldap_server_metadata": "ldapServerMetadata",
        "logs": "logs",
        "maintenance_window_start_time": "maintenanceWindowStartTime",
        "security_groups": "securityGroups",
        "storage_type": "storageType",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnBrokerProps:
    def __init__(
        self,
        *,
        auto_minor_version_upgrade: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        broker_name: builtins.str,
        deployment_mode: builtins.str,
        engine_type: builtins.str,
        engine_version: builtins.str,
        host_instance_type: builtins.str,
        publicly_accessible: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        users: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBroker.UserProperty, _IResolvable_a771d0ef]]],
        authentication_strategy: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[CfnBroker.ConfigurationIdProperty, _IResolvable_a771d0ef]] = None,
        encryption_options: typing.Optional[typing.Union[CfnBroker.EncryptionOptionsProperty, _IResolvable_a771d0ef]] = None,
        ldap_server_metadata: typing.Optional[typing.Union[CfnBroker.LdapServerMetadataProperty, _IResolvable_a771d0ef]] = None,
        logs: typing.Optional[typing.Union[CfnBroker.LogListProperty, _IResolvable_a771d0ef]] = None,
        maintenance_window_start_time: typing.Optional[typing.Union[CfnBroker.MaintenanceWindowProperty, _IResolvable_a771d0ef]] = None,
        security_groups: typing.Optional[typing.List[builtins.str]] = None,
        storage_type: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[CfnBroker.TagsEntryProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::AmazonMQ::Broker``.

        :param auto_minor_version_upgrade: ``AWS::AmazonMQ::Broker.AutoMinorVersionUpgrade``.
        :param broker_name: ``AWS::AmazonMQ::Broker.BrokerName``.
        :param deployment_mode: ``AWS::AmazonMQ::Broker.DeploymentMode``.
        :param engine_type: ``AWS::AmazonMQ::Broker.EngineType``.
        :param engine_version: ``AWS::AmazonMQ::Broker.EngineVersion``.
        :param host_instance_type: ``AWS::AmazonMQ::Broker.HostInstanceType``.
        :param publicly_accessible: ``AWS::AmazonMQ::Broker.PubliclyAccessible``.
        :param users: ``AWS::AmazonMQ::Broker.Users``.
        :param authentication_strategy: ``AWS::AmazonMQ::Broker.AuthenticationStrategy``.
        :param configuration: ``AWS::AmazonMQ::Broker.Configuration``.
        :param encryption_options: ``AWS::AmazonMQ::Broker.EncryptionOptions``.
        :param ldap_server_metadata: ``AWS::AmazonMQ::Broker.LdapServerMetadata``.
        :param logs: ``AWS::AmazonMQ::Broker.Logs``.
        :param maintenance_window_start_time: ``AWS::AmazonMQ::Broker.MaintenanceWindowStartTime``.
        :param security_groups: ``AWS::AmazonMQ::Broker.SecurityGroups``.
        :param storage_type: ``AWS::AmazonMQ::Broker.StorageType``.
        :param subnet_ids: ``AWS::AmazonMQ::Broker.SubnetIds``.
        :param tags: ``AWS::AmazonMQ::Broker.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "auto_minor_version_upgrade": auto_minor_version_upgrade,
            "broker_name": broker_name,
            "deployment_mode": deployment_mode,
            "engine_type": engine_type,
            "engine_version": engine_version,
            "host_instance_type": host_instance_type,
            "publicly_accessible": publicly_accessible,
            "users": users,
        }
        if authentication_strategy is not None:
            self._values["authentication_strategy"] = authentication_strategy
        if configuration is not None:
            self._values["configuration"] = configuration
        if encryption_options is not None:
            self._values["encryption_options"] = encryption_options
        if ldap_server_metadata is not None:
            self._values["ldap_server_metadata"] = ldap_server_metadata
        if logs is not None:
            self._values["logs"] = logs
        if maintenance_window_start_time is not None:
            self._values["maintenance_window_start_time"] = maintenance_window_start_time
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        """``AWS::AmazonMQ::Broker.AutoMinorVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-autominorversionupgrade
        """
        result = self._values.get("auto_minor_version_upgrade")
        assert result is not None, "Required property 'auto_minor_version_upgrade' is missing"
        return result

    @builtins.property
    def broker_name(self) -> builtins.str:
        """``AWS::AmazonMQ::Broker.BrokerName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-brokername
        """
        result = self._values.get("broker_name")
        assert result is not None, "Required property 'broker_name' is missing"
        return result

    @builtins.property
    def deployment_mode(self) -> builtins.str:
        """``AWS::AmazonMQ::Broker.DeploymentMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-deploymentmode
        """
        result = self._values.get("deployment_mode")
        assert result is not None, "Required property 'deployment_mode' is missing"
        return result

    @builtins.property
    def engine_type(self) -> builtins.str:
        """``AWS::AmazonMQ::Broker.EngineType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-enginetype
        """
        result = self._values.get("engine_type")
        assert result is not None, "Required property 'engine_type' is missing"
        return result

    @builtins.property
    def engine_version(self) -> builtins.str:
        """``AWS::AmazonMQ::Broker.EngineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-engineversion
        """
        result = self._values.get("engine_version")
        assert result is not None, "Required property 'engine_version' is missing"
        return result

    @builtins.property
    def host_instance_type(self) -> builtins.str:
        """``AWS::AmazonMQ::Broker.HostInstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-hostinstancetype
        """
        result = self._values.get("host_instance_type")
        assert result is not None, "Required property 'host_instance_type' is missing"
        return result

    @builtins.property
    def publicly_accessible(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        """``AWS::AmazonMQ::Broker.PubliclyAccessible``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-publiclyaccessible
        """
        result = self._values.get("publicly_accessible")
        assert result is not None, "Required property 'publicly_accessible' is missing"
        return result

    @builtins.property
    def users(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBroker.UserProperty, _IResolvable_a771d0ef]]]:
        """``AWS::AmazonMQ::Broker.Users``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-users
        """
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return result

    @builtins.property
    def authentication_strategy(self) -> typing.Optional[builtins.str]:
        """``AWS::AmazonMQ::Broker.AuthenticationStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-authenticationstrategy
        """
        result = self._values.get("authentication_strategy")
        return result

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBroker.ConfigurationIdProperty, _IResolvable_a771d0ef]]:
        """``AWS::AmazonMQ::Broker.Configuration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-configuration
        """
        result = self._values.get("configuration")
        return result

    @builtins.property
    def encryption_options(
        self,
    ) -> typing.Optional[typing.Union[CfnBroker.EncryptionOptionsProperty, _IResolvable_a771d0ef]]:
        """``AWS::AmazonMQ::Broker.EncryptionOptions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-encryptionoptions
        """
        result = self._values.get("encryption_options")
        return result

    @builtins.property
    def ldap_server_metadata(
        self,
    ) -> typing.Optional[typing.Union[CfnBroker.LdapServerMetadataProperty, _IResolvable_a771d0ef]]:
        """``AWS::AmazonMQ::Broker.LdapServerMetadata``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-ldapservermetadata
        """
        result = self._values.get("ldap_server_metadata")
        return result

    @builtins.property
    def logs(
        self,
    ) -> typing.Optional[typing.Union[CfnBroker.LogListProperty, _IResolvable_a771d0ef]]:
        """``AWS::AmazonMQ::Broker.Logs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-logs
        """
        result = self._values.get("logs")
        return result

    @builtins.property
    def maintenance_window_start_time(
        self,
    ) -> typing.Optional[typing.Union[CfnBroker.MaintenanceWindowProperty, _IResolvable_a771d0ef]]:
        """``AWS::AmazonMQ::Broker.MaintenanceWindowStartTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-maintenancewindowstarttime
        """
        result = self._values.get("maintenance_window_start_time")
        return result

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AmazonMQ::Broker.SecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-securitygroups
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AmazonMQ::Broker.StorageType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-storagetype
        """
        result = self._values.get("storage_type")
        return result

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AmazonMQ::Broker.SubnetIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-subnetids
        """
        result = self._values.get("subnet_ids")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnBroker.TagsEntryProperty]]:
        """``AWS::AmazonMQ::Broker.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBrokerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnConfiguration(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amazonmq.CfnConfiguration",
):
    """A CloudFormation ``AWS::AmazonMQ::Configuration``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html
    :cloudformationResource: AWS::AmazonMQ::Configuration
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        data: builtins.str,
        engine_type: builtins.str,
        engine_version: builtins.str,
        name: builtins.str,
        authentication_strategy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List["CfnConfiguration.TagsEntryProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::AmazonMQ::Configuration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data: ``AWS::AmazonMQ::Configuration.Data``.
        :param engine_type: ``AWS::AmazonMQ::Configuration.EngineType``.
        :param engine_version: ``AWS::AmazonMQ::Configuration.EngineVersion``.
        :param name: ``AWS::AmazonMQ::Configuration.Name``.
        :param authentication_strategy: ``AWS::AmazonMQ::Configuration.AuthenticationStrategy``.
        :param description: ``AWS::AmazonMQ::Configuration.Description``.
        :param tags: ``AWS::AmazonMQ::Configuration.Tags``.
        """
        props = CfnConfigurationProps(
            data=data,
            engine_type=engine_type,
            engine_version=engine_version,
            name=name,
            authentication_strategy=authentication_strategy,
            description=description,
            tags=tags,
        )

        jsii.create(CfnConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        """
        :cloudformationAttribute: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrRevision")
    def attr_revision(self) -> jsii.Number:
        """
        :cloudformationAttribute: Revision
        """
        return jsii.get(self, "attrRevision")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::AmazonMQ::Configuration.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        """``AWS::AmazonMQ::Configuration.Data``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-data
        """
        return jsii.get(self, "data")

    @data.setter # type: ignore
    def data(self, value: builtins.str) -> None:
        jsii.set(self, "data", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> builtins.str:
        """``AWS::AmazonMQ::Configuration.EngineType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-enginetype
        """
        return jsii.get(self, "engineType")

    @engine_type.setter # type: ignore
    def engine_type(self, value: builtins.str) -> None:
        jsii.set(self, "engineType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> builtins.str:
        """``AWS::AmazonMQ::Configuration.EngineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter # type: ignore
    def engine_version(self, value: builtins.str) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::AmazonMQ::Configuration.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authenticationStrategy")
    def authentication_strategy(self) -> typing.Optional[builtins.str]:
        """``AWS::AmazonMQ::Configuration.AuthenticationStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-authenticationstrategy
        """
        return jsii.get(self, "authenticationStrategy")

    @authentication_strategy.setter # type: ignore
    def authentication_strategy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "authenticationStrategy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::AmazonMQ::Configuration.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_amazonmq.CfnConfiguration.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            """
            :param key: ``CfnConfiguration.TagsEntryProperty.Key``.
            :param value: ``CfnConfiguration.TagsEntryProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnConfiguration.TagsEntryProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html#cfn-amazonmq-configuration-tagsentry-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnConfiguration.TagsEntryProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html#cfn-amazonmq-configuration-tagsentry-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnConfigurationAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amazonmq.CfnConfigurationAssociation",
):
    """A CloudFormation ``AWS::AmazonMQ::ConfigurationAssociation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html
    :cloudformationResource: AWS::AmazonMQ::ConfigurationAssociation
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        broker: builtins.str,
        configuration: typing.Union["CfnConfigurationAssociation.ConfigurationIdProperty", _IResolvable_a771d0ef],
    ) -> None:
        """Create a new ``AWS::AmazonMQ::ConfigurationAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param broker: ``AWS::AmazonMQ::ConfigurationAssociation.Broker``.
        :param configuration: ``AWS::AmazonMQ::ConfigurationAssociation.Configuration``.
        """
        props = CfnConfigurationAssociationProps(
            broker=broker, configuration=configuration
        )

        jsii.create(CfnConfigurationAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="broker")
    def broker(self) -> builtins.str:
        """``AWS::AmazonMQ::ConfigurationAssociation.Broker``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-broker
        """
        return jsii.get(self, "broker")

    @broker.setter # type: ignore
    def broker(self, value: builtins.str) -> None:
        jsii.set(self, "broker", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Union["CfnConfigurationAssociation.ConfigurationIdProperty", _IResolvable_a771d0ef]:
        """``AWS::AmazonMQ::ConfigurationAssociation.Configuration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-configuration
        """
        return jsii.get(self, "configuration")

    @configuration.setter # type: ignore
    def configuration(
        self,
        value: typing.Union["CfnConfigurationAssociation.ConfigurationIdProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "configuration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_amazonmq.CfnConfigurationAssociation.ConfigurationIdProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "revision": "revision"},
    )
    class ConfigurationIdProperty:
        def __init__(self, *, id: builtins.str, revision: jsii.Number) -> None:
            """
            :param id: ``CfnConfigurationAssociation.ConfigurationIdProperty.Id``.
            :param revision: ``CfnConfigurationAssociation.ConfigurationIdProperty.Revision``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
                "revision": revision,
            }

        @builtins.property
        def id(self) -> builtins.str:
            """``CfnConfigurationAssociation.ConfigurationIdProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html#cfn-amazonmq-configurationassociation-configurationid-id
            """
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return result

        @builtins.property
        def revision(self) -> jsii.Number:
            """``CfnConfigurationAssociation.ConfigurationIdProperty.Revision``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html#cfn-amazonmq-configurationassociation-configurationid-revision
            """
            result = self._values.get("revision")
            assert result is not None, "Required property 'revision' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_amazonmq.CfnConfigurationAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"broker": "broker", "configuration": "configuration"},
)
class CfnConfigurationAssociationProps:
    def __init__(
        self,
        *,
        broker: builtins.str,
        configuration: typing.Union[CfnConfigurationAssociation.ConfigurationIdProperty, _IResolvable_a771d0ef],
    ) -> None:
        """Properties for defining a ``AWS::AmazonMQ::ConfigurationAssociation``.

        :param broker: ``AWS::AmazonMQ::ConfigurationAssociation.Broker``.
        :param configuration: ``AWS::AmazonMQ::ConfigurationAssociation.Configuration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "broker": broker,
            "configuration": configuration,
        }

    @builtins.property
    def broker(self) -> builtins.str:
        """``AWS::AmazonMQ::ConfigurationAssociation.Broker``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-broker
        """
        result = self._values.get("broker")
        assert result is not None, "Required property 'broker' is missing"
        return result

    @builtins.property
    def configuration(
        self,
    ) -> typing.Union[CfnConfigurationAssociation.ConfigurationIdProperty, _IResolvable_a771d0ef]:
        """``AWS::AmazonMQ::ConfigurationAssociation.Configuration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-configuration
        """
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amazonmq.CfnConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "data": "data",
        "engine_type": "engineType",
        "engine_version": "engineVersion",
        "name": "name",
        "authentication_strategy": "authenticationStrategy",
        "description": "description",
        "tags": "tags",
    },
)
class CfnConfigurationProps:
    def __init__(
        self,
        *,
        data: builtins.str,
        engine_type: builtins.str,
        engine_version: builtins.str,
        name: builtins.str,
        authentication_strategy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[CfnConfiguration.TagsEntryProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::AmazonMQ::Configuration``.

        :param data: ``AWS::AmazonMQ::Configuration.Data``.
        :param engine_type: ``AWS::AmazonMQ::Configuration.EngineType``.
        :param engine_version: ``AWS::AmazonMQ::Configuration.EngineVersion``.
        :param name: ``AWS::AmazonMQ::Configuration.Name``.
        :param authentication_strategy: ``AWS::AmazonMQ::Configuration.AuthenticationStrategy``.
        :param description: ``AWS::AmazonMQ::Configuration.Description``.
        :param tags: ``AWS::AmazonMQ::Configuration.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "data": data,
            "engine_type": engine_type,
            "engine_version": engine_version,
            "name": name,
        }
        if authentication_strategy is not None:
            self._values["authentication_strategy"] = authentication_strategy
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data(self) -> builtins.str:
        """``AWS::AmazonMQ::Configuration.Data``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-data
        """
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return result

    @builtins.property
    def engine_type(self) -> builtins.str:
        """``AWS::AmazonMQ::Configuration.EngineType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-enginetype
        """
        result = self._values.get("engine_type")
        assert result is not None, "Required property 'engine_type' is missing"
        return result

    @builtins.property
    def engine_version(self) -> builtins.str:
        """``AWS::AmazonMQ::Configuration.EngineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-engineversion
        """
        result = self._values.get("engine_version")
        assert result is not None, "Required property 'engine_version' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::AmazonMQ::Configuration.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def authentication_strategy(self) -> typing.Optional[builtins.str]:
        """``AWS::AmazonMQ::Configuration.AuthenticationStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-authenticationstrategy
        """
        result = self._values.get("authentication_strategy")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::AmazonMQ::Configuration.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnConfiguration.TagsEntryProperty]]:
        """``AWS::AmazonMQ::Configuration.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnBroker",
    "CfnBrokerProps",
    "CfnConfiguration",
    "CfnConfigurationAssociation",
    "CfnConfigurationAssociationProps",
    "CfnConfigurationProps",
]

publication.publish()
