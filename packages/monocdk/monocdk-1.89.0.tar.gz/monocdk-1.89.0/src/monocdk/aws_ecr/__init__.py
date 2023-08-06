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
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    ResourceProps as _ResourceProps_9b554c0f,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_events import (
    EventPattern as _EventPattern_a23fbf37,
    IRuleTarget as _IRuleTarget_d45ec729,
    OnEventOptions as _OnEventOptions_d5081088,
    Rule as _Rule_6cfff189,
)
from ..aws_iam import (
    AddToResourcePolicyResult as _AddToResourcePolicyResult_0fd9d2a9,
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    PolicyStatement as _PolicyStatement_296fe8a3,
)


class AuthorizationToken(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ecr.AuthorizationToken",
):
    """(experimental) Authorization token to access private ECR repositories in the current environment via Docker CLI.

    :see: https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html
    :stability: experimental
    """

    @jsii.member(jsii_name="grantRead")
    @builtins.classmethod
    def grant_read(cls, grantee: _IGrantable_4c5a91d1) -> None:
        """(experimental) Grant access to retrieve an authorization token.

        :param grantee: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "grantRead", [grantee])


@jsii.implements(_IInspectable_82c04a63)
class CfnPublicRepository(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ecr.CfnPublicRepository",
):
    """A CloudFormation ``AWS::ECR::PublicRepository``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html
    :cloudformationResource: AWS::ECR::PublicRepository
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        repository_catalog_data: typing.Any = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::ECR::PublicRepository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param repository_catalog_data: ``AWS::ECR::PublicRepository.RepositoryCatalogData``.
        :param repository_name: ``AWS::ECR::PublicRepository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::PublicRepository.RepositoryPolicyText``.
        """
        props = CfnPublicRepositoryProps(
            repository_catalog_data=repository_catalog_data,
            repository_name=repository_name,
            repository_policy_text=repository_policy_text,
        )

        jsii.create(CfnPublicRepository, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryCatalogData")
    def repository_catalog_data(self) -> typing.Any:
        """``AWS::ECR::PublicRepository.RepositoryCatalogData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositorycatalogdata
        """
        return jsii.get(self, "repositoryCatalogData")

    @repository_catalog_data.setter # type: ignore
    def repository_catalog_data(self, value: typing.Any) -> None:
        jsii.set(self, "repositoryCatalogData", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryPolicyText")
    def repository_policy_text(self) -> typing.Any:
        """``AWS::ECR::PublicRepository.RepositoryPolicyText``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositorypolicytext
        """
        return jsii.get(self, "repositoryPolicyText")

    @repository_policy_text.setter # type: ignore
    def repository_policy_text(self, value: typing.Any) -> None:
        jsii.set(self, "repositoryPolicyText", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ECR::PublicRepository.RepositoryName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositoryname
        """
        return jsii.get(self, "repositoryName")

    @repository_name.setter # type: ignore
    def repository_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "repositoryName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_ecr.CfnPublicRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository_catalog_data": "repositoryCatalogData",
        "repository_name": "repositoryName",
        "repository_policy_text": "repositoryPolicyText",
    },
)
class CfnPublicRepositoryProps:
    def __init__(
        self,
        *,
        repository_catalog_data: typing.Any = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::ECR::PublicRepository``.

        :param repository_catalog_data: ``AWS::ECR::PublicRepository.RepositoryCatalogData``.
        :param repository_name: ``AWS::ECR::PublicRepository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::PublicRepository.RepositoryPolicyText``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if repository_catalog_data is not None:
            self._values["repository_catalog_data"] = repository_catalog_data
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if repository_policy_text is not None:
            self._values["repository_policy_text"] = repository_policy_text

    @builtins.property
    def repository_catalog_data(self) -> typing.Any:
        """``AWS::ECR::PublicRepository.RepositoryCatalogData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositorycatalogdata
        """
        result = self._values.get("repository_catalog_data")
        return result

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ECR::PublicRepository.RepositoryName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositoryname
        """
        result = self._values.get("repository_name")
        return result

    @builtins.property
    def repository_policy_text(self) -> typing.Any:
        """``AWS::ECR::PublicRepository.RepositoryPolicyText``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositorypolicytext
        """
        result = self._values.get("repository_policy_text")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublicRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRepository(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ecr.CfnRepository",
):
    """A CloudFormation ``AWS::ECR::Repository``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
    :cloudformationResource: AWS::ECR::Repository
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        image_scanning_configuration: typing.Any = None,
        image_tag_mutability: typing.Optional[builtins.str] = None,
        lifecycle_policy: typing.Optional[typing.Union["CfnRepository.LifecyclePolicyProperty", _IResolvable_a771d0ef]] = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::ECR::Repository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param image_scanning_configuration: ``AWS::ECR::Repository.ImageScanningConfiguration``.
        :param image_tag_mutability: ``AWS::ECR::Repository.ImageTagMutability``.
        :param lifecycle_policy: ``AWS::ECR::Repository.LifecyclePolicy``.
        :param repository_name: ``AWS::ECR::Repository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::Repository.RepositoryPolicyText``.
        :param tags: ``AWS::ECR::Repository.Tags``.
        """
        props = CfnRepositoryProps(
            image_scanning_configuration=image_scanning_configuration,
            image_tag_mutability=image_tag_mutability,
            lifecycle_policy=lifecycle_policy,
            repository_name=repository_name,
            repository_policy_text=repository_policy_text,
            tags=tags,
        )

        jsii.create(CfnRepository, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::ECR::Repository.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageScanningConfiguration")
    def image_scanning_configuration(self) -> typing.Any:
        """``AWS::ECR::Repository.ImageScanningConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagescanningconfiguration
        """
        return jsii.get(self, "imageScanningConfiguration")

    @image_scanning_configuration.setter # type: ignore
    def image_scanning_configuration(self, value: typing.Any) -> None:
        jsii.set(self, "imageScanningConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryPolicyText")
    def repository_policy_text(self) -> typing.Any:
        """``AWS::ECR::Repository.RepositoryPolicyText``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositorypolicytext
        """
        return jsii.get(self, "repositoryPolicyText")

    @repository_policy_text.setter # type: ignore
    def repository_policy_text(self, value: typing.Any) -> None:
        jsii.set(self, "repositoryPolicyText", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageTagMutability")
    def image_tag_mutability(self) -> typing.Optional[builtins.str]:
        """``AWS::ECR::Repository.ImageTagMutability``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagetagmutability
        """
        return jsii.get(self, "imageTagMutability")

    @image_tag_mutability.setter # type: ignore
    def image_tag_mutability(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageTagMutability", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lifecyclePolicy")
    def lifecycle_policy(
        self,
    ) -> typing.Optional[typing.Union["CfnRepository.LifecyclePolicyProperty", _IResolvable_a771d0ef]]:
        """``AWS::ECR::Repository.LifecyclePolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-lifecyclepolicy
        """
        return jsii.get(self, "lifecyclePolicy")

    @lifecycle_policy.setter # type: ignore
    def lifecycle_policy(
        self,
        value: typing.Optional[typing.Union["CfnRepository.LifecyclePolicyProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "lifecyclePolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ECR::Repository.RepositoryName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositoryname
        """
        return jsii.get(self, "repositoryName")

    @repository_name.setter # type: ignore
    def repository_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "repositoryName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_ecr.CfnRepository.LifecyclePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lifecycle_policy_text": "lifecyclePolicyText",
            "registry_id": "registryId",
        },
    )
    class LifecyclePolicyProperty:
        def __init__(
            self,
            *,
            lifecycle_policy_text: typing.Optional[builtins.str] = None,
            registry_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param lifecycle_policy_text: ``CfnRepository.LifecyclePolicyProperty.LifecyclePolicyText``.
            :param registry_id: ``CfnRepository.LifecyclePolicyProperty.RegistryId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if lifecycle_policy_text is not None:
                self._values["lifecycle_policy_text"] = lifecycle_policy_text
            if registry_id is not None:
                self._values["registry_id"] = registry_id

        @builtins.property
        def lifecycle_policy_text(self) -> typing.Optional[builtins.str]:
            """``CfnRepository.LifecyclePolicyProperty.LifecyclePolicyText``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-lifecyclepolicytext
            """
            result = self._values.get("lifecycle_policy_text")
            return result

        @builtins.property
        def registry_id(self) -> typing.Optional[builtins.str]:
            """``CfnRepository.LifecyclePolicyProperty.RegistryId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-registryid
            """
            result = self._values.get("registry_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecyclePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_ecr.CfnRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_scanning_configuration": "imageScanningConfiguration",
        "image_tag_mutability": "imageTagMutability",
        "lifecycle_policy": "lifecyclePolicy",
        "repository_name": "repositoryName",
        "repository_policy_text": "repositoryPolicyText",
        "tags": "tags",
    },
)
class CfnRepositoryProps:
    def __init__(
        self,
        *,
        image_scanning_configuration: typing.Any = None,
        image_tag_mutability: typing.Optional[builtins.str] = None,
        lifecycle_policy: typing.Optional[typing.Union[CfnRepository.LifecyclePolicyProperty, _IResolvable_a771d0ef]] = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ECR::Repository``.

        :param image_scanning_configuration: ``AWS::ECR::Repository.ImageScanningConfiguration``.
        :param image_tag_mutability: ``AWS::ECR::Repository.ImageTagMutability``.
        :param lifecycle_policy: ``AWS::ECR::Repository.LifecyclePolicy``.
        :param repository_name: ``AWS::ECR::Repository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::Repository.RepositoryPolicyText``.
        :param tags: ``AWS::ECR::Repository.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if image_scanning_configuration is not None:
            self._values["image_scanning_configuration"] = image_scanning_configuration
        if image_tag_mutability is not None:
            self._values["image_tag_mutability"] = image_tag_mutability
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if repository_policy_text is not None:
            self._values["repository_policy_text"] = repository_policy_text
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def image_scanning_configuration(self) -> typing.Any:
        """``AWS::ECR::Repository.ImageScanningConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagescanningconfiguration
        """
        result = self._values.get("image_scanning_configuration")
        return result

    @builtins.property
    def image_tag_mutability(self) -> typing.Optional[builtins.str]:
        """``AWS::ECR::Repository.ImageTagMutability``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagetagmutability
        """
        result = self._values.get("image_tag_mutability")
        return result

    @builtins.property
    def lifecycle_policy(
        self,
    ) -> typing.Optional[typing.Union[CfnRepository.LifecyclePolicyProperty, _IResolvable_a771d0ef]]:
        """``AWS::ECR::Repository.LifecyclePolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-lifecyclepolicy
        """
        result = self._values.get("lifecycle_policy")
        return result

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ECR::Repository.RepositoryName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositoryname
        """
        result = self._values.get("repository_name")
        return result

    @builtins.property
    def repository_policy_text(self) -> typing.Any:
        """``AWS::ECR::Repository.RepositoryPolicyText``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositorypolicytext
        """
        result = self._values.get("repository_policy_text")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::ECR::Repository.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_ecr.IRepository")
class IRepository(_IResource_8c1dbbbd, typing_extensions.Protocol):
    """(experimental) Represents an ECR repository.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRepositoryProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        """(experimental) The ARN of the repository.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        """(experimental) The name of the repository.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        """(experimental) The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY

        :stability: experimental
        :attribute: true
        """
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        """(experimental) Add a policy statement to the repository's resource policy.

        :param statement: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        """(experimental) Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant the given identity permissions to pull images in this repository.

        :param grantee: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(
        self,
        id: builtins.str,
        *,
        image_tag: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param image_tag: (experimental) Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(
        self,
        id: builtins.str,
        *,
        image_tags: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Defines an AWS CloudWatch event rule that can trigger a target when the image scan is completed.

        :param id: The id of the rule.
        :param image_tags: (experimental) Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(
        self,
        tag: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        """(experimental) Returns the URI of the repository for a certain tag. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Image tag to use (tools usually default to "latest" if omitted).

        :stability: experimental
        """
        ...


class _IRepositoryProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore
):
    """(experimental) Represents an ECR repository.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_ecr.IRepository"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        """(experimental) The ARN of the repository.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "repositoryArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        """(experimental) The name of the repository.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "repositoryName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        """(experimental) The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "repositoryUri")

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        """(experimental) Add a policy statement to the repository's resource policy.

        :param statement: -

        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        """(experimental) Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -

        :stability: experimental
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant the given identity permissions to pull images in this repository.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantPull", [grantee])

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantPullPush", [grantee])

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onCloudTrailEvent", [id, options])

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(
        self,
        id: builtins.str,
        *,
        image_tag: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param image_tag: (experimental) Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        options = OnCloudTrailImagePushedOptions(
            image_tag=image_tag,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onCloudTrailImagePushed", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(
        self,
        id: builtins.str,
        *,
        image_tags: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Defines an AWS CloudWatch event rule that can trigger a target when the image scan is completed.

        :param id: The id of the rule.
        :param image_tags: (experimental) Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        options = OnImageScanCompletedOptions(
            image_tags=image_tags,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onImageScanCompleted", [id, options])

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(
        self,
        tag: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        """(experimental) Returns the URI of the repository for a certain tag. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Image tag to use (tools usually default to "latest" if omitted).

        :stability: experimental
        """
        return jsii.invoke(self, "repositoryUriForTag", [tag])


@jsii.data_type(
    jsii_type="monocdk.aws_ecr.LifecycleRule",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "max_image_age": "maxImageAge",
        "max_image_count": "maxImageCount",
        "rule_priority": "rulePriority",
        "tag_prefix_list": "tagPrefixList",
        "tag_status": "tagStatus",
    },
)
class LifecycleRule:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        max_image_age: typing.Optional[_Duration_070aa057] = None,
        max_image_count: typing.Optional[jsii.Number] = None,
        rule_priority: typing.Optional[jsii.Number] = None,
        tag_prefix_list: typing.Optional[typing.List[builtins.str]] = None,
        tag_status: typing.Optional["TagStatus"] = None,
    ) -> None:
        """(experimental) An ECR life cycle rule.

        :param description: (experimental) Describes the purpose of the rule. Default: No description
        :param max_image_age: (experimental) The maximum age of images to retain. The value must represent a number of days. Specify exactly one of maxImageCount and maxImageAge.
        :param max_image_count: (experimental) The maximum number of images to retain. Specify exactly one of maxImageCount and maxImageAge.
        :param rule_priority: (experimental) Controls the order in which rules are evaluated (low to high). All rules must have a unique priority, where lower numbers have higher precedence. The first rule that matches is applied to an image. There can only be one rule with a tagStatus of Any, and it must have the highest rulePriority. All rules without a specified priority will have incrementing priorities automatically assigned to them, higher than any rules that DO have priorities. Default: Automatically assigned
        :param tag_prefix_list: (experimental) Select images that have ALL the given prefixes in their tag. Only if tagStatus == TagStatus.Tagged
        :param tag_status: (experimental) Select images based on tags. Only one rule is allowed to select untagged images, and it must have the highest rulePriority. Default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if max_image_age is not None:
            self._values["max_image_age"] = max_image_age
        if max_image_count is not None:
            self._values["max_image_count"] = max_image_count
        if rule_priority is not None:
            self._values["rule_priority"] = rule_priority
        if tag_prefix_list is not None:
            self._values["tag_prefix_list"] = tag_prefix_list
        if tag_status is not None:
            self._values["tag_status"] = tag_status

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """(experimental) Describes the purpose of the rule.

        :default: No description

        :stability: experimental
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def max_image_age(self) -> typing.Optional[_Duration_070aa057]:
        """(experimental) The maximum age of images to retain. The value must represent a number of days.

        Specify exactly one of maxImageCount and maxImageAge.

        :stability: experimental
        """
        result = self._values.get("max_image_age")
        return result

    @builtins.property
    def max_image_count(self) -> typing.Optional[jsii.Number]:
        """(experimental) The maximum number of images to retain.

        Specify exactly one of maxImageCount and maxImageAge.

        :stability: experimental
        """
        result = self._values.get("max_image_count")
        return result

    @builtins.property
    def rule_priority(self) -> typing.Optional[jsii.Number]:
        """(experimental) Controls the order in which rules are evaluated (low to high).

        All rules must have a unique priority, where lower numbers have
        higher precedence. The first rule that matches is applied to an image.

        There can only be one rule with a tagStatus of Any, and it must have
        the highest rulePriority.

        All rules without a specified priority will have incrementing priorities
        automatically assigned to them, higher than any rules that DO have priorities.

        :default: Automatically assigned

        :stability: experimental
        """
        result = self._values.get("rule_priority")
        return result

    @builtins.property
    def tag_prefix_list(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) Select images that have ALL the given prefixes in their tag.

        Only if tagStatus == TagStatus.Tagged

        :stability: experimental
        """
        result = self._values.get("tag_prefix_list")
        return result

    @builtins.property
    def tag_status(self) -> typing.Optional["TagStatus"]:
        """(experimental) Select images based on tags.

        Only one rule is allowed to select untagged images, and it must
        have the highest rulePriority.

        :default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise

        :stability: experimental
        """
        result = self._values.get("tag_status")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecycleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_ecr.OnCloudTrailImagePushedOptions",
    jsii_struct_bases=[_OnEventOptions_d5081088],
    name_mapping={
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "target": "target",
        "image_tag": "imageTag",
    },
)
class OnCloudTrailImagePushedOptions(_OnEventOptions_d5081088):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
        image_tag: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Options for the onCloudTrailImagePushed method.

        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param image_tag: (experimental) Only watch changes to this image tag. Default: - Watch changes to all tags

        :stability: experimental
        """
        if isinstance(event_pattern, dict):
            event_pattern = _EventPattern_a23fbf37(**event_pattern)
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if target is not None:
            self._values["target"] = target
        if image_tag is not None:
            self._values["image_tag"] = image_tag

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """(experimental) A description of the rule's purpose.

        :default: - No description

        :stability: experimental
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def event_pattern(self) -> typing.Optional[_EventPattern_a23fbf37]:
        """(experimental) Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        :stability: experimental
        """
        result = self._values.get("event_pattern")
        return result

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        """(experimental) A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        """
        result = self._values.get("rule_name")
        return result

    @builtins.property
    def target(self) -> typing.Optional[_IRuleTarget_d45ec729]:
        """(experimental) The target to register for the event.

        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        result = self._values.get("target")
        return result

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        """(experimental) Only watch changes to this image tag.

        :default: - Watch changes to all tags

        :stability: experimental
        """
        result = self._values.get("image_tag")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCloudTrailImagePushedOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_ecr.OnImageScanCompletedOptions",
    jsii_struct_bases=[_OnEventOptions_d5081088],
    name_mapping={
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "target": "target",
        "image_tags": "imageTags",
    },
)
class OnImageScanCompletedOptions(_OnEventOptions_d5081088):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
        image_tags: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """(experimental) Options for the OnImageScanCompleted method.

        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param image_tags: (experimental) Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags

        :stability: experimental
        """
        if isinstance(event_pattern, dict):
            event_pattern = _EventPattern_a23fbf37(**event_pattern)
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if target is not None:
            self._values["target"] = target
        if image_tags is not None:
            self._values["image_tags"] = image_tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """(experimental) A description of the rule's purpose.

        :default: - No description

        :stability: experimental
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def event_pattern(self) -> typing.Optional[_EventPattern_a23fbf37]:
        """(experimental) Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        :stability: experimental
        """
        result = self._values.get("event_pattern")
        return result

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        """(experimental) A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        """
        result = self._values.get("rule_name")
        return result

    @builtins.property
    def target(self) -> typing.Optional[_IRuleTarget_d45ec729]:
        """(experimental) The target to register for the event.

        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        result = self._values.get("target")
        return result

    @builtins.property
    def image_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) Only watch changes to the image tags spedified.

        Leave it undefined to watch the full repository.

        :default: - Watch the changes to the repository with all image tags

        :stability: experimental
        """
        result = self._values.get("image_tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnImageScanCompletedOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PublicGalleryAuthorizationToken(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ecr.PublicGalleryAuthorizationToken",
):
    """(experimental) Authorization token to access the global public ECR Gallery via Docker CLI.

    :see: https://docs.aws.amazon.com/AmazonECR/latest/public/public-registries.html#public-registry-auth
    :stability: experimental
    """

    @jsii.member(jsii_name="grantRead")
    @builtins.classmethod
    def grant_read(cls, grantee: _IGrantable_4c5a91d1) -> None:
        """(experimental) Grant access to retrieve an authorization token.

        :param grantee: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "grantRead", [grantee])


@jsii.data_type(
    jsii_type="monocdk.aws_ecr.RepositoryAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "repository_arn": "repositoryArn",
        "repository_name": "repositoryName",
    },
)
class RepositoryAttributes:
    def __init__(
        self,
        *,
        repository_arn: builtins.str,
        repository_name: builtins.str,
    ) -> None:
        """
        :param repository_arn: 
        :param repository_name: 

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "repository_arn": repository_arn,
            "repository_name": repository_name,
        }

    @builtins.property
    def repository_arn(self) -> builtins.str:
        """
        :stability: experimental
        """
        result = self._values.get("repository_arn")
        assert result is not None, "Required property 'repository_arn' is missing"
        return result

    @builtins.property
    def repository_name(self) -> builtins.str:
        """
        :stability: experimental
        """
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRepository)
class RepositoryBase(
    _Resource_abff4495,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_ecr.RepositoryBase",
):
    """(experimental) Base class for ECR repository.

    Reused between imported repositories and owned repositories.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _RepositoryBaseProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param account: (experimental) The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: (experimental) The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: (experimental) The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :stability: experimental
        """
        props = _ResourceProps_9b554c0f(
            account=account, physical_name=physical_name, region=region
        )

        jsii.create(RepositoryBase, self, [scope, id, props])

    @jsii.member(jsii_name="addToResourcePolicy")
    @abc.abstractmethod
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        """(experimental) Add a policy statement to the repository's resource policy.

        :param statement: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        """(experimental) Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -

        :stability: experimental
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant the given identity permissions to use the images in this repository.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantPull", [grantee])

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantPullPush", [grantee])

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onCloudTrailEvent", [id, options])

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(
        self,
        id: builtins.str,
        *,
        image_tag: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param image_tag: (experimental) Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        options = OnCloudTrailImagePushedOptions(
            image_tag=image_tag,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onCloudTrailImagePushed", [id, options])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(
        self,
        id: builtins.str,
        *,
        image_tags: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        """(experimental) Defines an AWS CloudWatch event rule that can trigger a target when an image scan is completed.

        :param id: The id of the rule.
        :param image_tags: (experimental) Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        """
        options = OnImageScanCompletedOptions(
            image_tags=image_tags,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onImageScanCompleted", [id, options])

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(
        self,
        tag: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        """(experimental) Returns the URL of the repository. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Optional image tag.

        :stability: experimental
        """
        return jsii.invoke(self, "repositoryUriForTag", [tag])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryArn")
    @abc.abstractmethod
    def repository_arn(self) -> builtins.str:
        """(experimental) The ARN of the repository.

        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    @abc.abstractmethod
    def repository_name(self) -> builtins.str:
        """(experimental) The name of the repository.

        :stability: experimental
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        """(experimental) The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY

        :stability: experimental
        """
        return jsii.get(self, "repositoryUri")


class _RepositoryBaseProxy(
    RepositoryBase, jsii.proxy_for(_Resource_abff4495) # type: ignore
):
    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        """(experimental) Add a policy statement to the repository's resource policy.

        :param statement: -

        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        """(experimental) The ARN of the repository.

        :stability: experimental
        """
        return jsii.get(self, "repositoryArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        """(experimental) The name of the repository.

        :stability: experimental
        """
        return jsii.get(self, "repositoryName")


@jsii.data_type(
    jsii_type="monocdk.aws_ecr.RepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_scan_on_push": "imageScanOnPush",
        "lifecycle_registry_id": "lifecycleRegistryId",
        "lifecycle_rules": "lifecycleRules",
        "removal_policy": "removalPolicy",
        "repository_name": "repositoryName",
    },
)
class RepositoryProps:
    def __init__(
        self,
        *,
        image_scan_on_push: typing.Optional[builtins.bool] = None,
        lifecycle_registry_id: typing.Optional[builtins.str] = None,
        lifecycle_rules: typing.Optional[typing.List[LifecycleRule]] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param image_scan_on_push: (experimental) Enable the scan on push when creating the repository. Default: false
        :param lifecycle_registry_id: (experimental) The AWS account ID associated with the registry that contains the repository. Default: The default registry is assumed.
        :param lifecycle_rules: (experimental) Life cycle rules to apply to this registry. Default: No life cycle rules
        :param removal_policy: (experimental) Determine what happens to the repository when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param repository_name: (experimental) Name for this repository. Default: Automatically generated name.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if image_scan_on_push is not None:
            self._values["image_scan_on_push"] = image_scan_on_push
        if lifecycle_registry_id is not None:
            self._values["lifecycle_registry_id"] = lifecycle_registry_id
        if lifecycle_rules is not None:
            self._values["lifecycle_rules"] = lifecycle_rules
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if repository_name is not None:
            self._values["repository_name"] = repository_name

    @builtins.property
    def image_scan_on_push(self) -> typing.Optional[builtins.bool]:
        """(experimental) Enable the scan on push when creating the repository.

        :default: false

        :stability: experimental
        """
        result = self._values.get("image_scan_on_push")
        return result

    @builtins.property
    def lifecycle_registry_id(self) -> typing.Optional[builtins.str]:
        """(experimental) The AWS account ID associated with the registry that contains the repository.

        :default: The default registry is assumed.

        :see: https://docs.aws.amazon.com/AmazonECR/latest/APIReference/API_PutLifecyclePolicy.html
        :stability: experimental
        """
        result = self._values.get("lifecycle_registry_id")
        return result

    @builtins.property
    def lifecycle_rules(self) -> typing.Optional[typing.List[LifecycleRule]]:
        """(experimental) Life cycle rules to apply to this registry.

        :default: No life cycle rules

        :stability: experimental
        """
        result = self._values.get("lifecycle_rules")
        return result

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        """(experimental) Determine what happens to the repository when the resource/stack is deleted.

        :default: RemovalPolicy.Retain

        :stability: experimental
        """
        result = self._values.get("removal_policy")
        return result

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        """(experimental) Name for this repository.

        :default: Automatically generated name.

        :stability: experimental
        """
        result = self._values.get("repository_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_ecr.TagStatus")
class TagStatus(enum.Enum):
    """(experimental) Select images based on tags.

    :stability: experimental
    """

    ANY = "ANY"
    """(experimental) Rule applies to all images.

    :stability: experimental
    """
    TAGGED = "TAGGED"
    """(experimental) Rule applies to tagged images.

    :stability: experimental
    """
    UNTAGGED = "UNTAGGED"
    """(experimental) Rule applies to untagged images.

    :stability: experimental
    """


class Repository(
    RepositoryBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ecr.Repository",
):
    """(experimental) Define an ECR repository.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        image_scan_on_push: typing.Optional[builtins.bool] = None,
        lifecycle_registry_id: typing.Optional[builtins.str] = None,
        lifecycle_rules: typing.Optional[typing.List[LifecycleRule]] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param image_scan_on_push: (experimental) Enable the scan on push when creating the repository. Default: false
        :param lifecycle_registry_id: (experimental) The AWS account ID associated with the registry that contains the repository. Default: The default registry is assumed.
        :param lifecycle_rules: (experimental) Life cycle rules to apply to this registry. Default: No life cycle rules
        :param removal_policy: (experimental) Determine what happens to the repository when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param repository_name: (experimental) Name for this repository. Default: Automatically generated name.

        :stability: experimental
        """
        props = RepositoryProps(
            image_scan_on_push=image_scan_on_push,
            lifecycle_registry_id=lifecycle_registry_id,
            lifecycle_rules=lifecycle_rules,
            removal_policy=removal_policy,
            repository_name=repository_name,
        )

        jsii.create(Repository, self, [scope, id, props])

    @jsii.member(jsii_name="arnForLocalRepository")
    @builtins.classmethod
    def arn_for_local_repository(
        cls,
        repository_name: builtins.str,
        scope: constructs.IConstruct,
        account: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        """(experimental) Returns an ECR ARN for a repository that resides in the same account/region as the current stack.

        :param repository_name: -
        :param scope: -
        :param account: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "arnForLocalRepository", [repository_name, scope, account])

    @jsii.member(jsii_name="fromRepositoryArn")
    @builtins.classmethod
    def from_repository_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        repository_arn: builtins.str,
    ) -> IRepository:
        """
        :param scope: -
        :param id: -
        :param repository_arn: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromRepositoryArn", [scope, id, repository_arn])

    @jsii.member(jsii_name="fromRepositoryAttributes")
    @builtins.classmethod
    def from_repository_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        repository_arn: builtins.str,
        repository_name: builtins.str,
    ) -> IRepository:
        """(experimental) Import a repository.

        :param scope: -
        :param id: -
        :param repository_arn: 
        :param repository_name: 

        :stability: experimental
        """
        attrs = RepositoryAttributes(
            repository_arn=repository_arn, repository_name=repository_name
        )

        return jsii.sinvoke(cls, "fromRepositoryAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromRepositoryName")
    @builtins.classmethod
    def from_repository_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        repository_name: builtins.str,
    ) -> IRepository:
        """
        :param scope: -
        :param id: -
        :param repository_name: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromRepositoryName", [scope, id, repository_name])

    @jsii.member(jsii_name="addLifecycleRule")
    def add_lifecycle_rule(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        max_image_age: typing.Optional[_Duration_070aa057] = None,
        max_image_count: typing.Optional[jsii.Number] = None,
        rule_priority: typing.Optional[jsii.Number] = None,
        tag_prefix_list: typing.Optional[typing.List[builtins.str]] = None,
        tag_status: typing.Optional[TagStatus] = None,
    ) -> None:
        """(experimental) Add a life cycle rule to the repository.

        Life cycle rules automatically expire images from the repository that match
        certain conditions.

        :param description: (experimental) Describes the purpose of the rule. Default: No description
        :param max_image_age: (experimental) The maximum age of images to retain. The value must represent a number of days. Specify exactly one of maxImageCount and maxImageAge.
        :param max_image_count: (experimental) The maximum number of images to retain. Specify exactly one of maxImageCount and maxImageAge.
        :param rule_priority: (experimental) Controls the order in which rules are evaluated (low to high). All rules must have a unique priority, where lower numbers have higher precedence. The first rule that matches is applied to an image. There can only be one rule with a tagStatus of Any, and it must have the highest rulePriority. All rules without a specified priority will have incrementing priorities automatically assigned to them, higher than any rules that DO have priorities. Default: Automatically assigned
        :param tag_prefix_list: (experimental) Select images that have ALL the given prefixes in their tag. Only if tagStatus == TagStatus.Tagged
        :param tag_status: (experimental) Select images based on tags. Only one rule is allowed to select untagged images, and it must have the highest rulePriority. Default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise

        :stability: experimental
        """
        rule = LifecycleRule(
            description=description,
            max_image_age=max_image_age,
            max_image_count=max_image_count,
            rule_priority=rule_priority,
            tag_prefix_list=tag_prefix_list,
            tag_status=tag_status,
        )

        return jsii.invoke(self, "addLifecycleRule", [rule])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        """(experimental) Add a policy statement to the repository's resource policy.

        :param statement: -

        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        """(experimental) The ARN of the repository.

        :stability: experimental
        """
        return jsii.get(self, "repositoryArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        """(experimental) The name of the repository.

        :stability: experimental
        """
        return jsii.get(self, "repositoryName")


__all__ = [
    "AuthorizationToken",
    "CfnPublicRepository",
    "CfnPublicRepositoryProps",
    "CfnRepository",
    "CfnRepositoryProps",
    "IRepository",
    "LifecycleRule",
    "OnCloudTrailImagePushedOptions",
    "OnImageScanCompletedOptions",
    "PublicGalleryAuthorizationToken",
    "Repository",
    "RepositoryAttributes",
    "RepositoryBase",
    "RepositoryProps",
    "TagStatus",
]

publication.publish()
