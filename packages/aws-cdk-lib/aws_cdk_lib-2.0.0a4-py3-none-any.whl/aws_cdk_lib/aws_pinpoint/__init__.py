import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import constructs
from .. import (
    CfnResource as _CfnResource_f7d91f4b,
    IInspectable as _IInspectable_3eb0224c,
    IResolvable as _IResolvable_6e2f5d88,
    TagManager as _TagManager_6a5badd9,
    TreeInspector as _TreeInspector_afbbf916,
)


@jsii.implements(_IInspectable_3eb0224c)
class CfnADMChannel(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnADMChannel",
):
    """A CloudFormation ``AWS::Pinpoint::ADMChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html
    :cloudformationResource: AWS::Pinpoint::ADMChannel
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::ADMChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::ADMChannel.ApplicationId``.
        :param client_id: ``AWS::Pinpoint::ADMChannel.ClientId``.
        :param client_secret: ``AWS::Pinpoint::ADMChannel.ClientSecret``.
        :param enabled: ``AWS::Pinpoint::ADMChannel.Enabled``.
        """
        props = CfnADMChannelProps(
            application_id=application_id,
            client_id=client_id,
            client_secret=client_secret,
            enabled=enabled,
        )

        jsii.create(CfnADMChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::ADMChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        """``AWS::Pinpoint::ADMChannel.ClientId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientid
        """
        return jsii.get(self, "clientId")

    @client_id.setter # type: ignore
    def client_id(self, value: builtins.str) -> None:
        jsii.set(self, "clientId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        """``AWS::Pinpoint::ADMChannel.ClientSecret``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientsecret
        """
        return jsii.get(self, "clientSecret")

    @client_secret.setter # type: ignore
    def client_secret(self, value: builtins.str) -> None:
        jsii.set(self, "clientSecret", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::ADMChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnADMChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "enabled": "enabled",
    },
)
class CfnADMChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        client_id: builtins.str,
        client_secret: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::ADMChannel``.

        :param application_id: ``AWS::Pinpoint::ADMChannel.ApplicationId``.
        :param client_id: ``AWS::Pinpoint::ADMChannel.ClientId``.
        :param client_secret: ``AWS::Pinpoint::ADMChannel.ClientSecret``.
        :param enabled: ``AWS::Pinpoint::ADMChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::ADMChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def client_id(self) -> builtins.str:
        """``AWS::Pinpoint::ADMChannel.ClientId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientid
        """
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return result

    @builtins.property
    def client_secret(self) -> builtins.str:
        """``AWS::Pinpoint::ADMChannel.ClientSecret``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-clientsecret
        """
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::ADMChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-admchannel.html#cfn-pinpoint-admchannel-enabled
        """
        result = self._values.get("enabled")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnADMChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnAPNSChannel(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnAPNSChannel",
):
    """A CloudFormation ``AWS::Pinpoint::APNSChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html
    :cloudformationResource: AWS::Pinpoint::APNSChannel
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::APNSChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::APNSChannel.ApplicationId``.
        :param bundle_id: ``AWS::Pinpoint::APNSChannel.BundleId``.
        :param certificate: ``AWS::Pinpoint::APNSChannel.Certificate``.
        :param default_authentication_method: ``AWS::Pinpoint::APNSChannel.DefaultAuthenticationMethod``.
        :param enabled: ``AWS::Pinpoint::APNSChannel.Enabled``.
        :param private_key: ``AWS::Pinpoint::APNSChannel.PrivateKey``.
        :param team_id: ``AWS::Pinpoint::APNSChannel.TeamId``.
        :param token_key: ``AWS::Pinpoint::APNSChannel.TokenKey``.
        :param token_key_id: ``AWS::Pinpoint::APNSChannel.TokenKeyId``.
        """
        props = CfnAPNSChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(CfnAPNSChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::APNSChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.BundleId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-bundleid
        """
        return jsii.get(self, "bundleId")

    @bundle_id.setter # type: ignore
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "bundleId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-certificate
        """
        return jsii.get(self, "certificate")

    @certificate.setter # type: ignore
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.DefaultAuthenticationMethod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-defaultauthenticationmethod
        """
        return jsii.get(self, "defaultAuthenticationMethod")

    @default_authentication_method.setter # type: ignore
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::APNSChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.PrivateKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-privatekey
        """
        return jsii.get(self, "privateKey")

    @private_key.setter # type: ignore
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "privateKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.TeamId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-teamid
        """
        return jsii.get(self, "teamId")

    @team_id.setter # type: ignore
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.TokenKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkey
        """
        return jsii.get(self, "tokenKey")

    @token_key.setter # type: ignore
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tokenKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkeyid
        """
        return jsii.get(self, "tokenKeyId")

    @token_key_id.setter # type: ignore
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnAPNSChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::APNSChannel``.

        :param application_id: ``AWS::Pinpoint::APNSChannel.ApplicationId``.
        :param bundle_id: ``AWS::Pinpoint::APNSChannel.BundleId``.
        :param certificate: ``AWS::Pinpoint::APNSChannel.Certificate``.
        :param default_authentication_method: ``AWS::Pinpoint::APNSChannel.DefaultAuthenticationMethod``.
        :param enabled: ``AWS::Pinpoint::APNSChannel.Enabled``.
        :param private_key: ``AWS::Pinpoint::APNSChannel.PrivateKey``.
        :param team_id: ``AWS::Pinpoint::APNSChannel.TeamId``.
        :param token_key: ``AWS::Pinpoint::APNSChannel.TokenKey``.
        :param token_key_id: ``AWS::Pinpoint::APNSChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::APNSChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.BundleId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-bundleid
        """
        result = self._values.get("bundle_id")
        return result

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-certificate
        """
        result = self._values.get("certificate")
        return result

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.DefaultAuthenticationMethod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-defaultauthenticationmethod
        """
        result = self._values.get("default_authentication_method")
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::APNSChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-enabled
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.PrivateKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-privatekey
        """
        result = self._values.get("private_key")
        return result

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.TeamId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-teamid
        """
        result = self._values.get("team_id")
        return result

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.TokenKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkey
        """
        result = self._values.get("token_key")
        return result

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnschannel.html#cfn-pinpoint-apnschannel-tokenkeyid
        """
        result = self._values.get("token_key_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnAPNSSandboxChannel(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnAPNSSandboxChannel",
):
    """A CloudFormation ``AWS::Pinpoint::APNSSandboxChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html
    :cloudformationResource: AWS::Pinpoint::APNSSandboxChannel
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::APNSSandboxChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::APNSSandboxChannel.ApplicationId``.
        :param bundle_id: ``AWS::Pinpoint::APNSSandboxChannel.BundleId``.
        :param certificate: ``AWS::Pinpoint::APNSSandboxChannel.Certificate``.
        :param default_authentication_method: ``AWS::Pinpoint::APNSSandboxChannel.DefaultAuthenticationMethod``.
        :param enabled: ``AWS::Pinpoint::APNSSandboxChannel.Enabled``.
        :param private_key: ``AWS::Pinpoint::APNSSandboxChannel.PrivateKey``.
        :param team_id: ``AWS::Pinpoint::APNSSandboxChannel.TeamId``.
        :param token_key: ``AWS::Pinpoint::APNSSandboxChannel.TokenKey``.
        :param token_key_id: ``AWS::Pinpoint::APNSSandboxChannel.TokenKeyId``.
        """
        props = CfnAPNSSandboxChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(CfnAPNSSandboxChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::APNSSandboxChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.BundleId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-bundleid
        """
        return jsii.get(self, "bundleId")

    @bundle_id.setter # type: ignore
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "bundleId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-certificate
        """
        return jsii.get(self, "certificate")

    @certificate.setter # type: ignore
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.DefaultAuthenticationMethod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-defaultauthenticationmethod
        """
        return jsii.get(self, "defaultAuthenticationMethod")

    @default_authentication_method.setter # type: ignore
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::APNSSandboxChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.PrivateKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-privatekey
        """
        return jsii.get(self, "privateKey")

    @private_key.setter # type: ignore
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "privateKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.TeamId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-teamid
        """
        return jsii.get(self, "teamId")

    @team_id.setter # type: ignore
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.TokenKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkey
        """
        return jsii.get(self, "tokenKey")

    @token_key.setter # type: ignore
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tokenKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkeyid
        """
        return jsii.get(self, "tokenKeyId")

    @token_key_id.setter # type: ignore
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnAPNSSandboxChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSSandboxChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::APNSSandboxChannel``.

        :param application_id: ``AWS::Pinpoint::APNSSandboxChannel.ApplicationId``.
        :param bundle_id: ``AWS::Pinpoint::APNSSandboxChannel.BundleId``.
        :param certificate: ``AWS::Pinpoint::APNSSandboxChannel.Certificate``.
        :param default_authentication_method: ``AWS::Pinpoint::APNSSandboxChannel.DefaultAuthenticationMethod``.
        :param enabled: ``AWS::Pinpoint::APNSSandboxChannel.Enabled``.
        :param private_key: ``AWS::Pinpoint::APNSSandboxChannel.PrivateKey``.
        :param team_id: ``AWS::Pinpoint::APNSSandboxChannel.TeamId``.
        :param token_key: ``AWS::Pinpoint::APNSSandboxChannel.TokenKey``.
        :param token_key_id: ``AWS::Pinpoint::APNSSandboxChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::APNSSandboxChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.BundleId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-bundleid
        """
        result = self._values.get("bundle_id")
        return result

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-certificate
        """
        result = self._values.get("certificate")
        return result

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.DefaultAuthenticationMethod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-defaultauthenticationmethod
        """
        result = self._values.get("default_authentication_method")
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::APNSSandboxChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-enabled
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.PrivateKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-privatekey
        """
        result = self._values.get("private_key")
        return result

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.TeamId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-teamid
        """
        result = self._values.get("team_id")
        return result

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.TokenKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkey
        """
        result = self._values.get("token_key")
        return result

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSSandboxChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnssandboxchannel.html#cfn-pinpoint-apnssandboxchannel-tokenkeyid
        """
        result = self._values.get("token_key_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSSandboxChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnAPNSVoipChannel(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnAPNSVoipChannel",
):
    """A CloudFormation ``AWS::Pinpoint::APNSVoipChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html
    :cloudformationResource: AWS::Pinpoint::APNSVoipChannel
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::APNSVoipChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::APNSVoipChannel.ApplicationId``.
        :param bundle_id: ``AWS::Pinpoint::APNSVoipChannel.BundleId``.
        :param certificate: ``AWS::Pinpoint::APNSVoipChannel.Certificate``.
        :param default_authentication_method: ``AWS::Pinpoint::APNSVoipChannel.DefaultAuthenticationMethod``.
        :param enabled: ``AWS::Pinpoint::APNSVoipChannel.Enabled``.
        :param private_key: ``AWS::Pinpoint::APNSVoipChannel.PrivateKey``.
        :param team_id: ``AWS::Pinpoint::APNSVoipChannel.TeamId``.
        :param token_key: ``AWS::Pinpoint::APNSVoipChannel.TokenKey``.
        :param token_key_id: ``AWS::Pinpoint::APNSVoipChannel.TokenKeyId``.
        """
        props = CfnAPNSVoipChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(CfnAPNSVoipChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::APNSVoipChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.BundleId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-bundleid
        """
        return jsii.get(self, "bundleId")

    @bundle_id.setter # type: ignore
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "bundleId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-certificate
        """
        return jsii.get(self, "certificate")

    @certificate.setter # type: ignore
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.DefaultAuthenticationMethod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-defaultauthenticationmethod
        """
        return jsii.get(self, "defaultAuthenticationMethod")

    @default_authentication_method.setter # type: ignore
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::APNSVoipChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.PrivateKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-privatekey
        """
        return jsii.get(self, "privateKey")

    @private_key.setter # type: ignore
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "privateKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.TeamId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-teamid
        """
        return jsii.get(self, "teamId")

    @team_id.setter # type: ignore
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.TokenKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkey
        """
        return jsii.get(self, "tokenKey")

    @token_key.setter # type: ignore
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tokenKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkeyid
        """
        return jsii.get(self, "tokenKeyId")

    @token_key_id.setter # type: ignore
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnAPNSVoipChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSVoipChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::APNSVoipChannel``.

        :param application_id: ``AWS::Pinpoint::APNSVoipChannel.ApplicationId``.
        :param bundle_id: ``AWS::Pinpoint::APNSVoipChannel.BundleId``.
        :param certificate: ``AWS::Pinpoint::APNSVoipChannel.Certificate``.
        :param default_authentication_method: ``AWS::Pinpoint::APNSVoipChannel.DefaultAuthenticationMethod``.
        :param enabled: ``AWS::Pinpoint::APNSVoipChannel.Enabled``.
        :param private_key: ``AWS::Pinpoint::APNSVoipChannel.PrivateKey``.
        :param team_id: ``AWS::Pinpoint::APNSVoipChannel.TeamId``.
        :param token_key: ``AWS::Pinpoint::APNSVoipChannel.TokenKey``.
        :param token_key_id: ``AWS::Pinpoint::APNSVoipChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::APNSVoipChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.BundleId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-bundleid
        """
        result = self._values.get("bundle_id")
        return result

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-certificate
        """
        result = self._values.get("certificate")
        return result

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.DefaultAuthenticationMethod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-defaultauthenticationmethod
        """
        result = self._values.get("default_authentication_method")
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::APNSVoipChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-enabled
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.PrivateKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-privatekey
        """
        result = self._values.get("private_key")
        return result

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.TeamId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-teamid
        """
        result = self._values.get("team_id")
        return result

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.TokenKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkey
        """
        result = self._values.get("token_key")
        return result

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipchannel.html#cfn-pinpoint-apnsvoipchannel-tokenkeyid
        """
        result = self._values.get("token_key_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSVoipChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnAPNSVoipSandboxChannel(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnAPNSVoipSandboxChannel",
):
    """A CloudFormation ``AWS::Pinpoint::APNSVoipSandboxChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html
    :cloudformationResource: AWS::Pinpoint::APNSVoipSandboxChannel
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::APNSVoipSandboxChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::APNSVoipSandboxChannel.ApplicationId``.
        :param bundle_id: ``AWS::Pinpoint::APNSVoipSandboxChannel.BundleId``.
        :param certificate: ``AWS::Pinpoint::APNSVoipSandboxChannel.Certificate``.
        :param default_authentication_method: ``AWS::Pinpoint::APNSVoipSandboxChannel.DefaultAuthenticationMethod``.
        :param enabled: ``AWS::Pinpoint::APNSVoipSandboxChannel.Enabled``.
        :param private_key: ``AWS::Pinpoint::APNSVoipSandboxChannel.PrivateKey``.
        :param team_id: ``AWS::Pinpoint::APNSVoipSandboxChannel.TeamId``.
        :param token_key: ``AWS::Pinpoint::APNSVoipSandboxChannel.TokenKey``.
        :param token_key_id: ``AWS::Pinpoint::APNSVoipSandboxChannel.TokenKeyId``.
        """
        props = CfnAPNSVoipSandboxChannelProps(
            application_id=application_id,
            bundle_id=bundle_id,
            certificate=certificate,
            default_authentication_method=default_authentication_method,
            enabled=enabled,
            private_key=private_key,
            team_id=team_id,
            token_key=token_key,
            token_key_id=token_key_id,
        )

        jsii.create(CfnAPNSVoipSandboxChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.BundleId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-bundleid
        """
        return jsii.get(self, "bundleId")

    @bundle_id.setter # type: ignore
    def bundle_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "bundleId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-certificate
        """
        return jsii.get(self, "certificate")

    @certificate.setter # type: ignore
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultAuthenticationMethod")
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.DefaultAuthenticationMethod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-defaultauthenticationmethod
        """
        return jsii.get(self, "defaultAuthenticationMethod")

    @default_authentication_method.setter # type: ignore
    def default_authentication_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "defaultAuthenticationMethod", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.PrivateKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-privatekey
        """
        return jsii.get(self, "privateKey")

    @private_key.setter # type: ignore
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "privateKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.TeamId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-teamid
        """
        return jsii.get(self, "teamId")

    @team_id.setter # type: ignore
    def team_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tokenKey")
    def token_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.TokenKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkey
        """
        return jsii.get(self, "tokenKey")

    @token_key.setter # type: ignore
    def token_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tokenKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tokenKeyId")
    def token_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkeyid
        """
        return jsii.get(self, "tokenKeyId")

    @token_key_id.setter # type: ignore
    def token_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tokenKeyId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnAPNSVoipSandboxChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "bundle_id": "bundleId",
        "certificate": "certificate",
        "default_authentication_method": "defaultAuthenticationMethod",
        "enabled": "enabled",
        "private_key": "privateKey",
        "team_id": "teamId",
        "token_key": "tokenKey",
        "token_key_id": "tokenKeyId",
    },
)
class CfnAPNSVoipSandboxChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        bundle_id: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        default_authentication_method: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        private_key: typing.Optional[builtins.str] = None,
        team_id: typing.Optional[builtins.str] = None,
        token_key: typing.Optional[builtins.str] = None,
        token_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::APNSVoipSandboxChannel``.

        :param application_id: ``AWS::Pinpoint::APNSVoipSandboxChannel.ApplicationId``.
        :param bundle_id: ``AWS::Pinpoint::APNSVoipSandboxChannel.BundleId``.
        :param certificate: ``AWS::Pinpoint::APNSVoipSandboxChannel.Certificate``.
        :param default_authentication_method: ``AWS::Pinpoint::APNSVoipSandboxChannel.DefaultAuthenticationMethod``.
        :param enabled: ``AWS::Pinpoint::APNSVoipSandboxChannel.Enabled``.
        :param private_key: ``AWS::Pinpoint::APNSVoipSandboxChannel.PrivateKey``.
        :param team_id: ``AWS::Pinpoint::APNSVoipSandboxChannel.TeamId``.
        :param token_key: ``AWS::Pinpoint::APNSVoipSandboxChannel.TokenKey``.
        :param token_key_id: ``AWS::Pinpoint::APNSVoipSandboxChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
        }
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if certificate is not None:
            self._values["certificate"] = certificate
        if default_authentication_method is not None:
            self._values["default_authentication_method"] = default_authentication_method
        if enabled is not None:
            self._values["enabled"] = enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if team_id is not None:
            self._values["team_id"] = team_id
        if token_key is not None:
            self._values["token_key"] = token_key
        if token_key_id is not None:
            self._values["token_key_id"] = token_key_id

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.BundleId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-bundleid
        """
        result = self._values.get("bundle_id")
        return result

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-certificate
        """
        result = self._values.get("certificate")
        return result

    @builtins.property
    def default_authentication_method(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.DefaultAuthenticationMethod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-defaultauthenticationmethod
        """
        result = self._values.get("default_authentication_method")
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-enabled
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.PrivateKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-privatekey
        """
        result = self._values.get("private_key")
        return result

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.TeamId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-teamid
        """
        result = self._values.get("team_id")
        return result

    @builtins.property
    def token_key(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.TokenKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkey
        """
        result = self._values.get("token_key")
        return result

    @builtins.property
    def token_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::APNSVoipSandboxChannel.TokenKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-apnsvoipsandboxchannel.html#cfn-pinpoint-apnsvoipsandboxchannel-tokenkeyid
        """
        result = self._values.get("token_key_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPNSVoipSandboxChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnApp(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnApp",
):
    """A CloudFormation ``AWS::Pinpoint::App``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html
    :cloudformationResource: AWS::Pinpoint::App
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        tags: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::App``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::Pinpoint::App.Name``.
        :param tags: ``AWS::Pinpoint::App.Tags``.
        """
        props = CfnAppProps(name=name, tags=tags)

        jsii.create(CfnApp, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::Pinpoint::App.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::Pinpoint::App.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnAppProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags"},
)
class CfnAppProps:
    def __init__(self, *, name: builtins.str, tags: typing.Any = None) -> None:
        """Properties for defining a ``AWS::Pinpoint::App``.

        :param name: ``AWS::Pinpoint::App.Name``.
        :param tags: ``AWS::Pinpoint::App.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::Pinpoint::App.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::Pinpoint::App.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-app.html#cfn-pinpoint-app-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnApplicationSettings(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnApplicationSettings",
):
    """A CloudFormation ``AWS::Pinpoint::ApplicationSettings``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html
    :cloudformationResource: AWS::Pinpoint::ApplicationSettings
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        campaign_hook: typing.Optional[typing.Union["CfnApplicationSettings.CampaignHookProperty", _IResolvable_6e2f5d88]] = None,
        cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        limits: typing.Optional[typing.Union["CfnApplicationSettings.LimitsProperty", _IResolvable_6e2f5d88]] = None,
        quiet_time: typing.Optional[typing.Union["CfnApplicationSettings.QuietTimeProperty", _IResolvable_6e2f5d88]] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::ApplicationSettings``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::ApplicationSettings.ApplicationId``.
        :param campaign_hook: ``AWS::Pinpoint::ApplicationSettings.CampaignHook``.
        :param cloud_watch_metrics_enabled: ``AWS::Pinpoint::ApplicationSettings.CloudWatchMetricsEnabled``.
        :param limits: ``AWS::Pinpoint::ApplicationSettings.Limits``.
        :param quiet_time: ``AWS::Pinpoint::ApplicationSettings.QuietTime``.
        """
        props = CfnApplicationSettingsProps(
            application_id=application_id,
            campaign_hook=campaign_hook,
            cloud_watch_metrics_enabled=cloud_watch_metrics_enabled,
            limits=limits,
            quiet_time=quiet_time,
        )

        jsii.create(CfnApplicationSettings, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::ApplicationSettings.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="campaignHook")
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union["CfnApplicationSettings.CampaignHookProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::ApplicationSettings.CampaignHook``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-campaignhook
        """
        return jsii.get(self, "campaignHook")

    @campaign_hook.setter # type: ignore
    def campaign_hook(
        self,
        value: typing.Optional[typing.Union["CfnApplicationSettings.CampaignHookProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "campaignHook", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cloudWatchMetricsEnabled")
    def cloud_watch_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::ApplicationSettings.CloudWatchMetricsEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-cloudwatchmetricsenabled
        """
        return jsii.get(self, "cloudWatchMetricsEnabled")

    @cloud_watch_metrics_enabled.setter # type: ignore
    def cloud_watch_metrics_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "cloudWatchMetricsEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> typing.Optional[typing.Union["CfnApplicationSettings.LimitsProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::ApplicationSettings.Limits``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-limits
        """
        return jsii.get(self, "limits")

    @limits.setter # type: ignore
    def limits(
        self,
        value: typing.Optional[typing.Union["CfnApplicationSettings.LimitsProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "limits", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="quietTime")
    def quiet_time(
        self,
    ) -> typing.Optional[typing.Union["CfnApplicationSettings.QuietTimeProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::ApplicationSettings.QuietTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-quiettime
        """
        return jsii.get(self, "quietTime")

    @quiet_time.setter # type: ignore
    def quiet_time(
        self,
        value: typing.Optional[typing.Union["CfnApplicationSettings.QuietTimeProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "quietTime", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnApplicationSettings.CampaignHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_function_name": "lambdaFunctionName",
            "mode": "mode",
            "web_url": "webUrl",
        },
    )
    class CampaignHookProperty:
        def __init__(
            self,
            *,
            lambda_function_name: typing.Optional[builtins.str] = None,
            mode: typing.Optional[builtins.str] = None,
            web_url: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param lambda_function_name: ``CfnApplicationSettings.CampaignHookProperty.LambdaFunctionName``.
            :param mode: ``CfnApplicationSettings.CampaignHookProperty.Mode``.
            :param web_url: ``CfnApplicationSettings.CampaignHookProperty.WebUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if lambda_function_name is not None:
                self._values["lambda_function_name"] = lambda_function_name
            if mode is not None:
                self._values["mode"] = mode
            if web_url is not None:
                self._values["web_url"] = web_url

        @builtins.property
        def lambda_function_name(self) -> typing.Optional[builtins.str]:
            """``CfnApplicationSettings.CampaignHookProperty.LambdaFunctionName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-lambdafunctionname
            """
            result = self._values.get("lambda_function_name")
            return result

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            """``CfnApplicationSettings.CampaignHookProperty.Mode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-mode
            """
            result = self._values.get("mode")
            return result

        @builtins.property
        def web_url(self) -> typing.Optional[builtins.str]:
            """``CfnApplicationSettings.CampaignHookProperty.WebUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-campaignhook.html#cfn-pinpoint-applicationsettings-campaignhook-weburl
            """
            result = self._values.get("web_url")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnApplicationSettings.LimitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "daily": "daily",
            "maximum_duration": "maximumDuration",
            "messages_per_second": "messagesPerSecond",
            "total": "total",
        },
    )
    class LimitsProperty:
        def __init__(
            self,
            *,
            daily: typing.Optional[jsii.Number] = None,
            maximum_duration: typing.Optional[jsii.Number] = None,
            messages_per_second: typing.Optional[jsii.Number] = None,
            total: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param daily: ``CfnApplicationSettings.LimitsProperty.Daily``.
            :param maximum_duration: ``CfnApplicationSettings.LimitsProperty.MaximumDuration``.
            :param messages_per_second: ``CfnApplicationSettings.LimitsProperty.MessagesPerSecond``.
            :param total: ``CfnApplicationSettings.LimitsProperty.Total``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if daily is not None:
                self._values["daily"] = daily
            if maximum_duration is not None:
                self._values["maximum_duration"] = maximum_duration
            if messages_per_second is not None:
                self._values["messages_per_second"] = messages_per_second
            if total is not None:
                self._values["total"] = total

        @builtins.property
        def daily(self) -> typing.Optional[jsii.Number]:
            """``CfnApplicationSettings.LimitsProperty.Daily``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-daily
            """
            result = self._values.get("daily")
            return result

        @builtins.property
        def maximum_duration(self) -> typing.Optional[jsii.Number]:
            """``CfnApplicationSettings.LimitsProperty.MaximumDuration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-maximumduration
            """
            result = self._values.get("maximum_duration")
            return result

        @builtins.property
        def messages_per_second(self) -> typing.Optional[jsii.Number]:
            """``CfnApplicationSettings.LimitsProperty.MessagesPerSecond``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-messagespersecond
            """
            result = self._values.get("messages_per_second")
            return result

        @builtins.property
        def total(self) -> typing.Optional[jsii.Number]:
            """``CfnApplicationSettings.LimitsProperty.Total``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-limits.html#cfn-pinpoint-applicationsettings-limits-total
            """
            result = self._values.get("total")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnApplicationSettings.QuietTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class QuietTimeProperty:
        def __init__(self, *, end: builtins.str, start: builtins.str) -> None:
            """
            :param end: ``CfnApplicationSettings.QuietTimeProperty.End``.
            :param start: ``CfnApplicationSettings.QuietTimeProperty.Start``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "end": end,
                "start": start,
            }

        @builtins.property
        def end(self) -> builtins.str:
            """``CfnApplicationSettings.QuietTimeProperty.End``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html#cfn-pinpoint-applicationsettings-quiettime-end
            """
            result = self._values.get("end")
            assert result is not None, "Required property 'end' is missing"
            return result

        @builtins.property
        def start(self) -> builtins.str:
            """``CfnApplicationSettings.QuietTimeProperty.Start``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-applicationsettings-quiettime.html#cfn-pinpoint-applicationsettings-quiettime-start
            """
            result = self._values.get("start")
            assert result is not None, "Required property 'start' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuietTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnApplicationSettingsProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "campaign_hook": "campaignHook",
        "cloud_watch_metrics_enabled": "cloudWatchMetricsEnabled",
        "limits": "limits",
        "quiet_time": "quietTime",
    },
)
class CfnApplicationSettingsProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        campaign_hook: typing.Optional[typing.Union[CfnApplicationSettings.CampaignHookProperty, _IResolvable_6e2f5d88]] = None,
        cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        limits: typing.Optional[typing.Union[CfnApplicationSettings.LimitsProperty, _IResolvable_6e2f5d88]] = None,
        quiet_time: typing.Optional[typing.Union[CfnApplicationSettings.QuietTimeProperty, _IResolvable_6e2f5d88]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::ApplicationSettings``.

        :param application_id: ``AWS::Pinpoint::ApplicationSettings.ApplicationId``.
        :param campaign_hook: ``AWS::Pinpoint::ApplicationSettings.CampaignHook``.
        :param cloud_watch_metrics_enabled: ``AWS::Pinpoint::ApplicationSettings.CloudWatchMetricsEnabled``.
        :param limits: ``AWS::Pinpoint::ApplicationSettings.Limits``.
        :param quiet_time: ``AWS::Pinpoint::ApplicationSettings.QuietTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
        }
        if campaign_hook is not None:
            self._values["campaign_hook"] = campaign_hook
        if cloud_watch_metrics_enabled is not None:
            self._values["cloud_watch_metrics_enabled"] = cloud_watch_metrics_enabled
        if limits is not None:
            self._values["limits"] = limits
        if quiet_time is not None:
            self._values["quiet_time"] = quiet_time

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::ApplicationSettings.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union[CfnApplicationSettings.CampaignHookProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::ApplicationSettings.CampaignHook``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-campaignhook
        """
        result = self._values.get("campaign_hook")
        return result

    @builtins.property
    def cloud_watch_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::ApplicationSettings.CloudWatchMetricsEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-cloudwatchmetricsenabled
        """
        result = self._values.get("cloud_watch_metrics_enabled")
        return result

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional[typing.Union[CfnApplicationSettings.LimitsProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::ApplicationSettings.Limits``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-limits
        """
        result = self._values.get("limits")
        return result

    @builtins.property
    def quiet_time(
        self,
    ) -> typing.Optional[typing.Union[CfnApplicationSettings.QuietTimeProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::ApplicationSettings.QuietTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-applicationsettings.html#cfn-pinpoint-applicationsettings-quiettime
        """
        result = self._values.get("quiet_time")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationSettingsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnBaiduChannel(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnBaiduChannel",
):
    """A CloudFormation ``AWS::Pinpoint::BaiduChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html
    :cloudformationResource: AWS::Pinpoint::BaiduChannel
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        secret_key: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::BaiduChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key: ``AWS::Pinpoint::BaiduChannel.ApiKey``.
        :param application_id: ``AWS::Pinpoint::BaiduChannel.ApplicationId``.
        :param secret_key: ``AWS::Pinpoint::BaiduChannel.SecretKey``.
        :param enabled: ``AWS::Pinpoint::BaiduChannel.Enabled``.
        """
        props = CfnBaiduChannelProps(
            api_key=api_key,
            application_id=application_id,
            secret_key=secret_key,
            enabled=enabled,
        )

        jsii.create(CfnBaiduChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        """``AWS::Pinpoint::BaiduChannel.ApiKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-apikey
        """
        return jsii.get(self, "apiKey")

    @api_key.setter # type: ignore
    def api_key(self, value: builtins.str) -> None:
        jsii.set(self, "apiKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::BaiduChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> builtins.str:
        """``AWS::Pinpoint::BaiduChannel.SecretKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-secretkey
        """
        return jsii.get(self, "secretKey")

    @secret_key.setter # type: ignore
    def secret_key(self, value: builtins.str) -> None:
        jsii.set(self, "secretKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::BaiduChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnBaiduChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "application_id": "applicationId",
        "secret_key": "secretKey",
        "enabled": "enabled",
    },
)
class CfnBaiduChannelProps:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        secret_key: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::BaiduChannel``.

        :param api_key: ``AWS::Pinpoint::BaiduChannel.ApiKey``.
        :param application_id: ``AWS::Pinpoint::BaiduChannel.ApplicationId``.
        :param secret_key: ``AWS::Pinpoint::BaiduChannel.SecretKey``.
        :param enabled: ``AWS::Pinpoint::BaiduChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_key": api_key,
            "application_id": application_id,
            "secret_key": secret_key,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def api_key(self) -> builtins.str:
        """``AWS::Pinpoint::BaiduChannel.ApiKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-apikey
        """
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return result

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::BaiduChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def secret_key(self) -> builtins.str:
        """``AWS::Pinpoint::BaiduChannel.SecretKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-secretkey
        """
        result = self._values.get("secret_key")
        assert result is not None, "Required property 'secret_key' is missing"
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::BaiduChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-baiduchannel.html#cfn-pinpoint-baiduchannel-enabled
        """
        result = self._values.get("enabled")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBaiduChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnCampaign(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign",
):
    """A CloudFormation ``AWS::Pinpoint::Campaign``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html
    :cloudformationResource: AWS::Pinpoint::Campaign
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        message_configuration: typing.Union["CfnCampaign.MessageConfigurationProperty", _IResolvable_6e2f5d88],
        name: builtins.str,
        schedule: typing.Union["CfnCampaign.ScheduleProperty", _IResolvable_6e2f5d88],
        segment_id: builtins.str,
        additional_treatments: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnCampaign.WriteTreatmentResourceProperty", _IResolvable_6e2f5d88]]]] = None,
        campaign_hook: typing.Optional[typing.Union["CfnCampaign.CampaignHookProperty", _IResolvable_6e2f5d88]] = None,
        description: typing.Optional[builtins.str] = None,
        holdout_percent: typing.Optional[jsii.Number] = None,
        is_paused: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        limits: typing.Optional[typing.Union["CfnCampaign.LimitsProperty", _IResolvable_6e2f5d88]] = None,
        segment_version: typing.Optional[jsii.Number] = None,
        tags: typing.Any = None,
        treatment_description: typing.Optional[builtins.str] = None,
        treatment_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::Campaign``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::Campaign.ApplicationId``.
        :param message_configuration: ``AWS::Pinpoint::Campaign.MessageConfiguration``.
        :param name: ``AWS::Pinpoint::Campaign.Name``.
        :param schedule: ``AWS::Pinpoint::Campaign.Schedule``.
        :param segment_id: ``AWS::Pinpoint::Campaign.SegmentId``.
        :param additional_treatments: ``AWS::Pinpoint::Campaign.AdditionalTreatments``.
        :param campaign_hook: ``AWS::Pinpoint::Campaign.CampaignHook``.
        :param description: ``AWS::Pinpoint::Campaign.Description``.
        :param holdout_percent: ``AWS::Pinpoint::Campaign.HoldoutPercent``.
        :param is_paused: ``AWS::Pinpoint::Campaign.IsPaused``.
        :param limits: ``AWS::Pinpoint::Campaign.Limits``.
        :param segment_version: ``AWS::Pinpoint::Campaign.SegmentVersion``.
        :param tags: ``AWS::Pinpoint::Campaign.Tags``.
        :param treatment_description: ``AWS::Pinpoint::Campaign.TreatmentDescription``.
        :param treatment_name: ``AWS::Pinpoint::Campaign.TreatmentName``.
        """
        props = CfnCampaignProps(
            application_id=application_id,
            message_configuration=message_configuration,
            name=name,
            schedule=schedule,
            segment_id=segment_id,
            additional_treatments=additional_treatments,
            campaign_hook=campaign_hook,
            description=description,
            holdout_percent=holdout_percent,
            is_paused=is_paused,
            limits=limits,
            segment_version=segment_version,
            tags=tags,
            treatment_description=treatment_description,
            treatment_name=treatment_name,
        )

        jsii.create(CfnCampaign, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="attrCampaignId")
    def attr_campaign_id(self) -> builtins.str:
        """
        :cloudformationAttribute: CampaignId
        """
        return jsii.get(self, "attrCampaignId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::Pinpoint::Campaign.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::Campaign.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="messageConfiguration")
    def message_configuration(
        self,
    ) -> typing.Union["CfnCampaign.MessageConfigurationProperty", _IResolvable_6e2f5d88]:
        """``AWS::Pinpoint::Campaign.MessageConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-messageconfiguration
        """
        return jsii.get(self, "messageConfiguration")

    @message_configuration.setter # type: ignore
    def message_configuration(
        self,
        value: typing.Union["CfnCampaign.MessageConfigurationProperty", _IResolvable_6e2f5d88],
    ) -> None:
        jsii.set(self, "messageConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::Pinpoint::Campaign.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> typing.Union["CfnCampaign.ScheduleProperty", _IResolvable_6e2f5d88]:
        """``AWS::Pinpoint::Campaign.Schedule``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-schedule
        """
        return jsii.get(self, "schedule")

    @schedule.setter # type: ignore
    def schedule(
        self,
        value: typing.Union["CfnCampaign.ScheduleProperty", _IResolvable_6e2f5d88],
    ) -> None:
        jsii.set(self, "schedule", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="segmentId")
    def segment_id(self) -> builtins.str:
        """``AWS::Pinpoint::Campaign.SegmentId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentid
        """
        return jsii.get(self, "segmentId")

    @segment_id.setter # type: ignore
    def segment_id(self, value: builtins.str) -> None:
        jsii.set(self, "segmentId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="additionalTreatments")
    def additional_treatments(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnCampaign.WriteTreatmentResourceProperty", _IResolvable_6e2f5d88]]]]:
        """``AWS::Pinpoint::Campaign.AdditionalTreatments``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-additionaltreatments
        """
        return jsii.get(self, "additionalTreatments")

    @additional_treatments.setter # type: ignore
    def additional_treatments(
        self,
        value: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnCampaign.WriteTreatmentResourceProperty", _IResolvable_6e2f5d88]]]],
    ) -> None:
        jsii.set(self, "additionalTreatments", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="campaignHook")
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union["CfnCampaign.CampaignHookProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::Campaign.CampaignHook``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-campaignhook
        """
        return jsii.get(self, "campaignHook")

    @campaign_hook.setter # type: ignore
    def campaign_hook(
        self,
        value: typing.Optional[typing.Union["CfnCampaign.CampaignHookProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "campaignHook", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::Campaign.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="holdoutPercent")
    def holdout_percent(self) -> typing.Optional[jsii.Number]:
        """``AWS::Pinpoint::Campaign.HoldoutPercent``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-holdoutpercent
        """
        return jsii.get(self, "holdoutPercent")

    @holdout_percent.setter # type: ignore
    def holdout_percent(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "holdoutPercent", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="isPaused")
    def is_paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::Campaign.IsPaused``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-ispaused
        """
        return jsii.get(self, "isPaused")

    @is_paused.setter # type: ignore
    def is_paused(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "isPaused", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="limits")
    def limits(
        self,
    ) -> typing.Optional[typing.Union["CfnCampaign.LimitsProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::Campaign.Limits``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-limits
        """
        return jsii.get(self, "limits")

    @limits.setter # type: ignore
    def limits(
        self,
        value: typing.Optional[typing.Union["CfnCampaign.LimitsProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "limits", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="segmentVersion")
    def segment_version(self) -> typing.Optional[jsii.Number]:
        """``AWS::Pinpoint::Campaign.SegmentVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentversion
        """
        return jsii.get(self, "segmentVersion")

    @segment_version.setter # type: ignore
    def segment_version(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "segmentVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="treatmentDescription")
    def treatment_description(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::Campaign.TreatmentDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentdescription
        """
        return jsii.get(self, "treatmentDescription")

    @treatment_description.setter # type: ignore
    def treatment_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "treatmentDescription", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="treatmentName")
    def treatment_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::Campaign.TreatmentName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentname
        """
        return jsii.get(self, "treatmentName")

    @treatment_name.setter # type: ignore
    def treatment_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "treatmentName", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.AttributeDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_type": "attributeType", "values": "values"},
    )
    class AttributeDimensionProperty:
        def __init__(
            self,
            *,
            attribute_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param attribute_type: ``CfnCampaign.AttributeDimensionProperty.AttributeType``.
            :param values: ``CfnCampaign.AttributeDimensionProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-attributedimension.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if attribute_type is not None:
                self._values["attribute_type"] = attribute_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def attribute_type(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.AttributeDimensionProperty.AttributeType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-attributedimension.html#cfn-pinpoint-campaign-attributedimension-attributetype
            """
            result = self._values.get("attribute_type")
            return result

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnCampaign.AttributeDimensionProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-attributedimension.html#cfn-pinpoint-campaign-attributedimension-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.CampaignEmailMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "body": "body",
            "from_address": "fromAddress",
            "html_body": "htmlBody",
            "title": "title",
        },
    )
    class CampaignEmailMessageProperty:
        def __init__(
            self,
            *,
            body: typing.Optional[builtins.str] = None,
            from_address: typing.Optional[builtins.str] = None,
            html_body: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param body: ``CfnCampaign.CampaignEmailMessageProperty.Body``.
            :param from_address: ``CfnCampaign.CampaignEmailMessageProperty.FromAddress``.
            :param html_body: ``CfnCampaign.CampaignEmailMessageProperty.HtmlBody``.
            :param title: ``CfnCampaign.CampaignEmailMessageProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body
            if from_address is not None:
                self._values["from_address"] = from_address
            if html_body is not None:
                self._values["html_body"] = html_body
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignEmailMessageProperty.Body``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-body
            """
            result = self._values.get("body")
            return result

        @builtins.property
        def from_address(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignEmailMessageProperty.FromAddress``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-fromaddress
            """
            result = self._values.get("from_address")
            return result

        @builtins.property
        def html_body(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignEmailMessageProperty.HtmlBody``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-htmlbody
            """
            result = self._values.get("html_body")
            return result

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignEmailMessageProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignemailmessage.html#cfn-pinpoint-campaign-campaignemailmessage-title
            """
            result = self._values.get("title")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignEmailMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.CampaignEventFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions", "filter_type": "filterType"},
    )
    class CampaignEventFilterProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union["CfnCampaign.EventDimensionsProperty", _IResolvable_6e2f5d88]] = None,
            filter_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param dimensions: ``CfnCampaign.CampaignEventFilterProperty.Dimensions``.
            :param filter_type: ``CfnCampaign.CampaignEventFilterProperty.FilterType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if filter_type is not None:
                self._values["filter_type"] = filter_type

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.EventDimensionsProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.CampaignEventFilterProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html#cfn-pinpoint-campaign-campaigneventfilter-dimensions
            """
            result = self._values.get("dimensions")
            return result

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignEventFilterProperty.FilterType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaigneventfilter.html#cfn-pinpoint-campaign-campaigneventfilter-filtertype
            """
            result = self._values.get("filter_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignEventFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.CampaignHookProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_function_name": "lambdaFunctionName",
            "mode": "mode",
            "web_url": "webUrl",
        },
    )
    class CampaignHookProperty:
        def __init__(
            self,
            *,
            lambda_function_name: typing.Optional[builtins.str] = None,
            mode: typing.Optional[builtins.str] = None,
            web_url: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param lambda_function_name: ``CfnCampaign.CampaignHookProperty.LambdaFunctionName``.
            :param mode: ``CfnCampaign.CampaignHookProperty.Mode``.
            :param web_url: ``CfnCampaign.CampaignHookProperty.WebUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if lambda_function_name is not None:
                self._values["lambda_function_name"] = lambda_function_name
            if mode is not None:
                self._values["mode"] = mode
            if web_url is not None:
                self._values["web_url"] = web_url

        @builtins.property
        def lambda_function_name(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignHookProperty.LambdaFunctionName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-lambdafunctionname
            """
            result = self._values.get("lambda_function_name")
            return result

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignHookProperty.Mode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-mode
            """
            result = self._values.get("mode")
            return result

        @builtins.property
        def web_url(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignHookProperty.WebUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignhook.html#cfn-pinpoint-campaign-campaignhook-weburl
            """
            result = self._values.get("web_url")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignHookProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.CampaignSmsMessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "body": "body",
            "message_type": "messageType",
            "sender_id": "senderId",
        },
    )
    class CampaignSmsMessageProperty:
        def __init__(
            self,
            *,
            body: typing.Optional[builtins.str] = None,
            message_type: typing.Optional[builtins.str] = None,
            sender_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param body: ``CfnCampaign.CampaignSmsMessageProperty.Body``.
            :param message_type: ``CfnCampaign.CampaignSmsMessageProperty.MessageType``.
            :param sender_id: ``CfnCampaign.CampaignSmsMessageProperty.SenderId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body
            if message_type is not None:
                self._values["message_type"] = message_type
            if sender_id is not None:
                self._values["sender_id"] = sender_id

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignSmsMessageProperty.Body``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-body
            """
            result = self._values.get("body")
            return result

        @builtins.property
        def message_type(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignSmsMessageProperty.MessageType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-messagetype
            """
            result = self._values.get("message_type")
            return result

        @builtins.property
        def sender_id(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.CampaignSmsMessageProperty.SenderId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-campaignsmsmessage.html#cfn-pinpoint-campaign-campaignsmsmessage-senderid
            """
            result = self._values.get("sender_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CampaignSmsMessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.EventDimensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "event_type": "eventType",
            "metrics": "metrics",
        },
    )
    class EventDimensionsProperty:
        def __init__(
            self,
            *,
            attributes: typing.Any = None,
            event_type: typing.Optional[typing.Union["CfnCampaign.SetDimensionProperty", _IResolvable_6e2f5d88]] = None,
            metrics: typing.Any = None,
        ) -> None:
            """
            :param attributes: ``CfnCampaign.EventDimensionsProperty.Attributes``.
            :param event_type: ``CfnCampaign.EventDimensionsProperty.EventType``.
            :param metrics: ``CfnCampaign.EventDimensionsProperty.Metrics``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if event_type is not None:
                self._values["event_type"] = event_type
            if metrics is not None:
                self._values["metrics"] = metrics

        @builtins.property
        def attributes(self) -> typing.Any:
            """``CfnCampaign.EventDimensionsProperty.Attributes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-attributes
            """
            result = self._values.get("attributes")
            return result

        @builtins.property
        def event_type(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.SetDimensionProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.EventDimensionsProperty.EventType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-eventtype
            """
            result = self._values.get("event_type")
            return result

        @builtins.property
        def metrics(self) -> typing.Any:
            """``CfnCampaign.EventDimensionsProperty.Metrics``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-eventdimensions.html#cfn-pinpoint-campaign-eventdimensions-metrics
            """
            result = self._values.get("metrics")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventDimensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.LimitsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "daily": "daily",
            "maximum_duration": "maximumDuration",
            "messages_per_second": "messagesPerSecond",
            "total": "total",
        },
    )
    class LimitsProperty:
        def __init__(
            self,
            *,
            daily: typing.Optional[jsii.Number] = None,
            maximum_duration: typing.Optional[jsii.Number] = None,
            messages_per_second: typing.Optional[jsii.Number] = None,
            total: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param daily: ``CfnCampaign.LimitsProperty.Daily``.
            :param maximum_duration: ``CfnCampaign.LimitsProperty.MaximumDuration``.
            :param messages_per_second: ``CfnCampaign.LimitsProperty.MessagesPerSecond``.
            :param total: ``CfnCampaign.LimitsProperty.Total``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if daily is not None:
                self._values["daily"] = daily
            if maximum_duration is not None:
                self._values["maximum_duration"] = maximum_duration
            if messages_per_second is not None:
                self._values["messages_per_second"] = messages_per_second
            if total is not None:
                self._values["total"] = total

        @builtins.property
        def daily(self) -> typing.Optional[jsii.Number]:
            """``CfnCampaign.LimitsProperty.Daily``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-daily
            """
            result = self._values.get("daily")
            return result

        @builtins.property
        def maximum_duration(self) -> typing.Optional[jsii.Number]:
            """``CfnCampaign.LimitsProperty.MaximumDuration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-maximumduration
            """
            result = self._values.get("maximum_duration")
            return result

        @builtins.property
        def messages_per_second(self) -> typing.Optional[jsii.Number]:
            """``CfnCampaign.LimitsProperty.MessagesPerSecond``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-messagespersecond
            """
            result = self._values.get("messages_per_second")
            return result

        @builtins.property
        def total(self) -> typing.Optional[jsii.Number]:
            """``CfnCampaign.LimitsProperty.Total``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-limits.html#cfn-pinpoint-campaign-limits-total
            """
            result = self._values.get("total")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.MessageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "adm_message": "admMessage",
            "apns_message": "apnsMessage",
            "baidu_message": "baiduMessage",
            "default_message": "defaultMessage",
            "email_message": "emailMessage",
            "gcm_message": "gcmMessage",
            "sms_message": "smsMessage",
        },
    )
    class MessageConfigurationProperty:
        def __init__(
            self,
            *,
            adm_message: typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_6e2f5d88]] = None,
            apns_message: typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_6e2f5d88]] = None,
            baidu_message: typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_6e2f5d88]] = None,
            default_message: typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_6e2f5d88]] = None,
            email_message: typing.Optional[typing.Union["CfnCampaign.CampaignEmailMessageProperty", _IResolvable_6e2f5d88]] = None,
            gcm_message: typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_6e2f5d88]] = None,
            sms_message: typing.Optional[typing.Union["CfnCampaign.CampaignSmsMessageProperty", _IResolvable_6e2f5d88]] = None,
        ) -> None:
            """
            :param adm_message: ``CfnCampaign.MessageConfigurationProperty.ADMMessage``.
            :param apns_message: ``CfnCampaign.MessageConfigurationProperty.APNSMessage``.
            :param baidu_message: ``CfnCampaign.MessageConfigurationProperty.BaiduMessage``.
            :param default_message: ``CfnCampaign.MessageConfigurationProperty.DefaultMessage``.
            :param email_message: ``CfnCampaign.MessageConfigurationProperty.EmailMessage``.
            :param gcm_message: ``CfnCampaign.MessageConfigurationProperty.GCMMessage``.
            :param sms_message: ``CfnCampaign.MessageConfigurationProperty.SMSMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if adm_message is not None:
                self._values["adm_message"] = adm_message
            if apns_message is not None:
                self._values["apns_message"] = apns_message
            if baidu_message is not None:
                self._values["baidu_message"] = baidu_message
            if default_message is not None:
                self._values["default_message"] = default_message
            if email_message is not None:
                self._values["email_message"] = email_message
            if gcm_message is not None:
                self._values["gcm_message"] = gcm_message
            if sms_message is not None:
                self._values["sms_message"] = sms_message

        @builtins.property
        def adm_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.MessageConfigurationProperty.ADMMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-admmessage
            """
            result = self._values.get("adm_message")
            return result

        @builtins.property
        def apns_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.MessageConfigurationProperty.APNSMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-apnsmessage
            """
            result = self._values.get("apns_message")
            return result

        @builtins.property
        def baidu_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.MessageConfigurationProperty.BaiduMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-baidumessage
            """
            result = self._values.get("baidu_message")
            return result

        @builtins.property
        def default_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.MessageConfigurationProperty.DefaultMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-defaultmessage
            """
            result = self._values.get("default_message")
            return result

        @builtins.property
        def email_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.CampaignEmailMessageProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.MessageConfigurationProperty.EmailMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-emailmessage
            """
            result = self._values.get("email_message")
            return result

        @builtins.property
        def gcm_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.MessageConfigurationProperty.GCMMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-gcmmessage
            """
            result = self._values.get("gcm_message")
            return result

        @builtins.property
        def sms_message(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.CampaignSmsMessageProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.MessageConfigurationProperty.SMSMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-messageconfiguration.html#cfn-pinpoint-campaign-messageconfiguration-smsmessage
            """
            result = self._values.get("sms_message")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.MessageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "image_icon_url": "imageIconUrl",
            "image_small_icon_url": "imageSmallIconUrl",
            "image_url": "imageUrl",
            "json_body": "jsonBody",
            "media_url": "mediaUrl",
            "raw_content": "rawContent",
            "silent_push": "silentPush",
            "time_to_live": "timeToLive",
            "title": "title",
            "url": "url",
        },
    )
    class MessageProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            image_icon_url: typing.Optional[builtins.str] = None,
            image_small_icon_url: typing.Optional[builtins.str] = None,
            image_url: typing.Optional[builtins.str] = None,
            json_body: typing.Optional[builtins.str] = None,
            media_url: typing.Optional[builtins.str] = None,
            raw_content: typing.Optional[builtins.str] = None,
            silent_push: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
            time_to_live: typing.Optional[jsii.Number] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param action: ``CfnCampaign.MessageProperty.Action``.
            :param body: ``CfnCampaign.MessageProperty.Body``.
            :param image_icon_url: ``CfnCampaign.MessageProperty.ImageIconUrl``.
            :param image_small_icon_url: ``CfnCampaign.MessageProperty.ImageSmallIconUrl``.
            :param image_url: ``CfnCampaign.MessageProperty.ImageUrl``.
            :param json_body: ``CfnCampaign.MessageProperty.JsonBody``.
            :param media_url: ``CfnCampaign.MessageProperty.MediaUrl``.
            :param raw_content: ``CfnCampaign.MessageProperty.RawContent``.
            :param silent_push: ``CfnCampaign.MessageProperty.SilentPush``.
            :param time_to_live: ``CfnCampaign.MessageProperty.TimeToLive``.
            :param title: ``CfnCampaign.MessageProperty.Title``.
            :param url: ``CfnCampaign.MessageProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if image_icon_url is not None:
                self._values["image_icon_url"] = image_icon_url
            if image_small_icon_url is not None:
                self._values["image_small_icon_url"] = image_small_icon_url
            if image_url is not None:
                self._values["image_url"] = image_url
            if json_body is not None:
                self._values["json_body"] = json_body
            if media_url is not None:
                self._values["media_url"] = media_url
            if raw_content is not None:
                self._values["raw_content"] = raw_content
            if silent_push is not None:
                self._values["silent_push"] = silent_push
            if time_to_live is not None:
                self._values["time_to_live"] = time_to_live
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MessageProperty.Action``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-action
            """
            result = self._values.get("action")
            return result

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MessageProperty.Body``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-body
            """
            result = self._values.get("body")
            return result

        @builtins.property
        def image_icon_url(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MessageProperty.ImageIconUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imageiconurl
            """
            result = self._values.get("image_icon_url")
            return result

        @builtins.property
        def image_small_icon_url(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MessageProperty.ImageSmallIconUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imagesmalliconurl
            """
            result = self._values.get("image_small_icon_url")
            return result

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MessageProperty.ImageUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-imageurl
            """
            result = self._values.get("image_url")
            return result

        @builtins.property
        def json_body(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MessageProperty.JsonBody``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-jsonbody
            """
            result = self._values.get("json_body")
            return result

        @builtins.property
        def media_url(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MessageProperty.MediaUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-mediaurl
            """
            result = self._values.get("media_url")
            return result

        @builtins.property
        def raw_content(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MessageProperty.RawContent``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-rawcontent
            """
            result = self._values.get("raw_content")
            return result

        @builtins.property
        def silent_push(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
            """``CfnCampaign.MessageProperty.SilentPush``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-silentpush
            """
            result = self._values.get("silent_push")
            return result

        @builtins.property
        def time_to_live(self) -> typing.Optional[jsii.Number]:
            """``CfnCampaign.MessageProperty.TimeToLive``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-timetolive
            """
            result = self._values.get("time_to_live")
            return result

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MessageProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-title
            """
            result = self._values.get("title")
            return result

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MessageProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-message.html#cfn-pinpoint-campaign-message-url
            """
            result = self._values.get("url")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.MetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison_operator": "comparisonOperator", "value": "value"},
    )
    class MetricDimensionProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param comparison_operator: ``CfnCampaign.MetricDimensionProperty.ComparisonOperator``.
            :param value: ``CfnCampaign.MetricDimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-metricdimension.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.MetricDimensionProperty.ComparisonOperator``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-metricdimension.html#cfn-pinpoint-campaign-metricdimension-comparisonoperator
            """
            result = self._values.get("comparison_operator")
            return result

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            """``CfnCampaign.MetricDimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-metricdimension.html#cfn-pinpoint-campaign-metricdimension-value
            """
            result = self._values.get("value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.QuietTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"end": "end", "start": "start"},
    )
    class QuietTimeProperty:
        def __init__(self, *, end: builtins.str, start: builtins.str) -> None:
            """
            :param end: ``CfnCampaign.QuietTimeProperty.End``.
            :param start: ``CfnCampaign.QuietTimeProperty.Start``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule-quiettime.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "end": end,
                "start": start,
            }

        @builtins.property
        def end(self) -> builtins.str:
            """``CfnCampaign.QuietTimeProperty.End``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule-quiettime.html#cfn-pinpoint-campaign-schedule-quiettime-end
            """
            result = self._values.get("end")
            assert result is not None, "Required property 'end' is missing"
            return result

        @builtins.property
        def start(self) -> builtins.str:
            """``CfnCampaign.QuietTimeProperty.Start``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule-quiettime.html#cfn-pinpoint-campaign-schedule-quiettime-start
            """
            result = self._values.get("start")
            assert result is not None, "Required property 'start' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuietTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_time": "endTime",
            "event_filter": "eventFilter",
            "frequency": "frequency",
            "is_local_time": "isLocalTime",
            "quiet_time": "quietTime",
            "start_time": "startTime",
            "time_zone": "timeZone",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            end_time: typing.Optional[builtins.str] = None,
            event_filter: typing.Optional[typing.Union["CfnCampaign.CampaignEventFilterProperty", _IResolvable_6e2f5d88]] = None,
            frequency: typing.Optional[builtins.str] = None,
            is_local_time: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
            quiet_time: typing.Optional[typing.Union["CfnCampaign.QuietTimeProperty", _IResolvable_6e2f5d88]] = None,
            start_time: typing.Optional[builtins.str] = None,
            time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param end_time: ``CfnCampaign.ScheduleProperty.EndTime``.
            :param event_filter: ``CfnCampaign.ScheduleProperty.EventFilter``.
            :param frequency: ``CfnCampaign.ScheduleProperty.Frequency``.
            :param is_local_time: ``CfnCampaign.ScheduleProperty.IsLocalTime``.
            :param quiet_time: ``CfnCampaign.ScheduleProperty.QuietTime``.
            :param start_time: ``CfnCampaign.ScheduleProperty.StartTime``.
            :param time_zone: ``CfnCampaign.ScheduleProperty.TimeZone``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if end_time is not None:
                self._values["end_time"] = end_time
            if event_filter is not None:
                self._values["event_filter"] = event_filter
            if frequency is not None:
                self._values["frequency"] = frequency
            if is_local_time is not None:
                self._values["is_local_time"] = is_local_time
            if quiet_time is not None:
                self._values["quiet_time"] = quiet_time
            if start_time is not None:
                self._values["start_time"] = start_time
            if time_zone is not None:
                self._values["time_zone"] = time_zone

        @builtins.property
        def end_time(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.ScheduleProperty.EndTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-endtime
            """
            result = self._values.get("end_time")
            return result

        @builtins.property
        def event_filter(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.CampaignEventFilterProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.ScheduleProperty.EventFilter``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-eventfilter
            """
            result = self._values.get("event_filter")
            return result

        @builtins.property
        def frequency(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.ScheduleProperty.Frequency``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-frequency
            """
            result = self._values.get("frequency")
            return result

        @builtins.property
        def is_local_time(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
            """``CfnCampaign.ScheduleProperty.IsLocalTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-islocaltime
            """
            result = self._values.get("is_local_time")
            return result

        @builtins.property
        def quiet_time(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.QuietTimeProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.ScheduleProperty.QuietTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-quiettime
            """
            result = self._values.get("quiet_time")
            return result

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.ScheduleProperty.StartTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-starttime
            """
            result = self._values.get("start_time")
            return result

        @builtins.property
        def time_zone(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.ScheduleProperty.TimeZone``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-schedule.html#cfn-pinpoint-campaign-schedule-timezone
            """
            result = self._values.get("time_zone")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.SetDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class SetDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param dimension_type: ``CfnCampaign.SetDimensionProperty.DimensionType``.
            :param values: ``CfnCampaign.SetDimensionProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.SetDimensionProperty.DimensionType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html#cfn-pinpoint-campaign-setdimension-dimensiontype
            """
            result = self._values.get("dimension_type")
            return result

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnCampaign.SetDimensionProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-setdimension.html#cfn-pinpoint-campaign-setdimension-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaign.WriteTreatmentResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "message_configuration": "messageConfiguration",
            "schedule": "schedule",
            "size_percent": "sizePercent",
            "treatment_description": "treatmentDescription",
            "treatment_name": "treatmentName",
        },
    )
    class WriteTreatmentResourceProperty:
        def __init__(
            self,
            *,
            message_configuration: typing.Optional[typing.Union["CfnCampaign.MessageConfigurationProperty", _IResolvable_6e2f5d88]] = None,
            schedule: typing.Optional[typing.Union["CfnCampaign.ScheduleProperty", _IResolvable_6e2f5d88]] = None,
            size_percent: typing.Optional[jsii.Number] = None,
            treatment_description: typing.Optional[builtins.str] = None,
            treatment_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param message_configuration: ``CfnCampaign.WriteTreatmentResourceProperty.MessageConfiguration``.
            :param schedule: ``CfnCampaign.WriteTreatmentResourceProperty.Schedule``.
            :param size_percent: ``CfnCampaign.WriteTreatmentResourceProperty.SizePercent``.
            :param treatment_description: ``CfnCampaign.WriteTreatmentResourceProperty.TreatmentDescription``.
            :param treatment_name: ``CfnCampaign.WriteTreatmentResourceProperty.TreatmentName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if message_configuration is not None:
                self._values["message_configuration"] = message_configuration
            if schedule is not None:
                self._values["schedule"] = schedule
            if size_percent is not None:
                self._values["size_percent"] = size_percent
            if treatment_description is not None:
                self._values["treatment_description"] = treatment_description
            if treatment_name is not None:
                self._values["treatment_name"] = treatment_name

        @builtins.property
        def message_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.MessageConfigurationProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.WriteTreatmentResourceProperty.MessageConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-messageconfiguration
            """
            result = self._values.get("message_configuration")
            return result

        @builtins.property
        def schedule(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.ScheduleProperty", _IResolvable_6e2f5d88]]:
            """``CfnCampaign.WriteTreatmentResourceProperty.Schedule``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-schedule
            """
            result = self._values.get("schedule")
            return result

        @builtins.property
        def size_percent(self) -> typing.Optional[jsii.Number]:
            """``CfnCampaign.WriteTreatmentResourceProperty.SizePercent``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-sizepercent
            """
            result = self._values.get("size_percent")
            return result

        @builtins.property
        def treatment_description(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.WriteTreatmentResourceProperty.TreatmentDescription``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-treatmentdescription
            """
            result = self._values.get("treatment_description")
            return result

        @builtins.property
        def treatment_name(self) -> typing.Optional[builtins.str]:
            """``CfnCampaign.WriteTreatmentResourceProperty.TreatmentName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-campaign-writetreatmentresource.html#cfn-pinpoint-campaign-writetreatmentresource-treatmentname
            """
            result = self._values.get("treatment_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WriteTreatmentResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnCampaignProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "message_configuration": "messageConfiguration",
        "name": "name",
        "schedule": "schedule",
        "segment_id": "segmentId",
        "additional_treatments": "additionalTreatments",
        "campaign_hook": "campaignHook",
        "description": "description",
        "holdout_percent": "holdoutPercent",
        "is_paused": "isPaused",
        "limits": "limits",
        "segment_version": "segmentVersion",
        "tags": "tags",
        "treatment_description": "treatmentDescription",
        "treatment_name": "treatmentName",
    },
)
class CfnCampaignProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        message_configuration: typing.Union[CfnCampaign.MessageConfigurationProperty, _IResolvable_6e2f5d88],
        name: builtins.str,
        schedule: typing.Union[CfnCampaign.ScheduleProperty, _IResolvable_6e2f5d88],
        segment_id: builtins.str,
        additional_treatments: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union[CfnCampaign.WriteTreatmentResourceProperty, _IResolvable_6e2f5d88]]]] = None,
        campaign_hook: typing.Optional[typing.Union[CfnCampaign.CampaignHookProperty, _IResolvable_6e2f5d88]] = None,
        description: typing.Optional[builtins.str] = None,
        holdout_percent: typing.Optional[jsii.Number] = None,
        is_paused: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        limits: typing.Optional[typing.Union[CfnCampaign.LimitsProperty, _IResolvable_6e2f5d88]] = None,
        segment_version: typing.Optional[jsii.Number] = None,
        tags: typing.Any = None,
        treatment_description: typing.Optional[builtins.str] = None,
        treatment_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::Campaign``.

        :param application_id: ``AWS::Pinpoint::Campaign.ApplicationId``.
        :param message_configuration: ``AWS::Pinpoint::Campaign.MessageConfiguration``.
        :param name: ``AWS::Pinpoint::Campaign.Name``.
        :param schedule: ``AWS::Pinpoint::Campaign.Schedule``.
        :param segment_id: ``AWS::Pinpoint::Campaign.SegmentId``.
        :param additional_treatments: ``AWS::Pinpoint::Campaign.AdditionalTreatments``.
        :param campaign_hook: ``AWS::Pinpoint::Campaign.CampaignHook``.
        :param description: ``AWS::Pinpoint::Campaign.Description``.
        :param holdout_percent: ``AWS::Pinpoint::Campaign.HoldoutPercent``.
        :param is_paused: ``AWS::Pinpoint::Campaign.IsPaused``.
        :param limits: ``AWS::Pinpoint::Campaign.Limits``.
        :param segment_version: ``AWS::Pinpoint::Campaign.SegmentVersion``.
        :param tags: ``AWS::Pinpoint::Campaign.Tags``.
        :param treatment_description: ``AWS::Pinpoint::Campaign.TreatmentDescription``.
        :param treatment_name: ``AWS::Pinpoint::Campaign.TreatmentName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
            "message_configuration": message_configuration,
            "name": name,
            "schedule": schedule,
            "segment_id": segment_id,
        }
        if additional_treatments is not None:
            self._values["additional_treatments"] = additional_treatments
        if campaign_hook is not None:
            self._values["campaign_hook"] = campaign_hook
        if description is not None:
            self._values["description"] = description
        if holdout_percent is not None:
            self._values["holdout_percent"] = holdout_percent
        if is_paused is not None:
            self._values["is_paused"] = is_paused
        if limits is not None:
            self._values["limits"] = limits
        if segment_version is not None:
            self._values["segment_version"] = segment_version
        if tags is not None:
            self._values["tags"] = tags
        if treatment_description is not None:
            self._values["treatment_description"] = treatment_description
        if treatment_name is not None:
            self._values["treatment_name"] = treatment_name

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::Campaign.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def message_configuration(
        self,
    ) -> typing.Union[CfnCampaign.MessageConfigurationProperty, _IResolvable_6e2f5d88]:
        """``AWS::Pinpoint::Campaign.MessageConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-messageconfiguration
        """
        result = self._values.get("message_configuration")
        assert result is not None, "Required property 'message_configuration' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::Pinpoint::Campaign.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def schedule(
        self,
    ) -> typing.Union[CfnCampaign.ScheduleProperty, _IResolvable_6e2f5d88]:
        """``AWS::Pinpoint::Campaign.Schedule``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-schedule
        """
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return result

    @builtins.property
    def segment_id(self) -> builtins.str:
        """``AWS::Pinpoint::Campaign.SegmentId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentid
        """
        result = self._values.get("segment_id")
        assert result is not None, "Required property 'segment_id' is missing"
        return result

    @builtins.property
    def additional_treatments(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union[CfnCampaign.WriteTreatmentResourceProperty, _IResolvable_6e2f5d88]]]]:
        """``AWS::Pinpoint::Campaign.AdditionalTreatments``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-additionaltreatments
        """
        result = self._values.get("additional_treatments")
        return result

    @builtins.property
    def campaign_hook(
        self,
    ) -> typing.Optional[typing.Union[CfnCampaign.CampaignHookProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::Campaign.CampaignHook``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-campaignhook
        """
        result = self._values.get("campaign_hook")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::Campaign.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def holdout_percent(self) -> typing.Optional[jsii.Number]:
        """``AWS::Pinpoint::Campaign.HoldoutPercent``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-holdoutpercent
        """
        result = self._values.get("holdout_percent")
        return result

    @builtins.property
    def is_paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::Campaign.IsPaused``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-ispaused
        """
        result = self._values.get("is_paused")
        return result

    @builtins.property
    def limits(
        self,
    ) -> typing.Optional[typing.Union[CfnCampaign.LimitsProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::Campaign.Limits``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-limits
        """
        result = self._values.get("limits")
        return result

    @builtins.property
    def segment_version(self) -> typing.Optional[jsii.Number]:
        """``AWS::Pinpoint::Campaign.SegmentVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-segmentversion
        """
        result = self._values.get("segment_version")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::Pinpoint::Campaign.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def treatment_description(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::Campaign.TreatmentDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentdescription
        """
        result = self._values.get("treatment_description")
        return result

    @builtins.property
    def treatment_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::Campaign.TreatmentName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-campaign.html#cfn-pinpoint-campaign-treatmentname
        """
        result = self._values.get("treatment_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCampaignProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnEmailChannel(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnEmailChannel",
):
    """A CloudFormation ``AWS::Pinpoint::EmailChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html
    :cloudformationResource: AWS::Pinpoint::EmailChannel
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        from_address: builtins.str,
        identity: builtins.str,
        configuration_set: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::EmailChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::EmailChannel.ApplicationId``.
        :param from_address: ``AWS::Pinpoint::EmailChannel.FromAddress``.
        :param identity: ``AWS::Pinpoint::EmailChannel.Identity``.
        :param configuration_set: ``AWS::Pinpoint::EmailChannel.ConfigurationSet``.
        :param enabled: ``AWS::Pinpoint::EmailChannel.Enabled``.
        :param role_arn: ``AWS::Pinpoint::EmailChannel.RoleArn``.
        """
        props = CfnEmailChannelProps(
            application_id=application_id,
            from_address=from_address,
            identity=identity,
            configuration_set=configuration_set,
            enabled=enabled,
            role_arn=role_arn,
        )

        jsii.create(CfnEmailChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::EmailChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fromAddress")
    def from_address(self) -> builtins.str:
        """``AWS::Pinpoint::EmailChannel.FromAddress``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-fromaddress
        """
        return jsii.get(self, "fromAddress")

    @from_address.setter # type: ignore
    def from_address(self, value: builtins.str) -> None:
        jsii.set(self, "fromAddress", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        """``AWS::Pinpoint::EmailChannel.Identity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-identity
        """
        return jsii.get(self, "identity")

    @identity.setter # type: ignore
    def identity(self, value: builtins.str) -> None:
        jsii.set(self, "identity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="configurationSet")
    def configuration_set(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailChannel.ConfigurationSet``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-configurationset
        """
        return jsii.get(self, "configurationSet")

    @configuration_set.setter # type: ignore
    def configuration_set(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "configurationSet", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::EmailChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailChannel.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnEmailChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "from_address": "fromAddress",
        "identity": "identity",
        "configuration_set": "configurationSet",
        "enabled": "enabled",
        "role_arn": "roleArn",
    },
)
class CfnEmailChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        from_address: builtins.str,
        identity: builtins.str,
        configuration_set: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::EmailChannel``.

        :param application_id: ``AWS::Pinpoint::EmailChannel.ApplicationId``.
        :param from_address: ``AWS::Pinpoint::EmailChannel.FromAddress``.
        :param identity: ``AWS::Pinpoint::EmailChannel.Identity``.
        :param configuration_set: ``AWS::Pinpoint::EmailChannel.ConfigurationSet``.
        :param enabled: ``AWS::Pinpoint::EmailChannel.Enabled``.
        :param role_arn: ``AWS::Pinpoint::EmailChannel.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
            "from_address": from_address,
            "identity": identity,
        }
        if configuration_set is not None:
            self._values["configuration_set"] = configuration_set
        if enabled is not None:
            self._values["enabled"] = enabled
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::EmailChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def from_address(self) -> builtins.str:
        """``AWS::Pinpoint::EmailChannel.FromAddress``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-fromaddress
        """
        result = self._values.get("from_address")
        assert result is not None, "Required property 'from_address' is missing"
        return result

    @builtins.property
    def identity(self) -> builtins.str:
        """``AWS::Pinpoint::EmailChannel.Identity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-identity
        """
        result = self._values.get("identity")
        assert result is not None, "Required property 'identity' is missing"
        return result

    @builtins.property
    def configuration_set(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailChannel.ConfigurationSet``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-configurationset
        """
        result = self._values.get("configuration_set")
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::EmailChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-enabled
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailChannel.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailchannel.html#cfn-pinpoint-emailchannel-rolearn
        """
        result = self._values.get("role_arn")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnEmailTemplate(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnEmailTemplate",
):
    """A CloudFormation ``AWS::Pinpoint::EmailTemplate``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html
    :cloudformationResource: AWS::Pinpoint::EmailTemplate
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        subject: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        html_part: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
        text_part: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::EmailTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param subject: ``AWS::Pinpoint::EmailTemplate.Subject``.
        :param template_name: ``AWS::Pinpoint::EmailTemplate.TemplateName``.
        :param default_substitutions: ``AWS::Pinpoint::EmailTemplate.DefaultSubstitutions``.
        :param html_part: ``AWS::Pinpoint::EmailTemplate.HtmlPart``.
        :param tags: ``AWS::Pinpoint::EmailTemplate.Tags``.
        :param template_description: ``AWS::Pinpoint::EmailTemplate.TemplateDescription``.
        :param text_part: ``AWS::Pinpoint::EmailTemplate.TextPart``.
        """
        props = CfnEmailTemplateProps(
            subject=subject,
            template_name=template_name,
            default_substitutions=default_substitutions,
            html_part=html_part,
            tags=tags,
            template_description=template_description,
            text_part=text_part,
        )

        jsii.create(CfnEmailTemplate, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::Pinpoint::EmailTemplate.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        """``AWS::Pinpoint::EmailTemplate.Subject``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-subject
        """
        return jsii.get(self, "subject")

    @subject.setter # type: ignore
    def subject(self, value: builtins.str) -> None:
        jsii.set(self, "subject", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        """``AWS::Pinpoint::EmailTemplate.TemplateName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatename
        """
        return jsii.get(self, "templateName")

    @template_name.setter # type: ignore
    def template_name(self, value: builtins.str) -> None:
        jsii.set(self, "templateName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultSubstitutions")
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailTemplate.DefaultSubstitutions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-defaultsubstitutions
        """
        return jsii.get(self, "defaultSubstitutions")

    @default_substitutions.setter # type: ignore
    def default_substitutions(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultSubstitutions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="htmlPart")
    def html_part(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailTemplate.HtmlPart``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-htmlpart
        """
        return jsii.get(self, "htmlPart")

    @html_part.setter # type: ignore
    def html_part(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "htmlPart", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailTemplate.TemplateDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatedescription
        """
        return jsii.get(self, "templateDescription")

    @template_description.setter # type: ignore
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "templateDescription", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="textPart")
    def text_part(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailTemplate.TextPart``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-textpart
        """
        return jsii.get(self, "textPart")

    @text_part.setter # type: ignore
    def text_part(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "textPart", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnEmailTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "subject": "subject",
        "template_name": "templateName",
        "default_substitutions": "defaultSubstitutions",
        "html_part": "htmlPart",
        "tags": "tags",
        "template_description": "templateDescription",
        "text_part": "textPart",
    },
)
class CfnEmailTemplateProps:
    def __init__(
        self,
        *,
        subject: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        html_part: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
        text_part: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::EmailTemplate``.

        :param subject: ``AWS::Pinpoint::EmailTemplate.Subject``.
        :param template_name: ``AWS::Pinpoint::EmailTemplate.TemplateName``.
        :param default_substitutions: ``AWS::Pinpoint::EmailTemplate.DefaultSubstitutions``.
        :param html_part: ``AWS::Pinpoint::EmailTemplate.HtmlPart``.
        :param tags: ``AWS::Pinpoint::EmailTemplate.Tags``.
        :param template_description: ``AWS::Pinpoint::EmailTemplate.TemplateDescription``.
        :param text_part: ``AWS::Pinpoint::EmailTemplate.TextPart``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "subject": subject,
            "template_name": template_name,
        }
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if html_part is not None:
            self._values["html_part"] = html_part
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description
        if text_part is not None:
            self._values["text_part"] = text_part

    @builtins.property
    def subject(self) -> builtins.str:
        """``AWS::Pinpoint::EmailTemplate.Subject``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-subject
        """
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return result

    @builtins.property
    def template_name(self) -> builtins.str:
        """``AWS::Pinpoint::EmailTemplate.TemplateName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatename
        """
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return result

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailTemplate.DefaultSubstitutions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-defaultsubstitutions
        """
        result = self._values.get("default_substitutions")
        return result

    @builtins.property
    def html_part(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailTemplate.HtmlPart``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-htmlpart
        """
        result = self._values.get("html_part")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::Pinpoint::EmailTemplate.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailTemplate.TemplateDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-templatedescription
        """
        result = self._values.get("template_description")
        return result

    @builtins.property
    def text_part(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::EmailTemplate.TextPart``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-emailtemplate.html#cfn-pinpoint-emailtemplate-textpart
        """
        result = self._values.get("text_part")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnEventStream(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnEventStream",
):
    """A CloudFormation ``AWS::Pinpoint::EventStream``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html
    :cloudformationResource: AWS::Pinpoint::EventStream
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        destination_stream_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        """Create a new ``AWS::Pinpoint::EventStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::EventStream.ApplicationId``.
        :param destination_stream_arn: ``AWS::Pinpoint::EventStream.DestinationStreamArn``.
        :param role_arn: ``AWS::Pinpoint::EventStream.RoleArn``.
        """
        props = CfnEventStreamProps(
            application_id=application_id,
            destination_stream_arn=destination_stream_arn,
            role_arn=role_arn,
        )

        jsii.create(CfnEventStream, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::EventStream.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="destinationStreamArn")
    def destination_stream_arn(self) -> builtins.str:
        """``AWS::Pinpoint::EventStream.DestinationStreamArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-destinationstreamarn
        """
        return jsii.get(self, "destinationStreamArn")

    @destination_stream_arn.setter # type: ignore
    def destination_stream_arn(self, value: builtins.str) -> None:
        jsii.set(self, "destinationStreamArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        """``AWS::Pinpoint::EventStream.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "roleArn", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnEventStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "destination_stream_arn": "destinationStreamArn",
        "role_arn": "roleArn",
    },
)
class CfnEventStreamProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        destination_stream_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::EventStream``.

        :param application_id: ``AWS::Pinpoint::EventStream.ApplicationId``.
        :param destination_stream_arn: ``AWS::Pinpoint::EventStream.DestinationStreamArn``.
        :param role_arn: ``AWS::Pinpoint::EventStream.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
            "destination_stream_arn": destination_stream_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::EventStream.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def destination_stream_arn(self) -> builtins.str:
        """``AWS::Pinpoint::EventStream.DestinationStreamArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-destinationstreamarn
        """
        result = self._values.get("destination_stream_arn")
        assert result is not None, "Required property 'destination_stream_arn' is missing"
        return result

    @builtins.property
    def role_arn(self) -> builtins.str:
        """``AWS::Pinpoint::EventStream.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-eventstream.html#cfn-pinpoint-eventstream-rolearn
        """
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnGCMChannel(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnGCMChannel",
):
    """A CloudFormation ``AWS::Pinpoint::GCMChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html
    :cloudformationResource: AWS::Pinpoint::GCMChannel
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::GCMChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key: ``AWS::Pinpoint::GCMChannel.ApiKey``.
        :param application_id: ``AWS::Pinpoint::GCMChannel.ApplicationId``.
        :param enabled: ``AWS::Pinpoint::GCMChannel.Enabled``.
        """
        props = CfnGCMChannelProps(
            api_key=api_key, application_id=application_id, enabled=enabled
        )

        jsii.create(CfnGCMChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        """``AWS::Pinpoint::GCMChannel.ApiKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-apikey
        """
        return jsii.get(self, "apiKey")

    @api_key.setter # type: ignore
    def api_key(self, value: builtins.str) -> None:
        jsii.set(self, "apiKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::GCMChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::GCMChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnGCMChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "application_id": "applicationId",
        "enabled": "enabled",
    },
)
class CfnGCMChannelProps:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::GCMChannel``.

        :param api_key: ``AWS::Pinpoint::GCMChannel.ApiKey``.
        :param application_id: ``AWS::Pinpoint::GCMChannel.ApplicationId``.
        :param enabled: ``AWS::Pinpoint::GCMChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "api_key": api_key,
            "application_id": application_id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def api_key(self) -> builtins.str:
        """``AWS::Pinpoint::GCMChannel.ApiKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-apikey
        """
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return result

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::GCMChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::GCMChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-gcmchannel.html#cfn-pinpoint-gcmchannel-enabled
        """
        result = self._values.get("enabled")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGCMChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnPushTemplate(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnPushTemplate",
):
    """A CloudFormation ``AWS::Pinpoint::PushTemplate``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html
    :cloudformationResource: AWS::Pinpoint::PushTemplate
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        template_name: builtins.str,
        adm: typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_6e2f5d88]] = None,
        apns: typing.Optional[typing.Union["CfnPushTemplate.APNSPushNotificationTemplateProperty", _IResolvable_6e2f5d88]] = None,
        baidu: typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_6e2f5d88]] = None,
        default: typing.Optional[typing.Union["CfnPushTemplate.DefaultPushNotificationTemplateProperty", _IResolvable_6e2f5d88]] = None,
        default_substitutions: typing.Optional[builtins.str] = None,
        gcm: typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_6e2f5d88]] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::PushTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template_name: ``AWS::Pinpoint::PushTemplate.TemplateName``.
        :param adm: ``AWS::Pinpoint::PushTemplate.ADM``.
        :param apns: ``AWS::Pinpoint::PushTemplate.APNS``.
        :param baidu: ``AWS::Pinpoint::PushTemplate.Baidu``.
        :param default: ``AWS::Pinpoint::PushTemplate.Default``.
        :param default_substitutions: ``AWS::Pinpoint::PushTemplate.DefaultSubstitutions``.
        :param gcm: ``AWS::Pinpoint::PushTemplate.GCM``.
        :param tags: ``AWS::Pinpoint::PushTemplate.Tags``.
        :param template_description: ``AWS::Pinpoint::PushTemplate.TemplateDescription``.
        """
        props = CfnPushTemplateProps(
            template_name=template_name,
            adm=adm,
            apns=apns,
            baidu=baidu,
            default=default,
            default_substitutions=default_substitutions,
            gcm=gcm,
            tags=tags,
            template_description=template_description,
        )

        jsii.create(CfnPushTemplate, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::Pinpoint::PushTemplate.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        """``AWS::Pinpoint::PushTemplate.TemplateName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatename
        """
        return jsii.get(self, "templateName")

    @template_name.setter # type: ignore
    def template_name(self, value: builtins.str) -> None:
        jsii.set(self, "templateName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="adm")
    def adm(
        self,
    ) -> typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::PushTemplate.ADM``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-adm
        """
        return jsii.get(self, "adm")

    @adm.setter # type: ignore
    def adm(
        self,
        value: typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "adm", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apns")
    def apns(
        self,
    ) -> typing.Optional[typing.Union["CfnPushTemplate.APNSPushNotificationTemplateProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::PushTemplate.APNS``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-apns
        """
        return jsii.get(self, "apns")

    @apns.setter # type: ignore
    def apns(
        self,
        value: typing.Optional[typing.Union["CfnPushTemplate.APNSPushNotificationTemplateProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "apns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="baidu")
    def baidu(
        self,
    ) -> typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::PushTemplate.Baidu``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-baidu
        """
        return jsii.get(self, "baidu")

    @baidu.setter # type: ignore
    def baidu(
        self,
        value: typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "baidu", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="default")
    def default(
        self,
    ) -> typing.Optional[typing.Union["CfnPushTemplate.DefaultPushNotificationTemplateProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::PushTemplate.Default``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-default
        """
        return jsii.get(self, "default")

    @default.setter # type: ignore
    def default(
        self,
        value: typing.Optional[typing.Union["CfnPushTemplate.DefaultPushNotificationTemplateProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "default", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultSubstitutions")
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::PushTemplate.DefaultSubstitutions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-defaultsubstitutions
        """
        return jsii.get(self, "defaultSubstitutions")

    @default_substitutions.setter # type: ignore
    def default_substitutions(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultSubstitutions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gcm")
    def gcm(
        self,
    ) -> typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::PushTemplate.GCM``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-gcm
        """
        return jsii.get(self, "gcm")

    @gcm.setter # type: ignore
    def gcm(
        self,
        value: typing.Optional[typing.Union["CfnPushTemplate.AndroidPushNotificationTemplateProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "gcm", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::PushTemplate.TemplateDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatedescription
        """
        return jsii.get(self, "templateDescription")

    @template_description.setter # type: ignore
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "templateDescription", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnPushTemplate.APNSPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "media_url": "mediaUrl",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class APNSPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            media_url: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param action: ``CfnPushTemplate.APNSPushNotificationTemplateProperty.Action``.
            :param body: ``CfnPushTemplate.APNSPushNotificationTemplateProperty.Body``.
            :param media_url: ``CfnPushTemplate.APNSPushNotificationTemplateProperty.MediaUrl``.
            :param sound: ``CfnPushTemplate.APNSPushNotificationTemplateProperty.Sound``.
            :param title: ``CfnPushTemplate.APNSPushNotificationTemplateProperty.Title``.
            :param url: ``CfnPushTemplate.APNSPushNotificationTemplateProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if media_url is not None:
                self._values["media_url"] = media_url
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.APNSPushNotificationTemplateProperty.Action``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-action
            """
            result = self._values.get("action")
            return result

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.APNSPushNotificationTemplateProperty.Body``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-body
            """
            result = self._values.get("body")
            return result

        @builtins.property
        def media_url(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.APNSPushNotificationTemplateProperty.MediaUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-mediaurl
            """
            result = self._values.get("media_url")
            return result

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.APNSPushNotificationTemplateProperty.Sound``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-sound
            """
            result = self._values.get("sound")
            return result

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.APNSPushNotificationTemplateProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-title
            """
            result = self._values.get("title")
            return result

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.APNSPushNotificationTemplateProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-apnspushnotificationtemplate.html#cfn-pinpoint-pushtemplate-apnspushnotificationtemplate-url
            """
            result = self._values.get("url")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "APNSPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnPushTemplate.AndroidPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "image_icon_url": "imageIconUrl",
            "image_url": "imageUrl",
            "small_image_icon_url": "smallImageIconUrl",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class AndroidPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            image_icon_url: typing.Optional[builtins.str] = None,
            image_url: typing.Optional[builtins.str] = None,
            small_image_icon_url: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param action: ``CfnPushTemplate.AndroidPushNotificationTemplateProperty.Action``.
            :param body: ``CfnPushTemplate.AndroidPushNotificationTemplateProperty.Body``.
            :param image_icon_url: ``CfnPushTemplate.AndroidPushNotificationTemplateProperty.ImageIconUrl``.
            :param image_url: ``CfnPushTemplate.AndroidPushNotificationTemplateProperty.ImageUrl``.
            :param small_image_icon_url: ``CfnPushTemplate.AndroidPushNotificationTemplateProperty.SmallImageIconUrl``.
            :param sound: ``CfnPushTemplate.AndroidPushNotificationTemplateProperty.Sound``.
            :param title: ``CfnPushTemplate.AndroidPushNotificationTemplateProperty.Title``.
            :param url: ``CfnPushTemplate.AndroidPushNotificationTemplateProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if image_icon_url is not None:
                self._values["image_icon_url"] = image_icon_url
            if image_url is not None:
                self._values["image_url"] = image_url
            if small_image_icon_url is not None:
                self._values["small_image_icon_url"] = small_image_icon_url
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.AndroidPushNotificationTemplateProperty.Action``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-action
            """
            result = self._values.get("action")
            return result

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.AndroidPushNotificationTemplateProperty.Body``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-body
            """
            result = self._values.get("body")
            return result

        @builtins.property
        def image_icon_url(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.AndroidPushNotificationTemplateProperty.ImageIconUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-imageiconurl
            """
            result = self._values.get("image_icon_url")
            return result

        @builtins.property
        def image_url(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.AndroidPushNotificationTemplateProperty.ImageUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-imageurl
            """
            result = self._values.get("image_url")
            return result

        @builtins.property
        def small_image_icon_url(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.AndroidPushNotificationTemplateProperty.SmallImageIconUrl``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-smallimageiconurl
            """
            result = self._values.get("small_image_icon_url")
            return result

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.AndroidPushNotificationTemplateProperty.Sound``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-sound
            """
            result = self._values.get("sound")
            return result

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.AndroidPushNotificationTemplateProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-title
            """
            result = self._values.get("title")
            return result

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.AndroidPushNotificationTemplateProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-androidpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-androidpushnotificationtemplate-url
            """
            result = self._values.get("url")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AndroidPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnPushTemplate.DefaultPushNotificationTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "body": "body",
            "sound": "sound",
            "title": "title",
            "url": "url",
        },
    )
    class DefaultPushNotificationTemplateProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            body: typing.Optional[builtins.str] = None,
            sound: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param action: ``CfnPushTemplate.DefaultPushNotificationTemplateProperty.Action``.
            :param body: ``CfnPushTemplate.DefaultPushNotificationTemplateProperty.Body``.
            :param sound: ``CfnPushTemplate.DefaultPushNotificationTemplateProperty.Sound``.
            :param title: ``CfnPushTemplate.DefaultPushNotificationTemplateProperty.Title``.
            :param url: ``CfnPushTemplate.DefaultPushNotificationTemplateProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if body is not None:
                self._values["body"] = body
            if sound is not None:
                self._values["sound"] = sound
            if title is not None:
                self._values["title"] = title
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.DefaultPushNotificationTemplateProperty.Action``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-action
            """
            result = self._values.get("action")
            return result

        @builtins.property
        def body(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.DefaultPushNotificationTemplateProperty.Body``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-body
            """
            result = self._values.get("body")
            return result

        @builtins.property
        def sound(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.DefaultPushNotificationTemplateProperty.Sound``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-sound
            """
            result = self._values.get("sound")
            return result

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.DefaultPushNotificationTemplateProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-title
            """
            result = self._values.get("title")
            return result

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            """``CfnPushTemplate.DefaultPushNotificationTemplateProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-pushtemplate-defaultpushnotificationtemplate.html#cfn-pinpoint-pushtemplate-defaultpushnotificationtemplate-url
            """
            result = self._values.get("url")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultPushNotificationTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnPushTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_name": "templateName",
        "adm": "adm",
        "apns": "apns",
        "baidu": "baidu",
        "default": "default",
        "default_substitutions": "defaultSubstitutions",
        "gcm": "gcm",
        "tags": "tags",
        "template_description": "templateDescription",
    },
)
class CfnPushTemplateProps:
    def __init__(
        self,
        *,
        template_name: builtins.str,
        adm: typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_6e2f5d88]] = None,
        apns: typing.Optional[typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, _IResolvable_6e2f5d88]] = None,
        baidu: typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_6e2f5d88]] = None,
        default: typing.Optional[typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, _IResolvable_6e2f5d88]] = None,
        default_substitutions: typing.Optional[builtins.str] = None,
        gcm: typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_6e2f5d88]] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::PushTemplate``.

        :param template_name: ``AWS::Pinpoint::PushTemplate.TemplateName``.
        :param adm: ``AWS::Pinpoint::PushTemplate.ADM``.
        :param apns: ``AWS::Pinpoint::PushTemplate.APNS``.
        :param baidu: ``AWS::Pinpoint::PushTemplate.Baidu``.
        :param default: ``AWS::Pinpoint::PushTemplate.Default``.
        :param default_substitutions: ``AWS::Pinpoint::PushTemplate.DefaultSubstitutions``.
        :param gcm: ``AWS::Pinpoint::PushTemplate.GCM``.
        :param tags: ``AWS::Pinpoint::PushTemplate.Tags``.
        :param template_description: ``AWS::Pinpoint::PushTemplate.TemplateDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "template_name": template_name,
        }
        if adm is not None:
            self._values["adm"] = adm
        if apns is not None:
            self._values["apns"] = apns
        if baidu is not None:
            self._values["baidu"] = baidu
        if default is not None:
            self._values["default"] = default
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if gcm is not None:
            self._values["gcm"] = gcm
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description

    @builtins.property
    def template_name(self) -> builtins.str:
        """``AWS::Pinpoint::PushTemplate.TemplateName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatename
        """
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return result

    @builtins.property
    def adm(
        self,
    ) -> typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::PushTemplate.ADM``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-adm
        """
        result = self._values.get("adm")
        return result

    @builtins.property
    def apns(
        self,
    ) -> typing.Optional[typing.Union[CfnPushTemplate.APNSPushNotificationTemplateProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::PushTemplate.APNS``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-apns
        """
        result = self._values.get("apns")
        return result

    @builtins.property
    def baidu(
        self,
    ) -> typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::PushTemplate.Baidu``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-baidu
        """
        result = self._values.get("baidu")
        return result

    @builtins.property
    def default(
        self,
    ) -> typing.Optional[typing.Union[CfnPushTemplate.DefaultPushNotificationTemplateProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::PushTemplate.Default``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-default
        """
        result = self._values.get("default")
        return result

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::PushTemplate.DefaultSubstitutions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-defaultsubstitutions
        """
        result = self._values.get("default_substitutions")
        return result

    @builtins.property
    def gcm(
        self,
    ) -> typing.Optional[typing.Union[CfnPushTemplate.AndroidPushNotificationTemplateProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::PushTemplate.GCM``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-gcm
        """
        result = self._values.get("gcm")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::Pinpoint::PushTemplate.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::PushTemplate.TemplateDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-pushtemplate.html#cfn-pinpoint-pushtemplate-templatedescription
        """
        result = self._values.get("template_description")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPushTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnSMSChannel(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnSMSChannel",
):
    """A CloudFormation ``AWS::Pinpoint::SMSChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html
    :cloudformationResource: AWS::Pinpoint::SMSChannel
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        sender_id: typing.Optional[builtins.str] = None,
        short_code: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::SMSChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::SMSChannel.ApplicationId``.
        :param enabled: ``AWS::Pinpoint::SMSChannel.Enabled``.
        :param sender_id: ``AWS::Pinpoint::SMSChannel.SenderId``.
        :param short_code: ``AWS::Pinpoint::SMSChannel.ShortCode``.
        """
        props = CfnSMSChannelProps(
            application_id=application_id,
            enabled=enabled,
            sender_id=sender_id,
            short_code=short_code,
        )

        jsii.create(CfnSMSChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::SMSChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::SMSChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="senderId")
    def sender_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::SMSChannel.SenderId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-senderid
        """
        return jsii.get(self, "senderId")

    @sender_id.setter # type: ignore
    def sender_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "senderId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="shortCode")
    def short_code(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::SMSChannel.ShortCode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-shortcode
        """
        return jsii.get(self, "shortCode")

    @short_code.setter # type: ignore
    def short_code(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "shortCode", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnSMSChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "enabled": "enabled",
        "sender_id": "senderId",
        "short_code": "shortCode",
    },
)
class CfnSMSChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
        sender_id: typing.Optional[builtins.str] = None,
        short_code: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::SMSChannel``.

        :param application_id: ``AWS::Pinpoint::SMSChannel.ApplicationId``.
        :param enabled: ``AWS::Pinpoint::SMSChannel.Enabled``.
        :param sender_id: ``AWS::Pinpoint::SMSChannel.SenderId``.
        :param short_code: ``AWS::Pinpoint::SMSChannel.ShortCode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if sender_id is not None:
            self._values["sender_id"] = sender_id
        if short_code is not None:
            self._values["short_code"] = short_code

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::SMSChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::SMSChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-enabled
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def sender_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::SMSChannel.SenderId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-senderid
        """
        result = self._values.get("sender_id")
        return result

    @builtins.property
    def short_code(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::SMSChannel.ShortCode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smschannel.html#cfn-pinpoint-smschannel-shortcode
        """
        result = self._values.get("short_code")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSMSChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnSegment(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment",
):
    """A CloudFormation ``AWS::Pinpoint::Segment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html
    :cloudformationResource: AWS::Pinpoint::Segment
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        name: builtins.str,
        dimensions: typing.Optional[typing.Union["CfnSegment.SegmentDimensionsProperty", _IResolvable_6e2f5d88]] = None,
        segment_groups: typing.Optional[typing.Union["CfnSegment.SegmentGroupsProperty", _IResolvable_6e2f5d88]] = None,
        tags: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::Segment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::Segment.ApplicationId``.
        :param name: ``AWS::Pinpoint::Segment.Name``.
        :param dimensions: ``AWS::Pinpoint::Segment.Dimensions``.
        :param segment_groups: ``AWS::Pinpoint::Segment.SegmentGroups``.
        :param tags: ``AWS::Pinpoint::Segment.Tags``.
        """
        props = CfnSegmentProps(
            application_id=application_id,
            name=name,
            dimensions=dimensions,
            segment_groups=segment_groups,
            tags=tags,
        )

        jsii.create(CfnSegment, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="attrSegmentId")
    def attr_segment_id(self) -> builtins.str:
        """
        :cloudformationAttribute: SegmentId
        """
        return jsii.get(self, "attrSegmentId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::Pinpoint::Segment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::Segment.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::Pinpoint::Segment.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dimensions")
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union["CfnSegment.SegmentDimensionsProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::Segment.Dimensions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-dimensions
        """
        return jsii.get(self, "dimensions")

    @dimensions.setter # type: ignore
    def dimensions(
        self,
        value: typing.Optional[typing.Union["CfnSegment.SegmentDimensionsProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "dimensions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="segmentGroups")
    def segment_groups(
        self,
    ) -> typing.Optional[typing.Union["CfnSegment.SegmentGroupsProperty", _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::Segment.SegmentGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-segmentgroups
        """
        return jsii.get(self, "segmentGroups")

    @segment_groups.setter # type: ignore
    def segment_groups(
        self,
        value: typing.Optional[typing.Union["CfnSegment.SegmentGroupsProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "segmentGroups", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.AttributeDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute_type": "attributeType", "values": "values"},
    )
    class AttributeDimensionProperty:
        def __init__(
            self,
            *,
            attribute_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param attribute_type: ``CfnSegment.AttributeDimensionProperty.AttributeType``.
            :param values: ``CfnSegment.AttributeDimensionProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-attributedimension.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if attribute_type is not None:
                self._values["attribute_type"] = attribute_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def attribute_type(self) -> typing.Optional[builtins.str]:
            """``CfnSegment.AttributeDimensionProperty.AttributeType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-attributedimension.html#cfn-pinpoint-segment-attributedimension-attributetype
            """
            result = self._values.get("attribute_type")
            return result

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnSegment.AttributeDimensionProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-attributedimension.html#cfn-pinpoint-segment-attributedimension-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.BehaviorProperty",
        jsii_struct_bases=[],
        name_mapping={"recency": "recency"},
    )
    class BehaviorProperty:
        def __init__(
            self,
            *,
            recency: typing.Optional[typing.Union["CfnSegment.RecencyProperty", _IResolvable_6e2f5d88]] = None,
        ) -> None:
            """
            :param recency: ``CfnSegment.BehaviorProperty.Recency``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if recency is not None:
                self._values["recency"] = recency

        @builtins.property
        def recency(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.RecencyProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.BehaviorProperty.Recency``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior.html#cfn-pinpoint-segment-segmentdimensions-behavior-recency
            """
            result = self._values.get("recency")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BehaviorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.CoordinatesProperty",
        jsii_struct_bases=[],
        name_mapping={"latitude": "latitude", "longitude": "longitude"},
    )
    class CoordinatesProperty:
        def __init__(self, *, latitude: jsii.Number, longitude: jsii.Number) -> None:
            """
            :param latitude: ``CfnSegment.CoordinatesProperty.Latitude``.
            :param longitude: ``CfnSegment.CoordinatesProperty.Longitude``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "latitude": latitude,
                "longitude": longitude,
            }

        @builtins.property
        def latitude(self) -> jsii.Number:
            """``CfnSegment.CoordinatesProperty.Latitude``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates-latitude
            """
            result = self._values.get("latitude")
            assert result is not None, "Required property 'latitude' is missing"
            return result

        @builtins.property
        def longitude(self) -> jsii.Number:
            """``CfnSegment.CoordinatesProperty.Longitude``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates-longitude
            """
            result = self._values.get("longitude")
            assert result is not None, "Required property 'longitude' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoordinatesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.DemographicProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_version": "appVersion",
            "channel": "channel",
            "device_type": "deviceType",
            "make": "make",
            "model": "model",
            "platform": "platform",
        },
    )
    class DemographicProperty:
        def __init__(
            self,
            *,
            app_version: typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]] = None,
            channel: typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]] = None,
            device_type: typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]] = None,
            make: typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]] = None,
            model: typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]] = None,
            platform: typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]] = None,
        ) -> None:
            """
            :param app_version: ``CfnSegment.DemographicProperty.AppVersion``.
            :param channel: ``CfnSegment.DemographicProperty.Channel``.
            :param device_type: ``CfnSegment.DemographicProperty.DeviceType``.
            :param make: ``CfnSegment.DemographicProperty.Make``.
            :param model: ``CfnSegment.DemographicProperty.Model``.
            :param platform: ``CfnSegment.DemographicProperty.Platform``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if app_version is not None:
                self._values["app_version"] = app_version
            if channel is not None:
                self._values["channel"] = channel
            if device_type is not None:
                self._values["device_type"] = device_type
            if make is not None:
                self._values["make"] = make
            if model is not None:
                self._values["model"] = model
            if platform is not None:
                self._values["platform"] = platform

        @builtins.property
        def app_version(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.DemographicProperty.AppVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-appversion
            """
            result = self._values.get("app_version")
            return result

        @builtins.property
        def channel(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.DemographicProperty.Channel``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-channel
            """
            result = self._values.get("channel")
            return result

        @builtins.property
        def device_type(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.DemographicProperty.DeviceType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-devicetype
            """
            result = self._values.get("device_type")
            return result

        @builtins.property
        def make(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.DemographicProperty.Make``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-make
            """
            result = self._values.get("make")
            return result

        @builtins.property
        def model(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.DemographicProperty.Model``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-model
            """
            result = self._values.get("model")
            return result

        @builtins.property
        def platform(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.DemographicProperty.Platform``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-demographic.html#cfn-pinpoint-segment-segmentdimensions-demographic-platform
            """
            result = self._values.get("platform")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DemographicProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.GPSPointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "coordinates": "coordinates",
            "range_in_kilometers": "rangeInKilometers",
        },
    )
    class GPSPointProperty:
        def __init__(
            self,
            *,
            coordinates: typing.Union["CfnSegment.CoordinatesProperty", _IResolvable_6e2f5d88],
            range_in_kilometers: jsii.Number,
        ) -> None:
            """
            :param coordinates: ``CfnSegment.GPSPointProperty.Coordinates``.
            :param range_in_kilometers: ``CfnSegment.GPSPointProperty.RangeInKilometers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "coordinates": coordinates,
                "range_in_kilometers": range_in_kilometers,
            }

        @builtins.property
        def coordinates(
            self,
        ) -> typing.Union["CfnSegment.CoordinatesProperty", _IResolvable_6e2f5d88]:
            """``CfnSegment.GPSPointProperty.Coordinates``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-coordinates
            """
            result = self._values.get("coordinates")
            assert result is not None, "Required property 'coordinates' is missing"
            return result

        @builtins.property
        def range_in_kilometers(self) -> jsii.Number:
            """``CfnSegment.GPSPointProperty.RangeInKilometers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location-gpspoint.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint-rangeinkilometers
            """
            result = self._values.get("range_in_kilometers")
            assert result is not None, "Required property 'range_in_kilometers' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GPSPointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.GroupsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "source_segments": "sourceSegments",
            "source_type": "sourceType",
            "type": "type",
        },
    )
    class GroupsProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnSegment.SegmentDimensionsProperty", _IResolvable_6e2f5d88]]]] = None,
            source_segments: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnSegment.SourceSegmentsProperty", _IResolvable_6e2f5d88]]]] = None,
            source_type: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param dimensions: ``CfnSegment.GroupsProperty.Dimensions``.
            :param source_segments: ``CfnSegment.GroupsProperty.SourceSegments``.
            :param source_type: ``CfnSegment.GroupsProperty.SourceType``.
            :param type: ``CfnSegment.GroupsProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if source_segments is not None:
                self._values["source_segments"] = source_segments
            if source_type is not None:
                self._values["source_type"] = source_type
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnSegment.SegmentDimensionsProperty", _IResolvable_6e2f5d88]]]]:
            """``CfnSegment.GroupsProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-dimensions
            """
            result = self._values.get("dimensions")
            return result

        @builtins.property
        def source_segments(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnSegment.SourceSegmentsProperty", _IResolvable_6e2f5d88]]]]:
            """``CfnSegment.GroupsProperty.SourceSegments``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-sourcesegments
            """
            result = self._values.get("source_segments")
            return result

        @builtins.property
        def source_type(self) -> typing.Optional[builtins.str]:
            """``CfnSegment.GroupsProperty.SourceType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-sourcetype
            """
            result = self._values.get("source_type")
            return result

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            """``CfnSegment.GroupsProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups.html#cfn-pinpoint-segment-segmentgroups-groups-type
            """
            result = self._values.get("type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"country": "country", "gps_point": "gpsPoint"},
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            country: typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]] = None,
            gps_point: typing.Optional[typing.Union["CfnSegment.GPSPointProperty", _IResolvable_6e2f5d88]] = None,
        ) -> None:
            """
            :param country: ``CfnSegment.LocationProperty.Country``.
            :param gps_point: ``CfnSegment.LocationProperty.GPSPoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if country is not None:
                self._values["country"] = country
            if gps_point is not None:
                self._values["gps_point"] = gps_point

        @builtins.property
        def country(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.SetDimensionProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.LocationProperty.Country``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location.html#cfn-pinpoint-segment-segmentdimensions-location-country
            """
            result = self._values.get("country")
            return result

        @builtins.property
        def gps_point(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.GPSPointProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.LocationProperty.GPSPoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-location.html#cfn-pinpoint-segment-segmentdimensions-location-gpspoint
            """
            result = self._values.get("gps_point")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.RecencyProperty",
        jsii_struct_bases=[],
        name_mapping={"duration": "duration", "recency_type": "recencyType"},
    )
    class RecencyProperty:
        def __init__(
            self,
            *,
            duration: builtins.str,
            recency_type: builtins.str,
        ) -> None:
            """
            :param duration: ``CfnSegment.RecencyProperty.Duration``.
            :param recency_type: ``CfnSegment.RecencyProperty.RecencyType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior-recency.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "duration": duration,
                "recency_type": recency_type,
            }

        @builtins.property
        def duration(self) -> builtins.str:
            """``CfnSegment.RecencyProperty.Duration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior-recency.html#cfn-pinpoint-segment-segmentdimensions-behavior-recency-duration
            """
            result = self._values.get("duration")
            assert result is not None, "Required property 'duration' is missing"
            return result

        @builtins.property
        def recency_type(self) -> builtins.str:
            """``CfnSegment.RecencyProperty.RecencyType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions-behavior-recency.html#cfn-pinpoint-segment-segmentdimensions-behavior-recency-recencytype
            """
            result = self._values.get("recency_type")
            assert result is not None, "Required property 'recency_type' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.SegmentDimensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "behavior": "behavior",
            "demographic": "demographic",
            "location": "location",
            "metrics": "metrics",
            "user_attributes": "userAttributes",
        },
    )
    class SegmentDimensionsProperty:
        def __init__(
            self,
            *,
            attributes: typing.Any = None,
            behavior: typing.Optional[typing.Union["CfnSegment.BehaviorProperty", _IResolvable_6e2f5d88]] = None,
            demographic: typing.Optional[typing.Union["CfnSegment.DemographicProperty", _IResolvable_6e2f5d88]] = None,
            location: typing.Optional[typing.Union["CfnSegment.LocationProperty", _IResolvable_6e2f5d88]] = None,
            metrics: typing.Any = None,
            user_attributes: typing.Any = None,
        ) -> None:
            """
            :param attributes: ``CfnSegment.SegmentDimensionsProperty.Attributes``.
            :param behavior: ``CfnSegment.SegmentDimensionsProperty.Behavior``.
            :param demographic: ``CfnSegment.SegmentDimensionsProperty.Demographic``.
            :param location: ``CfnSegment.SegmentDimensionsProperty.Location``.
            :param metrics: ``CfnSegment.SegmentDimensionsProperty.Metrics``.
            :param user_attributes: ``CfnSegment.SegmentDimensionsProperty.UserAttributes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if behavior is not None:
                self._values["behavior"] = behavior
            if demographic is not None:
                self._values["demographic"] = demographic
            if location is not None:
                self._values["location"] = location
            if metrics is not None:
                self._values["metrics"] = metrics
            if user_attributes is not None:
                self._values["user_attributes"] = user_attributes

        @builtins.property
        def attributes(self) -> typing.Any:
            """``CfnSegment.SegmentDimensionsProperty.Attributes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-attributes
            """
            result = self._values.get("attributes")
            return result

        @builtins.property
        def behavior(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.BehaviorProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.SegmentDimensionsProperty.Behavior``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-behavior
            """
            result = self._values.get("behavior")
            return result

        @builtins.property
        def demographic(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.DemographicProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.SegmentDimensionsProperty.Demographic``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-demographic
            """
            result = self._values.get("demographic")
            return result

        @builtins.property
        def location(
            self,
        ) -> typing.Optional[typing.Union["CfnSegment.LocationProperty", _IResolvable_6e2f5d88]]:
            """``CfnSegment.SegmentDimensionsProperty.Location``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-location
            """
            result = self._values.get("location")
            return result

        @builtins.property
        def metrics(self) -> typing.Any:
            """``CfnSegment.SegmentDimensionsProperty.Metrics``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-metrics
            """
            result = self._values.get("metrics")
            return result

        @builtins.property
        def user_attributes(self) -> typing.Any:
            """``CfnSegment.SegmentDimensionsProperty.UserAttributes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentdimensions.html#cfn-pinpoint-segment-segmentdimensions-userattributes
            """
            result = self._values.get("user_attributes")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentDimensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.SegmentGroupsProperty",
        jsii_struct_bases=[],
        name_mapping={"groups": "groups", "include": "include"},
    )
    class SegmentGroupsProperty:
        def __init__(
            self,
            *,
            groups: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnSegment.GroupsProperty", _IResolvable_6e2f5d88]]]] = None,
            include: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param groups: ``CfnSegment.SegmentGroupsProperty.Groups``.
            :param include: ``CfnSegment.SegmentGroupsProperty.Include``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if groups is not None:
                self._values["groups"] = groups
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def groups(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnSegment.GroupsProperty", _IResolvable_6e2f5d88]]]]:
            """``CfnSegment.SegmentGroupsProperty.Groups``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html#cfn-pinpoint-segment-segmentgroups-groups
            """
            result = self._values.get("groups")
            return result

        @builtins.property
        def include(self) -> typing.Optional[builtins.str]:
            """``CfnSegment.SegmentGroupsProperty.Include``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups.html#cfn-pinpoint-segment-segmentgroups-include
            """
            result = self._values.get("include")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentGroupsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.SetDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_type": "dimensionType", "values": "values"},
    )
    class SetDimensionProperty:
        def __init__(
            self,
            *,
            dimension_type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param dimension_type: ``CfnSegment.SetDimensionProperty.DimensionType``.
            :param values: ``CfnSegment.SetDimensionProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if dimension_type is not None:
                self._values["dimension_type"] = dimension_type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def dimension_type(self) -> typing.Optional[builtins.str]:
            """``CfnSegment.SetDimensionProperty.DimensionType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html#cfn-pinpoint-segment-setdimension-dimensiontype
            """
            result = self._values.get("dimension_type")
            return result

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnSegment.SetDimensionProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-setdimension.html#cfn-pinpoint-segment-setdimension-values
            """
            result = self._values.get("values")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegment.SourceSegmentsProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "version": "version"},
    )
    class SourceSegmentsProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param id: ``CfnSegment.SourceSegmentsProperty.Id``.
            :param version: ``CfnSegment.SourceSegmentsProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups-sourcesegments.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def id(self) -> builtins.str:
            """``CfnSegment.SourceSegmentsProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups-sourcesegments.html#cfn-pinpoint-segment-segmentgroups-groups-sourcesegments-id
            """
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return result

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            """``CfnSegment.SourceSegmentsProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pinpoint-segment-segmentgroups-groups-sourcesegments.html#cfn-pinpoint-segment-segmentgroups-groups-sourcesegments-version
            """
            result = self._values.get("version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceSegmentsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnSegmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "name": "name",
        "dimensions": "dimensions",
        "segment_groups": "segmentGroups",
        "tags": "tags",
    },
)
class CfnSegmentProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        name: builtins.str,
        dimensions: typing.Optional[typing.Union[CfnSegment.SegmentDimensionsProperty, _IResolvable_6e2f5d88]] = None,
        segment_groups: typing.Optional[typing.Union[CfnSegment.SegmentGroupsProperty, _IResolvable_6e2f5d88]] = None,
        tags: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::Segment``.

        :param application_id: ``AWS::Pinpoint::Segment.ApplicationId``.
        :param name: ``AWS::Pinpoint::Segment.Name``.
        :param dimensions: ``AWS::Pinpoint::Segment.Dimensions``.
        :param segment_groups: ``AWS::Pinpoint::Segment.SegmentGroups``.
        :param tags: ``AWS::Pinpoint::Segment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
            "name": name,
        }
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if segment_groups is not None:
            self._values["segment_groups"] = segment_groups
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::Segment.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::Pinpoint::Segment.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def dimensions(
        self,
    ) -> typing.Optional[typing.Union[CfnSegment.SegmentDimensionsProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::Segment.Dimensions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-dimensions
        """
        result = self._values.get("dimensions")
        return result

    @builtins.property
    def segment_groups(
        self,
    ) -> typing.Optional[typing.Union[CfnSegment.SegmentGroupsProperty, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::Segment.SegmentGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-segmentgroups
        """
        result = self._values.get("segment_groups")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::Pinpoint::Segment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-segment.html#cfn-pinpoint-segment-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSegmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnSmsTemplate(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnSmsTemplate",
):
    """A CloudFormation ``AWS::Pinpoint::SmsTemplate``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html
    :cloudformationResource: AWS::Pinpoint::SmsTemplate
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        body: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::SmsTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param body: ``AWS::Pinpoint::SmsTemplate.Body``.
        :param template_name: ``AWS::Pinpoint::SmsTemplate.TemplateName``.
        :param default_substitutions: ``AWS::Pinpoint::SmsTemplate.DefaultSubstitutions``.
        :param tags: ``AWS::Pinpoint::SmsTemplate.Tags``.
        :param template_description: ``AWS::Pinpoint::SmsTemplate.TemplateDescription``.
        """
        props = CfnSmsTemplateProps(
            body=body,
            template_name=template_name,
            default_substitutions=default_substitutions,
            tags=tags,
            template_description=template_description,
        )

        jsii.create(CfnSmsTemplate, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::Pinpoint::SmsTemplate.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        """``AWS::Pinpoint::SmsTemplate.Body``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-body
        """
        return jsii.get(self, "body")

    @body.setter # type: ignore
    def body(self, value: builtins.str) -> None:
        jsii.set(self, "body", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        """``AWS::Pinpoint::SmsTemplate.TemplateName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatename
        """
        return jsii.get(self, "templateName")

    @template_name.setter # type: ignore
    def template_name(self, value: builtins.str) -> None:
        jsii.set(self, "templateName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultSubstitutions")
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::SmsTemplate.DefaultSubstitutions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-defaultsubstitutions
        """
        return jsii.get(self, "defaultSubstitutions")

    @default_substitutions.setter # type: ignore
    def default_substitutions(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultSubstitutions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateDescription")
    def template_description(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::SmsTemplate.TemplateDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatedescription
        """
        return jsii.get(self, "templateDescription")

    @template_description.setter # type: ignore
    def template_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "templateDescription", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnSmsTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "body": "body",
        "template_name": "templateName",
        "default_substitutions": "defaultSubstitutions",
        "tags": "tags",
        "template_description": "templateDescription",
    },
)
class CfnSmsTemplateProps:
    def __init__(
        self,
        *,
        body: builtins.str,
        template_name: builtins.str,
        default_substitutions: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        template_description: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::SmsTemplate``.

        :param body: ``AWS::Pinpoint::SmsTemplate.Body``.
        :param template_name: ``AWS::Pinpoint::SmsTemplate.TemplateName``.
        :param default_substitutions: ``AWS::Pinpoint::SmsTemplate.DefaultSubstitutions``.
        :param tags: ``AWS::Pinpoint::SmsTemplate.Tags``.
        :param template_description: ``AWS::Pinpoint::SmsTemplate.TemplateDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "body": body,
            "template_name": template_name,
        }
        if default_substitutions is not None:
            self._values["default_substitutions"] = default_substitutions
        if tags is not None:
            self._values["tags"] = tags
        if template_description is not None:
            self._values["template_description"] = template_description

    @builtins.property
    def body(self) -> builtins.str:
        """``AWS::Pinpoint::SmsTemplate.Body``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-body
        """
        result = self._values.get("body")
        assert result is not None, "Required property 'body' is missing"
        return result

    @builtins.property
    def template_name(self) -> builtins.str:
        """``AWS::Pinpoint::SmsTemplate.TemplateName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatename
        """
        result = self._values.get("template_name")
        assert result is not None, "Required property 'template_name' is missing"
        return result

    @builtins.property
    def default_substitutions(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::SmsTemplate.DefaultSubstitutions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-defaultsubstitutions
        """
        result = self._values.get("default_substitutions")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::Pinpoint::SmsTemplate.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def template_description(self) -> typing.Optional[builtins.str]:
        """``AWS::Pinpoint::SmsTemplate.TemplateDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-smstemplate.html#cfn-pinpoint-smstemplate-templatedescription
        """
        result = self._values.get("template_description")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSmsTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnVoiceChannel(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnVoiceChannel",
):
    """A CloudFormation ``AWS::Pinpoint::VoiceChannel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html
    :cloudformationResource: AWS::Pinpoint::VoiceChannel
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
    ) -> None:
        """Create a new ``AWS::Pinpoint::VoiceChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: ``AWS::Pinpoint::VoiceChannel.ApplicationId``.
        :param enabled: ``AWS::Pinpoint::VoiceChannel.Enabled``.
        """
        props = CfnVoiceChannelProps(application_id=application_id, enabled=enabled)

        jsii.create(CfnVoiceChannel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::VoiceChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-applicationid
        """
        return jsii.get(self, "applicationId")

    @application_id.setter # type: ignore
    def application_id(self, value: builtins.str) -> None:
        jsii.set(self, "applicationId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::VoiceChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_pinpoint.CfnVoiceChannelProps",
    jsii_struct_bases=[],
    name_mapping={"application_id": "applicationId", "enabled": "enabled"},
)
class CfnVoiceChannelProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Pinpoint::VoiceChannel``.

        :param application_id: ``AWS::Pinpoint::VoiceChannel.ApplicationId``.
        :param enabled: ``AWS::Pinpoint::VoiceChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def application_id(self) -> builtins.str:
        """``AWS::Pinpoint::VoiceChannel.ApplicationId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-applicationid
        """
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
        """``AWS::Pinpoint::VoiceChannel.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpoint-voicechannel.html#cfn-pinpoint-voicechannel-enabled
        """
        result = self._values.get("enabled")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVoiceChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnADMChannel",
    "CfnADMChannelProps",
    "CfnAPNSChannel",
    "CfnAPNSChannelProps",
    "CfnAPNSSandboxChannel",
    "CfnAPNSSandboxChannelProps",
    "CfnAPNSVoipChannel",
    "CfnAPNSVoipChannelProps",
    "CfnAPNSVoipSandboxChannel",
    "CfnAPNSVoipSandboxChannelProps",
    "CfnApp",
    "CfnAppProps",
    "CfnApplicationSettings",
    "CfnApplicationSettingsProps",
    "CfnBaiduChannel",
    "CfnBaiduChannelProps",
    "CfnCampaign",
    "CfnCampaignProps",
    "CfnEmailChannel",
    "CfnEmailChannelProps",
    "CfnEmailTemplate",
    "CfnEmailTemplateProps",
    "CfnEventStream",
    "CfnEventStreamProps",
    "CfnGCMChannel",
    "CfnGCMChannelProps",
    "CfnPushTemplate",
    "CfnPushTemplateProps",
    "CfnSMSChannel",
    "CfnSMSChannelProps",
    "CfnSegment",
    "CfnSegmentProps",
    "CfnSmsTemplate",
    "CfnSmsTemplateProps",
    "CfnVoiceChannel",
    "CfnVoiceChannelProps",
]

publication.publish()
