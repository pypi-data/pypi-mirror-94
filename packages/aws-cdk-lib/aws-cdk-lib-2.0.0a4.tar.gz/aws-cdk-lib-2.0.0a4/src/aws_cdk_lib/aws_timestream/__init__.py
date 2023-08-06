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
    TagManager as _TagManager_6a5badd9,
    TreeInspector as _TreeInspector_afbbf916,
)


@jsii.implements(_IInspectable_3eb0224c)
class CfnDatabase(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_timestream.CfnDatabase",
):
    """A CloudFormation ``AWS::Timestream::Database``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html
    :cloudformationResource: AWS::Timestream::Database
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        database_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
    ) -> None:
        """Create a new ``AWS::Timestream::Database``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database_name: ``AWS::Timestream::Database.DatabaseName``.
        :param kms_key_id: ``AWS::Timestream::Database.KmsKeyId``.
        :param tags: ``AWS::Timestream::Database.Tags``.
        """
        props = CfnDatabaseProps(
            database_name=database_name, kms_key_id=kms_key_id, tags=tags
        )

        jsii.create(CfnDatabase, self, [scope, id, props])

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
        """``AWS::Timestream::Database.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Timestream::Database.DatabaseName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-databasename
        """
        return jsii.get(self, "databaseName")

    @database_name.setter # type: ignore
    def database_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "databaseName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Timestream::Database.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter # type: ignore
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_timestream.CfnDatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "kms_key_id": "kmsKeyId",
        "tags": "tags",
    },
)
class CfnDatabaseProps:
    def __init__(
        self,
        *,
        database_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Timestream::Database``.

        :param database_name: ``AWS::Timestream::Database.DatabaseName``.
        :param kms_key_id: ``AWS::Timestream::Database.KmsKeyId``.
        :param tags: ``AWS::Timestream::Database.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if database_name is not None:
            self._values["database_name"] = database_name
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Timestream::Database.DatabaseName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-databasename
        """
        result = self._values.get("database_name")
        return result

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Timestream::Database.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-kmskeyid
        """
        result = self._values.get("kms_key_id")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_c592b05a]]:
        """``AWS::Timestream::Database.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnTable(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_timestream.CfnTable",
):
    """A CloudFormation ``AWS::Timestream::Table``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html
    :cloudformationResource: AWS::Timestream::Table
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        database_name: builtins.str,
        retention_properties: typing.Any = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
    ) -> None:
        """Create a new ``AWS::Timestream::Table``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database_name: ``AWS::Timestream::Table.DatabaseName``.
        :param retention_properties: ``AWS::Timestream::Table.RetentionProperties``.
        :param table_name: ``AWS::Timestream::Table.TableName``.
        :param tags: ``AWS::Timestream::Table.Tags``.
        """
        props = CfnTableProps(
            database_name=database_name,
            retention_properties=retention_properties,
            table_name=table_name,
            tags=tags,
        )

        jsii.create(CfnTable, self, [scope, id, props])

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
        """``AWS::Timestream::Table.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        """``AWS::Timestream::Table.DatabaseName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-databasename
        """
        return jsii.get(self, "databaseName")

    @database_name.setter # type: ignore
    def database_name(self, value: builtins.str) -> None:
        jsii.set(self, "databaseName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="retentionProperties")
    def retention_properties(self) -> typing.Any:
        """``AWS::Timestream::Table.RetentionProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-retentionproperties
        """
        return jsii.get(self, "retentionProperties")

    @retention_properties.setter # type: ignore
    def retention_properties(self, value: typing.Any) -> None:
        jsii.set(self, "retentionProperties", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Timestream::Table.TableName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tablename
        """
        return jsii.get(self, "tableName")

    @table_name.setter # type: ignore
    def table_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tableName", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_timestream.CfnTableProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "retention_properties": "retentionProperties",
        "table_name": "tableName",
        "tags": "tags",
    },
)
class CfnTableProps:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        retention_properties: typing.Any = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Timestream::Table``.

        :param database_name: ``AWS::Timestream::Table.DatabaseName``.
        :param retention_properties: ``AWS::Timestream::Table.RetentionProperties``.
        :param table_name: ``AWS::Timestream::Table.TableName``.
        :param tags: ``AWS::Timestream::Table.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "database_name": database_name,
        }
        if retention_properties is not None:
            self._values["retention_properties"] = retention_properties
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def database_name(self) -> builtins.str:
        """``AWS::Timestream::Table.DatabaseName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-databasename
        """
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return result

    @builtins.property
    def retention_properties(self) -> typing.Any:
        """``AWS::Timestream::Table.RetentionProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-retentionproperties
        """
        result = self._values.get("retention_properties")
        return result

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Timestream::Table.TableName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tablename
        """
        result = self._values.get("table_name")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_c592b05a]]:
        """``AWS::Timestream::Table.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDatabase",
    "CfnDatabaseProps",
    "CfnTable",
    "CfnTableProps",
]

publication.publish()
