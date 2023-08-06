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
    TreeInspector as _TreeInspector_afbbf916,
)


@jsii.implements(_IInspectable_3eb0224c)
class CfnEnvironment(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironment",
):
    """A CloudFormation ``AWS::MWAA::Environment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html
    :cloudformationResource: AWS::MWAA::Environment
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        airflow_configuration_options: typing.Optional[typing.Union["CfnEnvironment.AirflowConfigurationOptionsProperty", _IResolvable_6e2f5d88]] = None,
        airflow_version: typing.Optional[builtins.str] = None,
        dag_s3_path: typing.Optional[builtins.str] = None,
        environment_class: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union["CfnEnvironment.LoggingConfigurationProperty", _IResolvable_6e2f5d88]] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        network_configuration: typing.Optional[typing.Union["CfnEnvironment.NetworkConfigurationProperty", _IResolvable_6e2f5d88]] = None,
        plugins_s3_object_version: typing.Optional[builtins.str] = None,
        plugins_s3_path: typing.Optional[builtins.str] = None,
        requirements_s3_object_version: typing.Optional[builtins.str] = None,
        requirements_s3_path: typing.Optional[builtins.str] = None,
        source_bucket_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional["CfnEnvironment.TagMapProperty"] = None,
        webserver_access_mode: typing.Optional[builtins.str] = None,
        webserver_url: typing.Optional[builtins.str] = None,
        weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::MWAA::Environment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param airflow_configuration_options: ``AWS::MWAA::Environment.AirflowConfigurationOptions``.
        :param airflow_version: ``AWS::MWAA::Environment.AirflowVersion``.
        :param dag_s3_path: ``AWS::MWAA::Environment.DagS3Path``.
        :param environment_class: ``AWS::MWAA::Environment.EnvironmentClass``.
        :param execution_role_arn: ``AWS::MWAA::Environment.ExecutionRoleArn``.
        :param kms_key: ``AWS::MWAA::Environment.KmsKey``.
        :param logging_configuration: ``AWS::MWAA::Environment.LoggingConfiguration``.
        :param max_workers: ``AWS::MWAA::Environment.MaxWorkers``.
        :param network_configuration: ``AWS::MWAA::Environment.NetworkConfiguration``.
        :param plugins_s3_object_version: ``AWS::MWAA::Environment.PluginsS3ObjectVersion``.
        :param plugins_s3_path: ``AWS::MWAA::Environment.PluginsS3Path``.
        :param requirements_s3_object_version: ``AWS::MWAA::Environment.RequirementsS3ObjectVersion``.
        :param requirements_s3_path: ``AWS::MWAA::Environment.RequirementsS3Path``.
        :param source_bucket_arn: ``AWS::MWAA::Environment.SourceBucketArn``.
        :param tags: ``AWS::MWAA::Environment.Tags``.
        :param webserver_access_mode: ``AWS::MWAA::Environment.WebserverAccessMode``.
        :param webserver_url: ``AWS::MWAA::Environment.WebserverUrl``.
        :param weekly_maintenance_window_start: ``AWS::MWAA::Environment.WeeklyMaintenanceWindowStart``.
        """
        props = CfnEnvironmentProps(
            airflow_configuration_options=airflow_configuration_options,
            airflow_version=airflow_version,
            dag_s3_path=dag_s3_path,
            environment_class=environment_class,
            execution_role_arn=execution_role_arn,
            kms_key=kms_key,
            logging_configuration=logging_configuration,
            max_workers=max_workers,
            network_configuration=network_configuration,
            plugins_s3_object_version=plugins_s3_object_version,
            plugins_s3_path=plugins_s3_path,
            requirements_s3_object_version=requirements_s3_object_version,
            requirements_s3_path=requirements_s3_path,
            source_bucket_arn=source_bucket_arn,
            tags=tags,
            webserver_access_mode=webserver_access_mode,
            webserver_url=webserver_url,
            weekly_maintenance_window_start=weekly_maintenance_window_start,
        )

        jsii.create(CfnEnvironment, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        """
        :cloudformationAttribute: CreatedAt
        """
        return jsii.get(self, "attrCreatedAt")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        """
        :cloudformationAttribute: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrServiceRoleArn")
    def attr_service_role_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: ServiceRoleArn
        """
        return jsii.get(self, "attrServiceRoleArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        """
        :cloudformationAttribute: Status
        """
        return jsii.get(self, "attrStatus")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="airflowConfigurationOptions")
    def airflow_configuration_options(
        self,
    ) -> typing.Optional[typing.Union["CfnEnvironment.AirflowConfigurationOptionsProperty", _IResolvable_6e2f5d88]]:
        """``AWS::MWAA::Environment.AirflowConfigurationOptions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-airflowconfigurationoptions
        """
        return jsii.get(self, "airflowConfigurationOptions")

    @airflow_configuration_options.setter # type: ignore
    def airflow_configuration_options(
        self,
        value: typing.Optional[typing.Union["CfnEnvironment.AirflowConfigurationOptionsProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "airflowConfigurationOptions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="airflowVersion")
    def airflow_version(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.AirflowVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-airflowversion
        """
        return jsii.get(self, "airflowVersion")

    @airflow_version.setter # type: ignore
    def airflow_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "airflowVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dagS3Path")
    def dag_s3_path(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.DagS3Path``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-dags3path
        """
        return jsii.get(self, "dagS3Path")

    @dag_s3_path.setter # type: ignore
    def dag_s3_path(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dagS3Path", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="environmentClass")
    def environment_class(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.EnvironmentClass``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-environmentclass
        """
        return jsii.get(self, "environmentClass")

    @environment_class.setter # type: ignore
    def environment_class(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "environmentClass", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.ExecutionRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-executionrolearn
        """
        return jsii.get(self, "executionRoleArn")

    @execution_role_arn.setter # type: ignore
    def execution_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "executionRoleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.KmsKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-kmskey
        """
        return jsii.get(self, "kmsKey")

    @kms_key.setter # type: ignore
    def kms_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnEnvironment.LoggingConfigurationProperty", _IResolvable_6e2f5d88]]:
        """``AWS::MWAA::Environment.LoggingConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-loggingconfiguration
        """
        return jsii.get(self, "loggingConfiguration")

    @logging_configuration.setter # type: ignore
    def logging_configuration(
        self,
        value: typing.Optional[typing.Union["CfnEnvironment.LoggingConfigurationProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "loggingConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxWorkers")
    def max_workers(self) -> typing.Optional[jsii.Number]:
        """``AWS::MWAA::Environment.MaxWorkers``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-maxworkers
        """
        return jsii.get(self, "maxWorkers")

    @max_workers.setter # type: ignore
    def max_workers(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxWorkers", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnEnvironment.NetworkConfigurationProperty", _IResolvable_6e2f5d88]]:
        """``AWS::MWAA::Environment.NetworkConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-networkconfiguration
        """
        return jsii.get(self, "networkConfiguration")

    @network_configuration.setter # type: ignore
    def network_configuration(
        self,
        value: typing.Optional[typing.Union["CfnEnvironment.NetworkConfigurationProperty", _IResolvable_6e2f5d88]],
    ) -> None:
        jsii.set(self, "networkConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pluginsS3ObjectVersion")
    def plugins_s3_object_version(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.PluginsS3ObjectVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-pluginss3objectversion
        """
        return jsii.get(self, "pluginsS3ObjectVersion")

    @plugins_s3_object_version.setter # type: ignore
    def plugins_s3_object_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "pluginsS3ObjectVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pluginsS3Path")
    def plugins_s3_path(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.PluginsS3Path``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-pluginss3path
        """
        return jsii.get(self, "pluginsS3Path")

    @plugins_s3_path.setter # type: ignore
    def plugins_s3_path(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "pluginsS3Path", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="requirementsS3ObjectVersion")
    def requirements_s3_object_version(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.RequirementsS3ObjectVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-requirementss3objectversion
        """
        return jsii.get(self, "requirementsS3ObjectVersion")

    @requirements_s3_object_version.setter # type: ignore
    def requirements_s3_object_version(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "requirementsS3ObjectVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="requirementsS3Path")
    def requirements_s3_path(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.RequirementsS3Path``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-requirementss3path
        """
        return jsii.get(self, "requirementsS3Path")

    @requirements_s3_path.setter # type: ignore
    def requirements_s3_path(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "requirementsS3Path", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceBucketArn")
    def source_bucket_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.SourceBucketArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-sourcebucketarn
        """
        return jsii.get(self, "sourceBucketArn")

    @source_bucket_arn.setter # type: ignore
    def source_bucket_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sourceBucketArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional["CfnEnvironment.TagMapProperty"]:
        """``AWS::MWAA::Environment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-tags
        """
        return jsii.get(self, "tags")

    @tags.setter # type: ignore
    def tags(self, value: typing.Optional["CfnEnvironment.TagMapProperty"]) -> None:
        jsii.set(self, "tags", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="webserverAccessMode")
    def webserver_access_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.WebserverAccessMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-webserveraccessmode
        """
        return jsii.get(self, "webserverAccessMode")

    @webserver_access_mode.setter # type: ignore
    def webserver_access_mode(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "webserverAccessMode", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="webserverUrl")
    def webserver_url(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.WebserverUrl``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-webserverurl
        """
        return jsii.get(self, "webserverUrl")

    @webserver_url.setter # type: ignore
    def webserver_url(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "webserverUrl", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="weeklyMaintenanceWindowStart")
    def weekly_maintenance_window_start(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.WeeklyMaintenanceWindowStart``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-weeklymaintenancewindowstart
        """
        return jsii.get(self, "weeklyMaintenanceWindowStart")

    @weekly_maintenance_window_start.setter # type: ignore
    def weekly_maintenance_window_start(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "weeklyMaintenanceWindowStart", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironment.AirflowConfigurationOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class AirflowConfigurationOptionsProperty:
        def __init__(self) -> None:
            """
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-airflowconfigurationoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AirflowConfigurationOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironment.LastUpdateProperty",
        jsii_struct_bases=[],
        name_mapping={"created_at": "createdAt", "error": "error", "status": "status"},
    )
    class LastUpdateProperty:
        def __init__(
            self,
            *,
            created_at: typing.Optional[builtins.str] = None,
            error: typing.Optional[typing.Union["CfnEnvironment.UpdateErrorProperty", _IResolvable_6e2f5d88]] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param created_at: ``CfnEnvironment.LastUpdateProperty.CreatedAt``.
            :param error: ``CfnEnvironment.LastUpdateProperty.Error``.
            :param status: ``CfnEnvironment.LastUpdateProperty.Status``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-lastupdate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if created_at is not None:
                self._values["created_at"] = created_at
            if error is not None:
                self._values["error"] = error
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def created_at(self) -> typing.Optional[builtins.str]:
            """``CfnEnvironment.LastUpdateProperty.CreatedAt``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-lastupdate.html#cfn-mwaa-environment-lastupdate-createdat
            """
            result = self._values.get("created_at")
            return result

        @builtins.property
        def error(
            self,
        ) -> typing.Optional[typing.Union["CfnEnvironment.UpdateErrorProperty", _IResolvable_6e2f5d88]]:
            """``CfnEnvironment.LastUpdateProperty.Error``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-lastupdate.html#cfn-mwaa-environment-lastupdate-error
            """
            result = self._values.get("error")
            return result

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            """``CfnEnvironment.LastUpdateProperty.Status``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-lastupdate.html#cfn-mwaa-environment-lastupdate-status
            """
            result = self._values.get("status")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LastUpdateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironment.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dag_processing_logs": "dagProcessingLogs",
            "scheduler_logs": "schedulerLogs",
            "task_logs": "taskLogs",
            "webserver_logs": "webserverLogs",
            "worker_logs": "workerLogs",
        },
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            dag_processing_logs: typing.Optional[typing.Union["CfnEnvironment.ModuleLoggingConfigurationProperty", _IResolvable_6e2f5d88]] = None,
            scheduler_logs: typing.Optional[typing.Union["CfnEnvironment.ModuleLoggingConfigurationProperty", _IResolvable_6e2f5d88]] = None,
            task_logs: typing.Optional[typing.Union["CfnEnvironment.ModuleLoggingConfigurationProperty", _IResolvable_6e2f5d88]] = None,
            webserver_logs: typing.Optional[typing.Union["CfnEnvironment.ModuleLoggingConfigurationProperty", _IResolvable_6e2f5d88]] = None,
            worker_logs: typing.Optional[typing.Union["CfnEnvironment.ModuleLoggingConfigurationProperty", _IResolvable_6e2f5d88]] = None,
        ) -> None:
            """
            :param dag_processing_logs: ``CfnEnvironment.LoggingConfigurationProperty.DagProcessingLogs``.
            :param scheduler_logs: ``CfnEnvironment.LoggingConfigurationProperty.SchedulerLogs``.
            :param task_logs: ``CfnEnvironment.LoggingConfigurationProperty.TaskLogs``.
            :param webserver_logs: ``CfnEnvironment.LoggingConfigurationProperty.WebserverLogs``.
            :param worker_logs: ``CfnEnvironment.LoggingConfigurationProperty.WorkerLogs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if dag_processing_logs is not None:
                self._values["dag_processing_logs"] = dag_processing_logs
            if scheduler_logs is not None:
                self._values["scheduler_logs"] = scheduler_logs
            if task_logs is not None:
                self._values["task_logs"] = task_logs
            if webserver_logs is not None:
                self._values["webserver_logs"] = webserver_logs
            if worker_logs is not None:
                self._values["worker_logs"] = worker_logs

        @builtins.property
        def dag_processing_logs(
            self,
        ) -> typing.Optional[typing.Union["CfnEnvironment.ModuleLoggingConfigurationProperty", _IResolvable_6e2f5d88]]:
            """``CfnEnvironment.LoggingConfigurationProperty.DagProcessingLogs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html#cfn-mwaa-environment-loggingconfiguration-dagprocessinglogs
            """
            result = self._values.get("dag_processing_logs")
            return result

        @builtins.property
        def scheduler_logs(
            self,
        ) -> typing.Optional[typing.Union["CfnEnvironment.ModuleLoggingConfigurationProperty", _IResolvable_6e2f5d88]]:
            """``CfnEnvironment.LoggingConfigurationProperty.SchedulerLogs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html#cfn-mwaa-environment-loggingconfiguration-schedulerlogs
            """
            result = self._values.get("scheduler_logs")
            return result

        @builtins.property
        def task_logs(
            self,
        ) -> typing.Optional[typing.Union["CfnEnvironment.ModuleLoggingConfigurationProperty", _IResolvable_6e2f5d88]]:
            """``CfnEnvironment.LoggingConfigurationProperty.TaskLogs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html#cfn-mwaa-environment-loggingconfiguration-tasklogs
            """
            result = self._values.get("task_logs")
            return result

        @builtins.property
        def webserver_logs(
            self,
        ) -> typing.Optional[typing.Union["CfnEnvironment.ModuleLoggingConfigurationProperty", _IResolvable_6e2f5d88]]:
            """``CfnEnvironment.LoggingConfigurationProperty.WebserverLogs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html#cfn-mwaa-environment-loggingconfiguration-webserverlogs
            """
            result = self._values.get("webserver_logs")
            return result

        @builtins.property
        def worker_logs(
            self,
        ) -> typing.Optional[typing.Union["CfnEnvironment.ModuleLoggingConfigurationProperty", _IResolvable_6e2f5d88]]:
            """``CfnEnvironment.LoggingConfigurationProperty.WorkerLogs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-loggingconfiguration.html#cfn-mwaa-environment-loggingconfiguration-workerlogs
            """
            result = self._values.get("worker_logs")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
            "enabled": "enabled",
            "log_level": "logLevel",
        },
    )
    class ModuleLoggingConfigurationProperty:
        def __init__(
            self,
            *,
            cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
            log_level: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param cloud_watch_log_group_arn: ``CfnEnvironment.ModuleLoggingConfigurationProperty.CloudWatchLogGroupArn``.
            :param enabled: ``CfnEnvironment.ModuleLoggingConfigurationProperty.Enabled``.
            :param log_level: ``CfnEnvironment.ModuleLoggingConfigurationProperty.LogLevel``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-moduleloggingconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if cloud_watch_log_group_arn is not None:
                self._values["cloud_watch_log_group_arn"] = cloud_watch_log_group_arn
            if enabled is not None:
                self._values["enabled"] = enabled
            if log_level is not None:
                self._values["log_level"] = log_level

        @builtins.property
        def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
            """``CfnEnvironment.ModuleLoggingConfigurationProperty.CloudWatchLogGroupArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-moduleloggingconfiguration.html#cfn-mwaa-environment-moduleloggingconfiguration-cloudwatchloggrouparn
            """
            result = self._values.get("cloud_watch_log_group_arn")
            return result

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
            """``CfnEnvironment.ModuleLoggingConfigurationProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-moduleloggingconfiguration.html#cfn-mwaa-environment-moduleloggingconfiguration-enabled
            """
            result = self._values.get("enabled")
            return result

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            """``CfnEnvironment.ModuleLoggingConfigurationProperty.LogLevel``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-moduleloggingconfiguration.html#cfn-mwaa-environment-moduleloggingconfiguration-loglevel
            """
            result = self._values.get("log_level")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ModuleLoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironment.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Union["CfnEnvironment.SecurityGroupListProperty", _IResolvable_6e2f5d88]] = None,
            subnet_ids: typing.Optional[typing.Union["CfnEnvironment.SubnetListProperty", _IResolvable_6e2f5d88]] = None,
        ) -> None:
            """
            :param security_group_ids: ``CfnEnvironment.NetworkConfigurationProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnEnvironment.NetworkConfigurationProperty.SubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-networkconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(
            self,
        ) -> typing.Optional[typing.Union["CfnEnvironment.SecurityGroupListProperty", _IResolvable_6e2f5d88]]:
            """``CfnEnvironment.NetworkConfigurationProperty.SecurityGroupIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-networkconfiguration.html#cfn-mwaa-environment-networkconfiguration-securitygroupids
            """
            result = self._values.get("security_group_ids")
            return result

        @builtins.property
        def subnet_ids(
            self,
        ) -> typing.Optional[typing.Union["CfnEnvironment.SubnetListProperty", _IResolvable_6e2f5d88]]:
            """``CfnEnvironment.NetworkConfigurationProperty.SubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-networkconfiguration.html#cfn-mwaa-environment-networkconfiguration-subnetids
            """
            result = self._values.get("subnet_ids")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironment.SecurityGroupListProperty",
        jsii_struct_bases=[],
        name_mapping={"security_group_list": "securityGroupList"},
    )
    class SecurityGroupListProperty:
        def __init__(
            self,
            *,
            security_group_list: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param security_group_list: ``CfnEnvironment.SecurityGroupListProperty.SecurityGroupList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-securitygrouplist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if security_group_list is not None:
                self._values["security_group_list"] = security_group_list

        @builtins.property
        def security_group_list(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnEnvironment.SecurityGroupListProperty.SecurityGroupList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-securitygrouplist.html#cfn-mwaa-environment-securitygrouplist-securitygrouplist
            """
            result = self._values.get("security_group_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecurityGroupListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironment.SubnetListProperty",
        jsii_struct_bases=[],
        name_mapping={"subnet_list": "subnetList"},
    )
    class SubnetListProperty:
        def __init__(
            self,
            *,
            subnet_list: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param subnet_list: ``CfnEnvironment.SubnetListProperty.SubnetList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-subnetlist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if subnet_list is not None:
                self._values["subnet_list"] = subnet_list

        @builtins.property
        def subnet_list(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnEnvironment.SubnetListProperty.SubnetList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-subnetlist.html#cfn-mwaa-environment-subnetlist-subnetlist
            """
            result = self._values.get("subnet_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubnetListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironment.TagMapProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class TagMapProperty:
        def __init__(self) -> None:
            """
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-tagmap.html
            """
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironment.UpdateErrorProperty",
        jsii_struct_bases=[],
        name_mapping={"error_code": "errorCode", "error_message": "errorMessage"},
    )
    class UpdateErrorProperty:
        def __init__(
            self,
            *,
            error_code: typing.Optional[builtins.str] = None,
            error_message: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param error_code: ``CfnEnvironment.UpdateErrorProperty.ErrorCode``.
            :param error_message: ``CfnEnvironment.UpdateErrorProperty.ErrorMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-updateerror.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if error_code is not None:
                self._values["error_code"] = error_code
            if error_message is not None:
                self._values["error_message"] = error_message

        @builtins.property
        def error_code(self) -> typing.Optional[builtins.str]:
            """``CfnEnvironment.UpdateErrorProperty.ErrorCode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-updateerror.html#cfn-mwaa-environment-updateerror-errorcode
            """
            result = self._values.get("error_code")
            return result

        @builtins.property
        def error_message(self) -> typing.Optional[builtins.str]:
            """``CfnEnvironment.UpdateErrorProperty.ErrorMessage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mwaa-environment-updateerror.html#cfn-mwaa-environment-updateerror-errormessage
            """
            result = self._values.get("error_message")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpdateErrorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_mwaa.CfnEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "airflow_configuration_options": "airflowConfigurationOptions",
        "airflow_version": "airflowVersion",
        "dag_s3_path": "dagS3Path",
        "environment_class": "environmentClass",
        "execution_role_arn": "executionRoleArn",
        "kms_key": "kmsKey",
        "logging_configuration": "loggingConfiguration",
        "max_workers": "maxWorkers",
        "network_configuration": "networkConfiguration",
        "plugins_s3_object_version": "pluginsS3ObjectVersion",
        "plugins_s3_path": "pluginsS3Path",
        "requirements_s3_object_version": "requirementsS3ObjectVersion",
        "requirements_s3_path": "requirementsS3Path",
        "source_bucket_arn": "sourceBucketArn",
        "tags": "tags",
        "webserver_access_mode": "webserverAccessMode",
        "webserver_url": "webserverUrl",
        "weekly_maintenance_window_start": "weeklyMaintenanceWindowStart",
    },
)
class CfnEnvironmentProps:
    def __init__(
        self,
        *,
        airflow_configuration_options: typing.Optional[typing.Union[CfnEnvironment.AirflowConfigurationOptionsProperty, _IResolvable_6e2f5d88]] = None,
        airflow_version: typing.Optional[builtins.str] = None,
        dag_s3_path: typing.Optional[builtins.str] = None,
        environment_class: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union[CfnEnvironment.LoggingConfigurationProperty, _IResolvable_6e2f5d88]] = None,
        max_workers: typing.Optional[jsii.Number] = None,
        network_configuration: typing.Optional[typing.Union[CfnEnvironment.NetworkConfigurationProperty, _IResolvable_6e2f5d88]] = None,
        plugins_s3_object_version: typing.Optional[builtins.str] = None,
        plugins_s3_path: typing.Optional[builtins.str] = None,
        requirements_s3_object_version: typing.Optional[builtins.str] = None,
        requirements_s3_path: typing.Optional[builtins.str] = None,
        source_bucket_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[CfnEnvironment.TagMapProperty] = None,
        webserver_access_mode: typing.Optional[builtins.str] = None,
        webserver_url: typing.Optional[builtins.str] = None,
        weekly_maintenance_window_start: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::MWAA::Environment``.

        :param airflow_configuration_options: ``AWS::MWAA::Environment.AirflowConfigurationOptions``.
        :param airflow_version: ``AWS::MWAA::Environment.AirflowVersion``.
        :param dag_s3_path: ``AWS::MWAA::Environment.DagS3Path``.
        :param environment_class: ``AWS::MWAA::Environment.EnvironmentClass``.
        :param execution_role_arn: ``AWS::MWAA::Environment.ExecutionRoleArn``.
        :param kms_key: ``AWS::MWAA::Environment.KmsKey``.
        :param logging_configuration: ``AWS::MWAA::Environment.LoggingConfiguration``.
        :param max_workers: ``AWS::MWAA::Environment.MaxWorkers``.
        :param network_configuration: ``AWS::MWAA::Environment.NetworkConfiguration``.
        :param plugins_s3_object_version: ``AWS::MWAA::Environment.PluginsS3ObjectVersion``.
        :param plugins_s3_path: ``AWS::MWAA::Environment.PluginsS3Path``.
        :param requirements_s3_object_version: ``AWS::MWAA::Environment.RequirementsS3ObjectVersion``.
        :param requirements_s3_path: ``AWS::MWAA::Environment.RequirementsS3Path``.
        :param source_bucket_arn: ``AWS::MWAA::Environment.SourceBucketArn``.
        :param tags: ``AWS::MWAA::Environment.Tags``.
        :param webserver_access_mode: ``AWS::MWAA::Environment.WebserverAccessMode``.
        :param webserver_url: ``AWS::MWAA::Environment.WebserverUrl``.
        :param weekly_maintenance_window_start: ``AWS::MWAA::Environment.WeeklyMaintenanceWindowStart``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html
        """
        if isinstance(tags, dict):
            tags = CfnEnvironment.TagMapProperty(**tags)
        self._values: typing.Dict[str, typing.Any] = {}
        if airflow_configuration_options is not None:
            self._values["airflow_configuration_options"] = airflow_configuration_options
        if airflow_version is not None:
            self._values["airflow_version"] = airflow_version
        if dag_s3_path is not None:
            self._values["dag_s3_path"] = dag_s3_path
        if environment_class is not None:
            self._values["environment_class"] = environment_class
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if max_workers is not None:
            self._values["max_workers"] = max_workers
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if plugins_s3_object_version is not None:
            self._values["plugins_s3_object_version"] = plugins_s3_object_version
        if plugins_s3_path is not None:
            self._values["plugins_s3_path"] = plugins_s3_path
        if requirements_s3_object_version is not None:
            self._values["requirements_s3_object_version"] = requirements_s3_object_version
        if requirements_s3_path is not None:
            self._values["requirements_s3_path"] = requirements_s3_path
        if source_bucket_arn is not None:
            self._values["source_bucket_arn"] = source_bucket_arn
        if tags is not None:
            self._values["tags"] = tags
        if webserver_access_mode is not None:
            self._values["webserver_access_mode"] = webserver_access_mode
        if webserver_url is not None:
            self._values["webserver_url"] = webserver_url
        if weekly_maintenance_window_start is not None:
            self._values["weekly_maintenance_window_start"] = weekly_maintenance_window_start

    @builtins.property
    def airflow_configuration_options(
        self,
    ) -> typing.Optional[typing.Union[CfnEnvironment.AirflowConfigurationOptionsProperty, _IResolvable_6e2f5d88]]:
        """``AWS::MWAA::Environment.AirflowConfigurationOptions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-airflowconfigurationoptions
        """
        result = self._values.get("airflow_configuration_options")
        return result

    @builtins.property
    def airflow_version(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.AirflowVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-airflowversion
        """
        result = self._values.get("airflow_version")
        return result

    @builtins.property
    def dag_s3_path(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.DagS3Path``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-dags3path
        """
        result = self._values.get("dag_s3_path")
        return result

    @builtins.property
    def environment_class(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.EnvironmentClass``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-environmentclass
        """
        result = self._values.get("environment_class")
        return result

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.ExecutionRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-executionrolearn
        """
        result = self._values.get("execution_role_arn")
        return result

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.KmsKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-kmskey
        """
        result = self._values.get("kms_key")
        return result

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnEnvironment.LoggingConfigurationProperty, _IResolvable_6e2f5d88]]:
        """``AWS::MWAA::Environment.LoggingConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-loggingconfiguration
        """
        result = self._values.get("logging_configuration")
        return result

    @builtins.property
    def max_workers(self) -> typing.Optional[jsii.Number]:
        """``AWS::MWAA::Environment.MaxWorkers``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-maxworkers
        """
        result = self._values.get("max_workers")
        return result

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnEnvironment.NetworkConfigurationProperty, _IResolvable_6e2f5d88]]:
        """``AWS::MWAA::Environment.NetworkConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-networkconfiguration
        """
        result = self._values.get("network_configuration")
        return result

    @builtins.property
    def plugins_s3_object_version(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.PluginsS3ObjectVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-pluginss3objectversion
        """
        result = self._values.get("plugins_s3_object_version")
        return result

    @builtins.property
    def plugins_s3_path(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.PluginsS3Path``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-pluginss3path
        """
        result = self._values.get("plugins_s3_path")
        return result

    @builtins.property
    def requirements_s3_object_version(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.RequirementsS3ObjectVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-requirementss3objectversion
        """
        result = self._values.get("requirements_s3_object_version")
        return result

    @builtins.property
    def requirements_s3_path(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.RequirementsS3Path``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-requirementss3path
        """
        result = self._values.get("requirements_s3_path")
        return result

    @builtins.property
    def source_bucket_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.SourceBucketArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-sourcebucketarn
        """
        result = self._values.get("source_bucket_arn")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[CfnEnvironment.TagMapProperty]:
        """``AWS::MWAA::Environment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def webserver_access_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.WebserverAccessMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-webserveraccessmode
        """
        result = self._values.get("webserver_access_mode")
        return result

    @builtins.property
    def webserver_url(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.WebserverUrl``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-webserverurl
        """
        result = self._values.get("webserver_url")
        return result

    @builtins.property
    def weekly_maintenance_window_start(self) -> typing.Optional[builtins.str]:
        """``AWS::MWAA::Environment.WeeklyMaintenanceWindowStart``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mwaa-environment.html#cfn-mwaa-environment-weeklymaintenancewindowstart
        """
        result = self._values.get("weekly_maintenance_window_start")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnEnvironment",
    "CfnEnvironmentProps",
]

publication.publish()
