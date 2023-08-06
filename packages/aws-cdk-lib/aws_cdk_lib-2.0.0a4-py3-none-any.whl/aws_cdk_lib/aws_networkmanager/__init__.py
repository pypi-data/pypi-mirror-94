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
    CfnTag as _CfnTag_c592b05a,
    IInspectable as _IInspectable_3eb0224c,
    IResolvable as _IResolvable_6e2f5d88,
    TagManager as _TagManager_6a5badd9,
    TreeInspector as _TreeInspector_afbbf916,
)


@jsii.implements(_IInspectable_3eb0224c)
class CfnCustomerGatewayAssociation(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnCustomerGatewayAssociation",
):
    """A CloudFormation ``AWS::NetworkManager::CustomerGatewayAssociation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html
    :cloudformationResource: AWS::NetworkManager::CustomerGatewayAssociation
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        customer_gateway_arn: builtins.str,
        device_id: builtins.str,
        global_network_id: builtins.str,
        link_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::NetworkManager::CustomerGatewayAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param customer_gateway_arn: ``AWS::NetworkManager::CustomerGatewayAssociation.CustomerGatewayArn``.
        :param device_id: ``AWS::NetworkManager::CustomerGatewayAssociation.DeviceId``.
        :param global_network_id: ``AWS::NetworkManager::CustomerGatewayAssociation.GlobalNetworkId``.
        :param link_id: ``AWS::NetworkManager::CustomerGatewayAssociation.LinkId``.
        """
        props = CfnCustomerGatewayAssociationProps(
            customer_gateway_arn=customer_gateway_arn,
            device_id=device_id,
            global_network_id=global_network_id,
            link_id=link_id,
        )

        jsii.create(CfnCustomerGatewayAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="customerGatewayArn")
    def customer_gateway_arn(self) -> builtins.str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.CustomerGatewayArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-customergatewayarn
        """
        return jsii.get(self, "customerGatewayArn")

    @customer_gateway_arn.setter # type: ignore
    def customer_gateway_arn(self, value: builtins.str) -> None:
        jsii.set(self, "customerGatewayArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.DeviceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-deviceid
        """
        return jsii.get(self, "deviceId")

    @device_id.setter # type: ignore
    def device_id(self, value: builtins.str) -> None:
        jsii.set(self, "deviceId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter # type: ignore
    def global_network_id(self, value: builtins.str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="linkId")
    def link_id(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::CustomerGatewayAssociation.LinkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-linkid
        """
        return jsii.get(self, "linkId")

    @link_id.setter # type: ignore
    def link_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "linkId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnCustomerGatewayAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "customer_gateway_arn": "customerGatewayArn",
        "device_id": "deviceId",
        "global_network_id": "globalNetworkId",
        "link_id": "linkId",
    },
)
class CfnCustomerGatewayAssociationProps:
    def __init__(
        self,
        *,
        customer_gateway_arn: builtins.str,
        device_id: builtins.str,
        global_network_id: builtins.str,
        link_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::NetworkManager::CustomerGatewayAssociation``.

        :param customer_gateway_arn: ``AWS::NetworkManager::CustomerGatewayAssociation.CustomerGatewayArn``.
        :param device_id: ``AWS::NetworkManager::CustomerGatewayAssociation.DeviceId``.
        :param global_network_id: ``AWS::NetworkManager::CustomerGatewayAssociation.GlobalNetworkId``.
        :param link_id: ``AWS::NetworkManager::CustomerGatewayAssociation.LinkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "customer_gateway_arn": customer_gateway_arn,
            "device_id": device_id,
            "global_network_id": global_network_id,
        }
        if link_id is not None:
            self._values["link_id"] = link_id

    @builtins.property
    def customer_gateway_arn(self) -> builtins.str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.CustomerGatewayArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-customergatewayarn
        """
        result = self._values.get("customer_gateway_arn")
        assert result is not None, "Required property 'customer_gateway_arn' is missing"
        return result

    @builtins.property
    def device_id(self) -> builtins.str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.DeviceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-deviceid
        """
        result = self._values.get("device_id")
        assert result is not None, "Required property 'device_id' is missing"
        return result

    @builtins.property
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::CustomerGatewayAssociation.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-globalnetworkid
        """
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return result

    @builtins.property
    def link_id(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::CustomerGatewayAssociation.LinkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-linkid
        """
        result = self._values.get("link_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomerGatewayAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnDevice(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnDevice",
):
    """A CloudFormation ``AWS::NetworkManager::Device``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html
    :cloudformationResource: AWS::NetworkManager::Device
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        global_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union["CfnDevice.LocationProperty", _IResolvable_6e2f5d88]] = None,
        model: typing.Optional[builtins.str] = None,
        serial_number: typing.Optional[builtins.str] = None,
        site_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
        type: typing.Optional[builtins.str] = None,
        vendor: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::NetworkManager::Device``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param global_network_id: ``AWS::NetworkManager::Device.GlobalNetworkId``.
        :param description: ``AWS::NetworkManager::Device.Description``.
        :param location: ``AWS::NetworkManager::Device.Location``.
        :param model: ``AWS::NetworkManager::Device.Model``.
        :param serial_number: ``AWS::NetworkManager::Device.SerialNumber``.
        :param site_id: ``AWS::NetworkManager::Device.SiteId``.
        :param tags: ``AWS::NetworkManager::Device.Tags``.
        :param type: ``AWS::NetworkManager::Device.Type``.
        :param vendor: ``AWS::NetworkManager::Device.Vendor``.
        """
        props = CfnDeviceProps(
            global_network_id=global_network_id,
            description=description,
            location=location,
            model=model,
            serial_number=serial_number,
            site_id=site_id,
            tags=tags,
            type=type,
            vendor=vendor,
        )

        jsii.create(CfnDevice, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrDeviceArn")
    def attr_device_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: DeviceArn
        """
        return jsii.get(self, "attrDeviceArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrDeviceId")
    def attr_device_id(self) -> builtins.str:
        """
        :cloudformationAttribute: DeviceId
        """
        return jsii.get(self, "attrDeviceId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::NetworkManager::Device.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::Device.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter # type: ignore
    def global_network_id(self, value: builtins.str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="location")
    def location(
        self,
    ) -> typing.Optional[typing.Union["CfnDevice.LocationProperty", _IResolvable_6e2f5d88]]:
        """``AWS::NetworkManager::Device.Location``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-location
        """
        return jsii.get(self, "location")

    @location.setter # type: ignore
    def location(
        self,
        value: typing.Optional[typing.Union["CfnDevice.LocationProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "location", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="model")
    def model(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.Model``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-model
        """
        return jsii.get(self, "model")

    @model.setter # type: ignore
    def model(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "model", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.SerialNumber``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-serialnumber
        """
        return jsii.get(self, "serialNumber")

    @serial_number.setter # type: ignore
    def serial_number(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "serialNumber", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="siteId")
    def site_id(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.SiteId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-siteid
        """
        return jsii.get(self, "siteId")

    @site_id.setter # type: ignore
    def site_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "siteId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vendor")
    def vendor(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.Vendor``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-vendor
        """
        return jsii.get(self, "vendor")

    @vendor.setter # type: ignore
    def vendor(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "vendor", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_networkmanager.CfnDevice.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address": "address",
            "latitude": "latitude",
            "longitude": "longitude",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            latitude: typing.Optional[builtins.str] = None,
            longitude: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param address: ``CfnDevice.LocationProperty.Address``.
            :param latitude: ``CfnDevice.LocationProperty.Latitude``.
            :param longitude: ``CfnDevice.LocationProperty.Longitude``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if latitude is not None:
                self._values["latitude"] = latitude
            if longitude is not None:
                self._values["longitude"] = longitude

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            """``CfnDevice.LocationProperty.Address``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-address
            """
            result = self._values.get("address")
            return result

        @builtins.property
        def latitude(self) -> typing.Optional[builtins.str]:
            """``CfnDevice.LocationProperty.Latitude``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-latitude
            """
            result = self._values.get("latitude")
            return result

        @builtins.property
        def longitude(self) -> typing.Optional[builtins.str]:
            """``CfnDevice.LocationProperty.Longitude``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-longitude
            """
            result = self._values.get("longitude")
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
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnDeviceProps",
    jsii_struct_bases=[],
    name_mapping={
        "global_network_id": "globalNetworkId",
        "description": "description",
        "location": "location",
        "model": "model",
        "serial_number": "serialNumber",
        "site_id": "siteId",
        "tags": "tags",
        "type": "type",
        "vendor": "vendor",
    },
)
class CfnDeviceProps:
    def __init__(
        self,
        *,
        global_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[CfnDevice.LocationProperty, _IResolvable_6e2f5d88]] = None,
        model: typing.Optional[builtins.str] = None,
        serial_number: typing.Optional[builtins.str] = None,
        site_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
        type: typing.Optional[builtins.str] = None,
        vendor: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::NetworkManager::Device``.

        :param global_network_id: ``AWS::NetworkManager::Device.GlobalNetworkId``.
        :param description: ``AWS::NetworkManager::Device.Description``.
        :param location: ``AWS::NetworkManager::Device.Location``.
        :param model: ``AWS::NetworkManager::Device.Model``.
        :param serial_number: ``AWS::NetworkManager::Device.SerialNumber``.
        :param site_id: ``AWS::NetworkManager::Device.SiteId``.
        :param tags: ``AWS::NetworkManager::Device.Tags``.
        :param type: ``AWS::NetworkManager::Device.Type``.
        :param vendor: ``AWS::NetworkManager::Device.Vendor``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "global_network_id": global_network_id,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if model is not None:
            self._values["model"] = model
        if serial_number is not None:
            self._values["serial_number"] = serial_number
        if site_id is not None:
            self._values["site_id"] = site_id
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if vendor is not None:
            self._values["vendor"] = vendor

    @builtins.property
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::Device.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-globalnetworkid
        """
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[CfnDevice.LocationProperty, _IResolvable_6e2f5d88]]:
        """``AWS::NetworkManager::Device.Location``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-location
        """
        result = self._values.get("location")
        return result

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.Model``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-model
        """
        result = self._values.get("model")
        return result

    @builtins.property
    def serial_number(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.SerialNumber``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-serialnumber
        """
        result = self._values.get("serial_number")
        return result

    @builtins.property
    def site_id(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.SiteId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-siteid
        """
        result = self._values.get("site_id")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_c592b05a]]:
        """``AWS::NetworkManager::Device.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-type
        """
        result = self._values.get("type")
        return result

    @builtins.property
    def vendor(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Device.Vendor``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-vendor
        """
        result = self._values.get("vendor")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeviceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnGlobalNetwork(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnGlobalNetwork",
):
    """A CloudFormation ``AWS::NetworkManager::GlobalNetwork``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html
    :cloudformationResource: AWS::NetworkManager::GlobalNetwork
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
    ) -> None:
        """Create a new ``AWS::NetworkManager::GlobalNetwork``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::NetworkManager::GlobalNetwork.Description``.
        :param tags: ``AWS::NetworkManager::GlobalNetwork.Tags``.
        """
        props = CfnGlobalNetworkProps(description=description, tags=tags)

        jsii.create(CfnGlobalNetwork, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::NetworkManager::GlobalNetwork.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::GlobalNetwork.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnGlobalNetworkProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "tags": "tags"},
)
class CfnGlobalNetworkProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::NetworkManager::GlobalNetwork``.

        :param description: ``AWS::NetworkManager::GlobalNetwork.Description``.
        :param tags: ``AWS::NetworkManager::GlobalNetwork.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::GlobalNetwork.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_c592b05a]]:
        """``AWS::NetworkManager::GlobalNetwork.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGlobalNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnLink(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnLink",
):
    """A CloudFormation ``AWS::NetworkManager::Link``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html
    :cloudformationResource: AWS::NetworkManager::Link
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bandwidth: typing.Union["CfnLink.BandwidthProperty", _IResolvable_6e2f5d88],
        global_network_id: builtins.str,
        site_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        provider: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::NetworkManager::Link``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bandwidth: ``AWS::NetworkManager::Link.Bandwidth``.
        :param global_network_id: ``AWS::NetworkManager::Link.GlobalNetworkId``.
        :param site_id: ``AWS::NetworkManager::Link.SiteId``.
        :param description: ``AWS::NetworkManager::Link.Description``.
        :param provider: ``AWS::NetworkManager::Link.Provider``.
        :param tags: ``AWS::NetworkManager::Link.Tags``.
        :param type: ``AWS::NetworkManager::Link.Type``.
        """
        props = CfnLinkProps(
            bandwidth=bandwidth,
            global_network_id=global_network_id,
            site_id=site_id,
            description=description,
            provider=provider,
            tags=tags,
            type=type,
        )

        jsii.create(CfnLink, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrLinkArn")
    def attr_link_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: LinkArn
        """
        return jsii.get(self, "attrLinkArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrLinkId")
    def attr_link_id(self) -> builtins.str:
        """
        :cloudformationAttribute: LinkId
        """
        return jsii.get(self, "attrLinkId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::NetworkManager::Link.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(
        self,
    ) -> typing.Union["CfnLink.BandwidthProperty", _IResolvable_6e2f5d88]:
        """``AWS::NetworkManager::Link.Bandwidth``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-bandwidth
        """
        return jsii.get(self, "bandwidth")

    @bandwidth.setter # type: ignore
    def bandwidth(
        self,
        value: typing.Union["CfnLink.BandwidthProperty", _IResolvable_6e2f5d88],
    ) -> None:
        jsii.set(self, "bandwidth", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::Link.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter # type: ignore
    def global_network_id(self, value: builtins.str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="siteId")
    def site_id(self) -> builtins.str:
        """``AWS::NetworkManager::Link.SiteId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-siteid
        """
        return jsii.get(self, "siteId")

    @site_id.setter # type: ignore
    def site_id(self, value: builtins.str) -> None:
        jsii.set(self, "siteId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Link.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Link.Provider``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-provider
        """
        return jsii.get(self, "provider")

    @provider.setter # type: ignore
    def provider(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "provider", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Link.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "type", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_networkmanager.CfnLink.BandwidthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "download_speed": "downloadSpeed",
            "upload_speed": "uploadSpeed",
        },
    )
    class BandwidthProperty:
        def __init__(
            self,
            *,
            download_speed: typing.Optional[jsii.Number] = None,
            upload_speed: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param download_speed: ``CfnLink.BandwidthProperty.DownloadSpeed``.
            :param upload_speed: ``CfnLink.BandwidthProperty.UploadSpeed``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if download_speed is not None:
                self._values["download_speed"] = download_speed
            if upload_speed is not None:
                self._values["upload_speed"] = upload_speed

        @builtins.property
        def download_speed(self) -> typing.Optional[jsii.Number]:
            """``CfnLink.BandwidthProperty.DownloadSpeed``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html#cfn-networkmanager-link-bandwidth-downloadspeed
            """
            result = self._values.get("download_speed")
            return result

        @builtins.property
        def upload_speed(self) -> typing.Optional[jsii.Number]:
            """``CfnLink.BandwidthProperty.UploadSpeed``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html#cfn-networkmanager-link-bandwidth-uploadspeed
            """
            result = self._values.get("upload_speed")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BandwidthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_3eb0224c)
class CfnLinkAssociation(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnLinkAssociation",
):
    """A CloudFormation ``AWS::NetworkManager::LinkAssociation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html
    :cloudformationResource: AWS::NetworkManager::LinkAssociation
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        device_id: builtins.str,
        global_network_id: builtins.str,
        link_id: builtins.str,
    ) -> None:
        """Create a new ``AWS::NetworkManager::LinkAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param device_id: ``AWS::NetworkManager::LinkAssociation.DeviceId``.
        :param global_network_id: ``AWS::NetworkManager::LinkAssociation.GlobalNetworkId``.
        :param link_id: ``AWS::NetworkManager::LinkAssociation.LinkId``.
        """
        props = CfnLinkAssociationProps(
            device_id=device_id, global_network_id=global_network_id, link_id=link_id
        )

        jsii.create(CfnLinkAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        """``AWS::NetworkManager::LinkAssociation.DeviceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-deviceid
        """
        return jsii.get(self, "deviceId")

    @device_id.setter # type: ignore
    def device_id(self, value: builtins.str) -> None:
        jsii.set(self, "deviceId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::LinkAssociation.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter # type: ignore
    def global_network_id(self, value: builtins.str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="linkId")
    def link_id(self) -> builtins.str:
        """``AWS::NetworkManager::LinkAssociation.LinkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-linkid
        """
        return jsii.get(self, "linkId")

    @link_id.setter # type: ignore
    def link_id(self, value: builtins.str) -> None:
        jsii.set(self, "linkId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnLinkAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "device_id": "deviceId",
        "global_network_id": "globalNetworkId",
        "link_id": "linkId",
    },
)
class CfnLinkAssociationProps:
    def __init__(
        self,
        *,
        device_id: builtins.str,
        global_network_id: builtins.str,
        link_id: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::NetworkManager::LinkAssociation``.

        :param device_id: ``AWS::NetworkManager::LinkAssociation.DeviceId``.
        :param global_network_id: ``AWS::NetworkManager::LinkAssociation.GlobalNetworkId``.
        :param link_id: ``AWS::NetworkManager::LinkAssociation.LinkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "device_id": device_id,
            "global_network_id": global_network_id,
            "link_id": link_id,
        }

    @builtins.property
    def device_id(self) -> builtins.str:
        """``AWS::NetworkManager::LinkAssociation.DeviceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-deviceid
        """
        result = self._values.get("device_id")
        assert result is not None, "Required property 'device_id' is missing"
        return result

    @builtins.property
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::LinkAssociation.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-globalnetworkid
        """
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return result

    @builtins.property
    def link_id(self) -> builtins.str:
        """``AWS::NetworkManager::LinkAssociation.LinkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-linkid
        """
        result = self._values.get("link_id")
        assert result is not None, "Required property 'link_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLinkAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnLinkProps",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth": "bandwidth",
        "global_network_id": "globalNetworkId",
        "site_id": "siteId",
        "description": "description",
        "provider": "provider",
        "tags": "tags",
        "type": "type",
    },
)
class CfnLinkProps:
    def __init__(
        self,
        *,
        bandwidth: typing.Union[CfnLink.BandwidthProperty, _IResolvable_6e2f5d88],
        global_network_id: builtins.str,
        site_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        provider: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::NetworkManager::Link``.

        :param bandwidth: ``AWS::NetworkManager::Link.Bandwidth``.
        :param global_network_id: ``AWS::NetworkManager::Link.GlobalNetworkId``.
        :param site_id: ``AWS::NetworkManager::Link.SiteId``.
        :param description: ``AWS::NetworkManager::Link.Description``.
        :param provider: ``AWS::NetworkManager::Link.Provider``.
        :param tags: ``AWS::NetworkManager::Link.Tags``.
        :param type: ``AWS::NetworkManager::Link.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "bandwidth": bandwidth,
            "global_network_id": global_network_id,
            "site_id": site_id,
        }
        if description is not None:
            self._values["description"] = description
        if provider is not None:
            self._values["provider"] = provider
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def bandwidth(
        self,
    ) -> typing.Union[CfnLink.BandwidthProperty, _IResolvable_6e2f5d88]:
        """``AWS::NetworkManager::Link.Bandwidth``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-bandwidth
        """
        result = self._values.get("bandwidth")
        assert result is not None, "Required property 'bandwidth' is missing"
        return result

    @builtins.property
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::Link.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-globalnetworkid
        """
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return result

    @builtins.property
    def site_id(self) -> builtins.str:
        """``AWS::NetworkManager::Link.SiteId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-siteid
        """
        result = self._values.get("site_id")
        assert result is not None, "Required property 'site_id' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Link.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def provider(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Link.Provider``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-provider
        """
        result = self._values.get("provider")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_c592b05a]]:
        """``AWS::NetworkManager::Link.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Link.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-type
        """
        result = self._values.get("type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLinkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnSite(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnSite",
):
    """A CloudFormation ``AWS::NetworkManager::Site``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html
    :cloudformationResource: AWS::NetworkManager::Site
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        global_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union["CfnSite.LocationProperty", _IResolvable_6e2f5d88]] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
    ) -> None:
        """Create a new ``AWS::NetworkManager::Site``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param global_network_id: ``AWS::NetworkManager::Site.GlobalNetworkId``.
        :param description: ``AWS::NetworkManager::Site.Description``.
        :param location: ``AWS::NetworkManager::Site.Location``.
        :param tags: ``AWS::NetworkManager::Site.Tags``.
        """
        props = CfnSiteProps(
            global_network_id=global_network_id,
            description=description,
            location=location,
            tags=tags,
        )

        jsii.create(CfnSite, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrSiteArn")
    def attr_site_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: SiteArn
        """
        return jsii.get(self, "attrSiteArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrSiteId")
    def attr_site_id(self) -> builtins.str:
        """
        :cloudformationAttribute: SiteId
        """
        return jsii.get(self, "attrSiteId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::NetworkManager::Site.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::Site.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter # type: ignore
    def global_network_id(self, value: builtins.str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Site.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="location")
    def location(
        self,
    ) -> typing.Optional[typing.Union["CfnSite.LocationProperty", _IResolvable_6e2f5d88]]:
        """``AWS::NetworkManager::Site.Location``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-location
        """
        return jsii.get(self, "location")

    @location.setter # type: ignore
    def location(
        self,
        value: typing.Optional[typing.Union["CfnSite.LocationProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "location", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_networkmanager.CfnSite.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address": "address",
            "latitude": "latitude",
            "longitude": "longitude",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            latitude: typing.Optional[builtins.str] = None,
            longitude: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param address: ``CfnSite.LocationProperty.Address``.
            :param latitude: ``CfnSite.LocationProperty.Latitude``.
            :param longitude: ``CfnSite.LocationProperty.Longitude``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if latitude is not None:
                self._values["latitude"] = latitude
            if longitude is not None:
                self._values["longitude"] = longitude

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            """``CfnSite.LocationProperty.Address``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-address
            """
            result = self._values.get("address")
            return result

        @builtins.property
        def latitude(self) -> typing.Optional[builtins.str]:
            """``CfnSite.LocationProperty.Latitude``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-latitude
            """
            result = self._values.get("latitude")
            return result

        @builtins.property
        def longitude(self) -> typing.Optional[builtins.str]:
            """``CfnSite.LocationProperty.Longitude``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-longitude
            """
            result = self._values.get("longitude")
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
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnSiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "global_network_id": "globalNetworkId",
        "description": "description",
        "location": "location",
        "tags": "tags",
    },
)
class CfnSiteProps:
    def __init__(
        self,
        *,
        global_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[CfnSite.LocationProperty, _IResolvable_6e2f5d88]] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::NetworkManager::Site``.

        :param global_network_id: ``AWS::NetworkManager::Site.GlobalNetworkId``.
        :param description: ``AWS::NetworkManager::Site.Description``.
        :param location: ``AWS::NetworkManager::Site.Location``.
        :param tags: ``AWS::NetworkManager::Site.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "global_network_id": global_network_id,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::Site.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-globalnetworkid
        """
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkManager::Site.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[CfnSite.LocationProperty, _IResolvable_6e2f5d88]]:
        """``AWS::NetworkManager::Site.Location``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-location
        """
        result = self._values.get("location")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_c592b05a]]:
        """``AWS::NetworkManager::Site.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnTransitGatewayRegistration(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnTransitGatewayRegistration",
):
    """A CloudFormation ``AWS::NetworkManager::TransitGatewayRegistration``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html
    :cloudformationResource: AWS::NetworkManager::TransitGatewayRegistration
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        global_network_id: builtins.str,
        transit_gateway_arn: builtins.str,
    ) -> None:
        """Create a new ``AWS::NetworkManager::TransitGatewayRegistration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param global_network_id: ``AWS::NetworkManager::TransitGatewayRegistration.GlobalNetworkId``.
        :param transit_gateway_arn: ``AWS::NetworkManager::TransitGatewayRegistration.TransitGatewayArn``.
        """
        props = CfnTransitGatewayRegistrationProps(
            global_network_id=global_network_id,
            transit_gateway_arn=transit_gateway_arn,
        )

        jsii.create(CfnTransitGatewayRegistration, self, [scope, id, props])

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
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::TransitGatewayRegistration.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-globalnetworkid
        """
        return jsii.get(self, "globalNetworkId")

    @global_network_id.setter # type: ignore
    def global_network_id(self, value: builtins.str) -> None:
        jsii.set(self, "globalNetworkId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="transitGatewayArn")
    def transit_gateway_arn(self) -> builtins.str:
        """``AWS::NetworkManager::TransitGatewayRegistration.TransitGatewayArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-transitgatewayarn
        """
        return jsii.get(self, "transitGatewayArn")

    @transit_gateway_arn.setter # type: ignore
    def transit_gateway_arn(self, value: builtins.str) -> None:
        jsii.set(self, "transitGatewayArn", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networkmanager.CfnTransitGatewayRegistrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "global_network_id": "globalNetworkId",
        "transit_gateway_arn": "transitGatewayArn",
    },
)
class CfnTransitGatewayRegistrationProps:
    def __init__(
        self,
        *,
        global_network_id: builtins.str,
        transit_gateway_arn: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::NetworkManager::TransitGatewayRegistration``.

        :param global_network_id: ``AWS::NetworkManager::TransitGatewayRegistration.GlobalNetworkId``.
        :param transit_gateway_arn: ``AWS::NetworkManager::TransitGatewayRegistration.TransitGatewayArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "global_network_id": global_network_id,
            "transit_gateway_arn": transit_gateway_arn,
        }

    @builtins.property
    def global_network_id(self) -> builtins.str:
        """``AWS::NetworkManager::TransitGatewayRegistration.GlobalNetworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-globalnetworkid
        """
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return result

    @builtins.property
    def transit_gateway_arn(self) -> builtins.str:
        """``AWS::NetworkManager::TransitGatewayRegistration.TransitGatewayArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-transitgatewayarn
        """
        result = self._values.get("transit_gateway_arn")
        assert result is not None, "Required property 'transit_gateway_arn' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTransitGatewayRegistrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCustomerGatewayAssociation",
    "CfnCustomerGatewayAssociationProps",
    "CfnDevice",
    "CfnDeviceProps",
    "CfnGlobalNetwork",
    "CfnGlobalNetworkProps",
    "CfnLink",
    "CfnLinkAssociation",
    "CfnLinkAssociationProps",
    "CfnLinkProps",
    "CfnSite",
    "CfnSiteProps",
    "CfnTransitGatewayRegistration",
    "CfnTransitGatewayRegistrationProps",
]

publication.publish()
