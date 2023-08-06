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
class CfnApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnApplication",
):
    """A CloudFormation ``AWS::ServiceCatalogAppRegistry::Application``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html
    :cloudformationResource: AWS::ServiceCatalogAppRegistry::Application
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """Create a new ``AWS::ServiceCatalogAppRegistry::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::ServiceCatalogAppRegistry::Application.Name``.
        :param description: ``AWS::ServiceCatalogAppRegistry::Application.Description``.
        :param tags: ``AWS::ServiceCatalogAppRegistry::Application.Tags``.
        """
        props = CfnApplicationProps(name=name, description=description, tags=tags)

        jsii.create(CfnApplication, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::ServiceCatalogAppRegistry::Application.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::Application.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ServiceCatalogAppRegistry::Application.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description", "tags": "tags"},
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ServiceCatalogAppRegistry::Application``.

        :param name: ``AWS::ServiceCatalogAppRegistry::Application.Name``.
        :param description: ``AWS::ServiceCatalogAppRegistry::Application.Description``.
        :param tags: ``AWS::ServiceCatalogAppRegistry::Application.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::Application.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ServiceCatalogAppRegistry::Application.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """``AWS::ServiceCatalogAppRegistry::Application.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-application.html#cfn-servicecatalogappregistry-application-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAttributeGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnAttributeGroup",
):
    """A CloudFormation ``AWS::ServiceCatalogAppRegistry::AttributeGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html
    :cloudformationResource: AWS::ServiceCatalogAppRegistry::AttributeGroup
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        attributes: typing.Union["CfnAttributeGroup.AttributesProperty", _IResolvable_a771d0ef],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """Create a new ``AWS::ServiceCatalogAppRegistry::AttributeGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param attributes: ``AWS::ServiceCatalogAppRegistry::AttributeGroup.Attributes``.
        :param name: ``AWS::ServiceCatalogAppRegistry::AttributeGroup.Name``.
        :param description: ``AWS::ServiceCatalogAppRegistry::AttributeGroup.Description``.
        :param tags: ``AWS::ServiceCatalogAppRegistry::AttributeGroup.Tags``.
        """
        props = CfnAttributeGroupProps(
            attributes=attributes, name=name, description=description, tags=tags
        )

        jsii.create(CfnAttributeGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Union["CfnAttributeGroup.AttributesProperty", _IResolvable_a771d0ef]:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroup.Attributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-attributes
        """
        return jsii.get(self, "attributes")

    @attributes.setter # type: ignore
    def attributes(
        self,
        value: typing.Union["CfnAttributeGroup.AttributesProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "attributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroup.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_servicecatalogappregistry.CfnAttributeGroup.AttributesProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class AttributesProperty:
        def __init__(self) -> None:
            """
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalogappregistry-attributegroup-attributes.html
            """
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnAttributeGroupAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnAttributeGroupAssociation",
):
    """A CloudFormation ``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html
    :cloudformationResource: AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application: builtins.str,
        attribute_group: builtins.str,
    ) -> None:
        """Create a new ``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application: ``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.Application``.
        :param attribute_group: ``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.AttributeGroup``.
        """
        props = CfnAttributeGroupAssociationProps(
            application=application, attribute_group=attribute_group
        )

        jsii.create(CfnAttributeGroupAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrApplicationArn")
    def attr_application_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: ApplicationArn
        """
        return jsii.get(self, "attrApplicationArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrAttributeGroupArn")
    def attr_attribute_group_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: AttributeGroupArn
        """
        return jsii.get(self, "attrAttributeGroupArn")

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
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.Application``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html#cfn-servicecatalogappregistry-attributegroupassociation-application
        """
        return jsii.get(self, "application")

    @application.setter # type: ignore
    def application(self, value: builtins.str) -> None:
        jsii.set(self, "application", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attributeGroup")
    def attribute_group(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.AttributeGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html#cfn-servicecatalogappregistry-attributegroupassociation-attributegroup
        """
        return jsii.get(self, "attributeGroup")

    @attribute_group.setter # type: ignore
    def attribute_group(self, value: builtins.str) -> None:
        jsii.set(self, "attributeGroup", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnAttributeGroupAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"application": "application", "attribute_group": "attributeGroup"},
)
class CfnAttributeGroupAssociationProps:
    def __init__(
        self,
        *,
        application: builtins.str,
        attribute_group: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation``.

        :param application: ``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.Application``.
        :param attribute_group: ``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.AttributeGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application": application,
            "attribute_group": attribute_group,
        }

    @builtins.property
    def application(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.Application``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html#cfn-servicecatalogappregistry-attributegroupassociation-application
        """
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return result

    @builtins.property
    def attribute_group(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroupAssociation.AttributeGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroupassociation.html#cfn-servicecatalogappregistry-attributegroupassociation-attributegroup
        """
        result = self._values.get("attribute_group")
        assert result is not None, "Required property 'attribute_group' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAttributeGroupAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnAttributeGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "name": "name",
        "description": "description",
        "tags": "tags",
    },
)
class CfnAttributeGroupProps:
    def __init__(
        self,
        *,
        attributes: typing.Union[CfnAttributeGroup.AttributesProperty, _IResolvable_a771d0ef],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ServiceCatalogAppRegistry::AttributeGroup``.

        :param attributes: ``AWS::ServiceCatalogAppRegistry::AttributeGroup.Attributes``.
        :param name: ``AWS::ServiceCatalogAppRegistry::AttributeGroup.Name``.
        :param description: ``AWS::ServiceCatalogAppRegistry::AttributeGroup.Description``.
        :param tags: ``AWS::ServiceCatalogAppRegistry::AttributeGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "attributes": attributes,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def attributes(
        self,
    ) -> typing.Union[CfnAttributeGroup.AttributesProperty, _IResolvable_a771d0ef]:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroup.Attributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-attributes
        """
        result = self._values.get("attributes")
        assert result is not None, "Required property 'attributes' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroup.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """``AWS::ServiceCatalogAppRegistry::AttributeGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-attributegroup.html#cfn-servicecatalogappregistry-attributegroup-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAttributeGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResourceAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnResourceAssociation",
):
    """A CloudFormation ``AWS::ServiceCatalogAppRegistry::ResourceAssociation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html
    :cloudformationResource: AWS::ServiceCatalogAppRegistry::ResourceAssociation
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application: builtins.str,
        resource: builtins.str,
        resource_type: builtins.str,
    ) -> None:
        """Create a new ``AWS::ServiceCatalogAppRegistry::ResourceAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application: ``AWS::ServiceCatalogAppRegistry::ResourceAssociation.Application``.
        :param resource: ``AWS::ServiceCatalogAppRegistry::ResourceAssociation.Resource``.
        :param resource_type: ``AWS::ServiceCatalogAppRegistry::ResourceAssociation.ResourceType``.
        """
        props = CfnResourceAssociationProps(
            application=application, resource=resource, resource_type=resource_type
        )

        jsii.create(CfnResourceAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrApplicationArn")
    def attr_application_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: ApplicationArn
        """
        return jsii.get(self, "attrApplicationArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        """
        :cloudformationAttribute: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrResourceArn")
    def attr_resource_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: ResourceArn
        """
        return jsii.get(self, "attrResourceArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::ResourceAssociation.Application``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-application
        """
        return jsii.get(self, "application")

    @application.setter # type: ignore
    def application(self, value: builtins.str) -> None:
        jsii.set(self, "application", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::ResourceAssociation.Resource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-resource
        """
        return jsii.get(self, "resource")

    @resource.setter # type: ignore
    def resource(self, value: builtins.str) -> None:
        jsii.set(self, "resource", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::ResourceAssociation.ResourceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-resourcetype
        """
        return jsii.get(self, "resourceType")

    @resource_type.setter # type: ignore
    def resource_type(self, value: builtins.str) -> None:
        jsii.set(self, "resourceType", value)


@jsii.data_type(
    jsii_type="monocdk.aws_servicecatalogappregistry.CfnResourceAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "resource": "resource",
        "resource_type": "resourceType",
    },
)
class CfnResourceAssociationProps:
    def __init__(
        self,
        *,
        application: builtins.str,
        resource: builtins.str,
        resource_type: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::ServiceCatalogAppRegistry::ResourceAssociation``.

        :param application: ``AWS::ServiceCatalogAppRegistry::ResourceAssociation.Application``.
        :param resource: ``AWS::ServiceCatalogAppRegistry::ResourceAssociation.Resource``.
        :param resource_type: ``AWS::ServiceCatalogAppRegistry::ResourceAssociation.ResourceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "application": application,
            "resource": resource,
            "resource_type": resource_type,
        }

    @builtins.property
    def application(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::ResourceAssociation.Application``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-application
        """
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return result

    @builtins.property
    def resource(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::ResourceAssociation.Resource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-resource
        """
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return result

    @builtins.property
    def resource_type(self) -> builtins.str:
        """``AWS::ServiceCatalogAppRegistry::ResourceAssociation.ResourceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalogappregistry-resourceassociation.html#cfn-servicecatalogappregistry-resourceassociation-resourcetype
        """
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
    "CfnAttributeGroup",
    "CfnAttributeGroupAssociation",
    "CfnAttributeGroupAssociationProps",
    "CfnAttributeGroupProps",
    "CfnResourceAssociation",
    "CfnResourceAssociationProps",
]

publication.publish()
