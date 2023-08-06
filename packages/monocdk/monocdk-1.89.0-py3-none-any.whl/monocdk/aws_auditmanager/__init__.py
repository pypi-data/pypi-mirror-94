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
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnAssessment(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_auditmanager.CfnAssessment",
):
    """A CloudFormation ``AWS::AuditManager::Assessment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html
    :cloudformationResource: AWS::AuditManager::Assessment
    """

    def __init__(
        self,
        scope_: _Construct_e78e779f,
        id: builtins.str,
        *,
        assessment_reports_destination: typing.Optional[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", _IResolvable_a771d0ef]] = None,
        aws_account: typing.Optional[typing.Union["CfnAssessment.AWSAccountProperty", _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        framework_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.RoleProperty", _IResolvable_a771d0ef]]]] = None,
        scope: typing.Optional[typing.Union["CfnAssessment.ScopeProperty", _IResolvable_a771d0ef]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::AuditManager::Assessment``.

        :param scope_: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assessment_reports_destination: ``AWS::AuditManager::Assessment.AssessmentReportsDestination``.
        :param aws_account: ``AWS::AuditManager::Assessment.AwsAccount``.
        :param description: ``AWS::AuditManager::Assessment.Description``.
        :param framework_id: ``AWS::AuditManager::Assessment.FrameworkId``.
        :param name: ``AWS::AuditManager::Assessment.Name``.
        :param roles: ``AWS::AuditManager::Assessment.Roles``.
        :param scope: ``AWS::AuditManager::Assessment.Scope``.
        :param status: ``AWS::AuditManager::Assessment.Status``.
        :param tags: ``AWS::AuditManager::Assessment.Tags``.
        """
        props = CfnAssessmentProps(
            assessment_reports_destination=assessment_reports_destination,
            aws_account=aws_account,
            description=description,
            framework_id=framework_id,
            name=name,
            roles=roles,
            scope=scope,
            status=status,
            tags=tags,
        )

        jsii.create(CfnAssessment, self, [scope_, id, props])

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
    @jsii.member(jsii_name="attrAssessmentId")
    def attr_assessment_id(self) -> builtins.str:
        """
        :cloudformationAttribute: AssessmentId
        """
        return jsii.get(self, "attrAssessmentId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> _IResolvable_a771d0ef:
        """
        :cloudformationAttribute: CreationTime
        """
        return jsii.get(self, "attrCreationTime")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrDelegations")
    def attr_delegations(self) -> _IResolvable_a771d0ef:
        """
        :cloudformationAttribute: Delegations
        """
        return jsii.get(self, "attrDelegations")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrFrameworkId")
    def attr_framework_id(self) -> builtins.str:
        """
        :cloudformationAttribute: FrameworkId
        """
        return jsii.get(self, "attrFrameworkId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::AuditManager::Assessment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="assessmentReportsDestination")
    def assessment_reports_destination(
        self,
    ) -> typing.Optional[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", _IResolvable_a771d0ef]]:
        """``AWS::AuditManager::Assessment.AssessmentReportsDestination``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-assessmentreportsdestination
        """
        return jsii.get(self, "assessmentReportsDestination")

    @assessment_reports_destination.setter # type: ignore
    def assessment_reports_destination(
        self,
        value: typing.Optional[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "assessmentReportsDestination", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="awsAccount")
    def aws_account(
        self,
    ) -> typing.Optional[typing.Union["CfnAssessment.AWSAccountProperty", _IResolvable_a771d0ef]]:
        """``AWS::AuditManager::Assessment.AwsAccount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-awsaccount
        """
        return jsii.get(self, "awsAccount")

    @aws_account.setter # type: ignore
    def aws_account(
        self,
        value: typing.Optional[typing.Union["CfnAssessment.AWSAccountProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "awsAccount", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::AuditManager::Assessment.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="frameworkId")
    def framework_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AuditManager::Assessment.FrameworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-frameworkid
        """
        return jsii.get(self, "frameworkId")

    @framework_id.setter # type: ignore
    def framework_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "frameworkId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::AuditManager::Assessment.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roles")
    def roles(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.RoleProperty", _IResolvable_a771d0ef]]]]:
        """``AWS::AuditManager::Assessment.Roles``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-roles
        """
        return jsii.get(self, "roles")

    @roles.setter # type: ignore
    def roles(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.RoleProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "roles", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scope")
    def scope(
        self,
    ) -> typing.Optional[typing.Union["CfnAssessment.ScopeProperty", _IResolvable_a771d0ef]]:
        """``AWS::AuditManager::Assessment.Scope``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-scope
        """
        return jsii.get(self, "scope")

    @scope.setter # type: ignore
    def scope(
        self,
        value: typing.Optional[typing.Union["CfnAssessment.ScopeProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "scope", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::AuditManager::Assessment.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-status
        """
        return jsii.get(self, "status")

    @status.setter # type: ignore
    def status(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.AWSAccountProperty",
        jsii_struct_bases=[],
        name_mapping={"email_address": "emailAddress", "id": "id", "name": "name"},
    )
    class AWSAccountProperty:
        def __init__(
            self,
            *,
            email_address: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param email_address: ``CfnAssessment.AWSAccountProperty.EmailAddress``.
            :param id: ``CfnAssessment.AWSAccountProperty.Id``.
            :param name: ``CfnAssessment.AWSAccountProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if email_address is not None:
                self._values["email_address"] = email_address
            if id is not None:
                self._values["id"] = id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def email_address(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.AWSAccountProperty.EmailAddress``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html#cfn-auditmanager-assessment-awsaccount-emailaddress
            """
            result = self._values.get("email_address")
            return result

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.AWSAccountProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html#cfn-auditmanager-assessment-awsaccount-id
            """
            result = self._values.get("id")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.AWSAccountProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html#cfn-auditmanager-assessment-awsaccount-name
            """
            result = self._values.get("name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSAccountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.AWSServiceProperty",
        jsii_struct_bases=[],
        name_mapping={"service_name": "serviceName"},
    )
    class AWSServiceProperty:
        def __init__(
            self,
            *,
            service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param service_name: ``CfnAssessment.AWSServiceProperty.ServiceName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsservice.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if service_name is not None:
                self._values["service_name"] = service_name

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.AWSServiceProperty.ServiceName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsservice.html#cfn-auditmanager-assessment-awsservice-servicename
            """
            result = self._values.get("service_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSServiceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.AssessmentReportsDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "destination_type": "destinationType",
        },
    )
    class AssessmentReportsDestinationProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
            destination_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param destination: ``CfnAssessment.AssessmentReportsDestinationProperty.Destination``.
            :param destination_type: ``CfnAssessment.AssessmentReportsDestinationProperty.DestinationType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-assessmentreportsdestination.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if destination_type is not None:
                self._values["destination_type"] = destination_type

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.AssessmentReportsDestinationProperty.Destination``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-assessmentreportsdestination.html#cfn-auditmanager-assessment-assessmentreportsdestination-destination
            """
            result = self._values.get("destination")
            return result

        @builtins.property
        def destination_type(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.AssessmentReportsDestinationProperty.DestinationType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-assessmentreportsdestination.html#cfn-auditmanager-assessment-assessmentreportsdestination-destinationtype
            """
            result = self._values.get("destination_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssessmentReportsDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.DelegationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "assessment_id": "assessmentId",
            "assessment_name": "assessmentName",
            "comment": "comment",
            "control_set_id": "controlSetId",
            "created_by": "createdBy",
            "creation_time": "creationTime",
            "id": "id",
            "last_updated": "lastUpdated",
            "role_arn": "roleArn",
            "role_type": "roleType",
            "status": "status",
        },
    )
    class DelegationProperty:
        def __init__(
            self,
            *,
            assessment_id: typing.Optional[builtins.str] = None,
            assessment_name: typing.Optional[builtins.str] = None,
            comment: typing.Optional[builtins.str] = None,
            control_set_id: typing.Optional[builtins.str] = None,
            created_by: typing.Optional[builtins.str] = None,
            creation_time: typing.Optional[jsii.Number] = None,
            id: typing.Optional[builtins.str] = None,
            last_updated: typing.Optional[jsii.Number] = None,
            role_arn: typing.Optional[builtins.str] = None,
            role_type: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param assessment_id: ``CfnAssessment.DelegationProperty.AssessmentId``.
            :param assessment_name: ``CfnAssessment.DelegationProperty.AssessmentName``.
            :param comment: ``CfnAssessment.DelegationProperty.Comment``.
            :param control_set_id: ``CfnAssessment.DelegationProperty.ControlSetId``.
            :param created_by: ``CfnAssessment.DelegationProperty.CreatedBy``.
            :param creation_time: ``CfnAssessment.DelegationProperty.CreationTime``.
            :param id: ``CfnAssessment.DelegationProperty.Id``.
            :param last_updated: ``CfnAssessment.DelegationProperty.LastUpdated``.
            :param role_arn: ``CfnAssessment.DelegationProperty.RoleArn``.
            :param role_type: ``CfnAssessment.DelegationProperty.RoleType``.
            :param status: ``CfnAssessment.DelegationProperty.Status``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if assessment_id is not None:
                self._values["assessment_id"] = assessment_id
            if assessment_name is not None:
                self._values["assessment_name"] = assessment_name
            if comment is not None:
                self._values["comment"] = comment
            if control_set_id is not None:
                self._values["control_set_id"] = control_set_id
            if created_by is not None:
                self._values["created_by"] = created_by
            if creation_time is not None:
                self._values["creation_time"] = creation_time
            if id is not None:
                self._values["id"] = id
            if last_updated is not None:
                self._values["last_updated"] = last_updated
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if role_type is not None:
                self._values["role_type"] = role_type
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def assessment_id(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.DelegationProperty.AssessmentId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-assessmentid
            """
            result = self._values.get("assessment_id")
            return result

        @builtins.property
        def assessment_name(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.DelegationProperty.AssessmentName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-assessmentname
            """
            result = self._values.get("assessment_name")
            return result

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.DelegationProperty.Comment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-comment
            """
            result = self._values.get("comment")
            return result

        @builtins.property
        def control_set_id(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.DelegationProperty.ControlSetId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-controlsetid
            """
            result = self._values.get("control_set_id")
            return result

        @builtins.property
        def created_by(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.DelegationProperty.CreatedBy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-createdby
            """
            result = self._values.get("created_by")
            return result

        @builtins.property
        def creation_time(self) -> typing.Optional[jsii.Number]:
            """``CfnAssessment.DelegationProperty.CreationTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-creationtime
            """
            result = self._values.get("creation_time")
            return result

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.DelegationProperty.Id``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-id
            """
            result = self._values.get("id")
            return result

        @builtins.property
        def last_updated(self) -> typing.Optional[jsii.Number]:
            """``CfnAssessment.DelegationProperty.LastUpdated``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-lastupdated
            """
            result = self._values.get("last_updated")
            return result

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.DelegationProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-rolearn
            """
            result = self._values.get("role_arn")
            return result

        @builtins.property
        def role_type(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.DelegationProperty.RoleType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-roletype
            """
            result = self._values.get("role_type")
            return result

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.DelegationProperty.Status``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-status
            """
            result = self._values.get("status")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DelegationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.RoleProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "role_type": "roleType"},
    )
    class RoleProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            role_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param role_arn: ``CfnAssessment.RoleProperty.RoleArn``.
            :param role_type: ``CfnAssessment.RoleProperty.RoleType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-role.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if role_type is not None:
                self._values["role_type"] = role_type

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.RoleProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-role.html#cfn-auditmanager-assessment-role-rolearn
            """
            result = self._values.get("role_arn")
            return result

        @builtins.property
        def role_type(self) -> typing.Optional[builtins.str]:
            """``CfnAssessment.RoleProperty.RoleType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-role.html#cfn-auditmanager-assessment-role-roletype
            """
            result = self._values.get("role_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.ScopeProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_accounts": "awsAccounts", "aws_services": "awsServices"},
    )
    class ScopeProperty:
        def __init__(
            self,
            *,
            aws_accounts: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.AWSAccountProperty", _IResolvable_a771d0ef]]]] = None,
            aws_services: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.AWSServiceProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param aws_accounts: ``CfnAssessment.ScopeProperty.AwsAccounts``.
            :param aws_services: ``CfnAssessment.ScopeProperty.AwsServices``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-scope.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if aws_accounts is not None:
                self._values["aws_accounts"] = aws_accounts
            if aws_services is not None:
                self._values["aws_services"] = aws_services

        @builtins.property
        def aws_accounts(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.AWSAccountProperty", _IResolvable_a771d0ef]]]]:
            """``CfnAssessment.ScopeProperty.AwsAccounts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-scope.html#cfn-auditmanager-assessment-scope-awsaccounts
            """
            result = self._values.get("aws_accounts")
            return result

        @builtins.property
        def aws_services(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.AWSServiceProperty", _IResolvable_a771d0ef]]]]:
            """``CfnAssessment.ScopeProperty.AwsServices``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-scope.html#cfn-auditmanager-assessment-scope-awsservices
            """
            result = self._values.get("aws_services")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_auditmanager.CfnAssessmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "assessment_reports_destination": "assessmentReportsDestination",
        "aws_account": "awsAccount",
        "description": "description",
        "framework_id": "frameworkId",
        "name": "name",
        "roles": "roles",
        "scope": "scope",
        "status": "status",
        "tags": "tags",
    },
)
class CfnAssessmentProps:
    def __init__(
        self,
        *,
        assessment_reports_destination: typing.Optional[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, _IResolvable_a771d0ef]] = None,
        aws_account: typing.Optional[typing.Union[CfnAssessment.AWSAccountProperty, _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        framework_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssessment.RoleProperty, _IResolvable_a771d0ef]]]] = None,
        scope: typing.Optional[typing.Union[CfnAssessment.ScopeProperty, _IResolvable_a771d0ef]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::AuditManager::Assessment``.

        :param assessment_reports_destination: ``AWS::AuditManager::Assessment.AssessmentReportsDestination``.
        :param aws_account: ``AWS::AuditManager::Assessment.AwsAccount``.
        :param description: ``AWS::AuditManager::Assessment.Description``.
        :param framework_id: ``AWS::AuditManager::Assessment.FrameworkId``.
        :param name: ``AWS::AuditManager::Assessment.Name``.
        :param roles: ``AWS::AuditManager::Assessment.Roles``.
        :param scope: ``AWS::AuditManager::Assessment.Scope``.
        :param status: ``AWS::AuditManager::Assessment.Status``.
        :param tags: ``AWS::AuditManager::Assessment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if assessment_reports_destination is not None:
            self._values["assessment_reports_destination"] = assessment_reports_destination
        if aws_account is not None:
            self._values["aws_account"] = aws_account
        if description is not None:
            self._values["description"] = description
        if framework_id is not None:
            self._values["framework_id"] = framework_id
        if name is not None:
            self._values["name"] = name
        if roles is not None:
            self._values["roles"] = roles
        if scope is not None:
            self._values["scope"] = scope
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def assessment_reports_destination(
        self,
    ) -> typing.Optional[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, _IResolvable_a771d0ef]]:
        """``AWS::AuditManager::Assessment.AssessmentReportsDestination``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-assessmentreportsdestination
        """
        result = self._values.get("assessment_reports_destination")
        return result

    @builtins.property
    def aws_account(
        self,
    ) -> typing.Optional[typing.Union[CfnAssessment.AWSAccountProperty, _IResolvable_a771d0ef]]:
        """``AWS::AuditManager::Assessment.AwsAccount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-awsaccount
        """
        result = self._values.get("aws_account")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::AuditManager::Assessment.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def framework_id(self) -> typing.Optional[builtins.str]:
        """``AWS::AuditManager::Assessment.FrameworkId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-frameworkid
        """
        result = self._values.get("framework_id")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::AuditManager::Assessment.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def roles(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssessment.RoleProperty, _IResolvable_a771d0ef]]]]:
        """``AWS::AuditManager::Assessment.Roles``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-roles
        """
        result = self._values.get("roles")
        return result

    @builtins.property
    def scope(
        self,
    ) -> typing.Optional[typing.Union[CfnAssessment.ScopeProperty, _IResolvable_a771d0ef]]:
        """``AWS::AuditManager::Assessment.Scope``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-scope
        """
        result = self._values.get("scope")
        return result

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::AuditManager::Assessment.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-status
        """
        result = self._values.get("status")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::AuditManager::Assessment.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssessmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAssessment",
    "CfnAssessmentProps",
]

publication.publish()
