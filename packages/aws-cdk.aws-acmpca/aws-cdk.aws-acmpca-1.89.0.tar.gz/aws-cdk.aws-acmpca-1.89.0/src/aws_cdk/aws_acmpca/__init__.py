"""
# AWS::ACMPCA Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_acmpca as acmpca
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
import constructs


class CertificateAuthority(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CertificateAuthority",
):
    """(experimental) Defines a Certificate for ACMPCA.

    :stability: experimental
    :resource: AWS::ACMPCA::CertificateAuthority
    """

    @jsii.member(jsii_name="fromCertificateAuthorityArn")
    @builtins.classmethod
    def from_certificate_authority_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        certificate_authority_arn: builtins.str,
    ) -> "ICertificateAuthority":
        """(experimental) Import an existing Certificate given an ARN.

        :param scope: -
        :param id: -
        :param certificate_authority_arn: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCertificateAuthorityArn", [scope, id, certificate_authority_arn])


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCertificate(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificate",
):
    """A CloudFormation ``AWS::ACMPCA::Certificate``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html
    :cloudformationResource: AWS::ACMPCA::Certificate
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        certificate_authority_arn: builtins.str,
        certificate_signing_request: builtins.str,
        signing_algorithm: builtins.str,
        validity: typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ValidityProperty"],
        api_passthrough: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ApiPassthroughProperty"]] = None,
        template_arn: typing.Optional[builtins.str] = None,
        validity_not_before: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ValidityProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::ACMPCA::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate_authority_arn: ``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.
        :param certificate_signing_request: ``AWS::ACMPCA::Certificate.CertificateSigningRequest``.
        :param signing_algorithm: ``AWS::ACMPCA::Certificate.SigningAlgorithm``.
        :param validity: ``AWS::ACMPCA::Certificate.Validity``.
        :param api_passthrough: ``AWS::ACMPCA::Certificate.ApiPassthrough``.
        :param template_arn: ``AWS::ACMPCA::Certificate.TemplateArn``.
        :param validity_not_before: ``AWS::ACMPCA::Certificate.ValidityNotBefore``.
        """
        props = CfnCertificateProps(
            certificate_authority_arn=certificate_authority_arn,
            certificate_signing_request=certificate_signing_request,
            signing_algorithm=signing_algorithm,
            validity=validity,
            api_passthrough=api_passthrough,
            template_arn=template_arn,
            validity_not_before=validity_not_before,
        )

        jsii.create(CfnCertificate, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrCertificate")
    def attr_certificate(self) -> builtins.str:
        """
        :cloudformationAttribute: Certificate
        """
        return jsii.get(self, "attrCertificate")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificateauthorityarn
        """
        return jsii.get(self, "certificateAuthorityArn")

    @certificate_authority_arn.setter # type: ignore
    def certificate_authority_arn(self, value: builtins.str) -> None:
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateSigningRequest")
    def certificate_signing_request(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.CertificateSigningRequest``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificatesigningrequest
        """
        return jsii.get(self, "certificateSigningRequest")

    @certificate_signing_request.setter # type: ignore
    def certificate_signing_request(self, value: builtins.str) -> None:
        jsii.set(self, "certificateSigningRequest", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.SigningAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-signingalgorithm
        """
        return jsii.get(self, "signingAlgorithm")

    @signing_algorithm.setter # type: ignore
    def signing_algorithm(self, value: builtins.str) -> None:
        jsii.set(self, "signingAlgorithm", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="validity")
    def validity(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ValidityProperty"]:
        """``AWS::ACMPCA::Certificate.Validity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validity
        """
        return jsii.get(self, "validity")

    @validity.setter # type: ignore
    def validity(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ValidityProperty"],
    ) -> None:
        jsii.set(self, "validity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiPassthrough")
    def api_passthrough(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ApiPassthroughProperty"]]:
        """``AWS::ACMPCA::Certificate.ApiPassthrough``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-apipassthrough
        """
        return jsii.get(self, "apiPassthrough")

    @api_passthrough.setter # type: ignore
    def api_passthrough(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ApiPassthroughProperty"]],
    ) -> None:
        jsii.set(self, "apiPassthrough", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateArn")
    def template_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::Certificate.TemplateArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-templatearn
        """
        return jsii.get(self, "templateArn")

    @template_arn.setter # type: ignore
    def template_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "templateArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="validityNotBefore")
    def validity_not_before(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ValidityProperty"]]:
        """``AWS::ACMPCA::Certificate.ValidityNotBefore``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validitynotbefore
        """
        return jsii.get(self, "validityNotBefore")

    @validity_not_before.setter # type: ignore
    def validity_not_before(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ValidityProperty"]],
    ) -> None:
        jsii.set(self, "validityNotBefore", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.ApiPassthroughProperty",
        jsii_struct_bases=[],
        name_mapping={"extensions": "extensions", "subject": "subject"},
    )
    class ApiPassthroughProperty:
        def __init__(
            self,
            *,
            extensions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ExtensionsProperty"]] = None,
            subject: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.SubjectProperty"]] = None,
        ) -> None:
            """
            :param extensions: ``CfnCertificate.ApiPassthroughProperty.Extensions``.
            :param subject: ``CfnCertificate.ApiPassthroughProperty.Subject``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-apipassthrough.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if extensions is not None:
                self._values["extensions"] = extensions
            if subject is not None:
                self._values["subject"] = subject

        @builtins.property
        def extensions(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ExtensionsProperty"]]:
            """``CfnCertificate.ApiPassthroughProperty.Extensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-apipassthrough.html#cfn-acmpca-certificate-apipassthrough-extensions
            """
            result = self._values.get("extensions")
            return result

        @builtins.property
        def subject(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.SubjectProperty"]]:
            """``CfnCertificate.ApiPassthroughProperty.Subject``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-apipassthrough.html#cfn-acmpca-certificate-apipassthrough-subject
            """
            result = self._values.get("subject")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiPassthroughProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.CertificatePolicyListProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_policy_list": "certificatePolicyList"},
    )
    class CertificatePolicyListProperty:
        def __init__(
            self,
            *,
            certificate_policy_list: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.PolicyInformationProperty"]]]] = None,
        ) -> None:
            """
            :param certificate_policy_list: ``CfnCertificate.CertificatePolicyListProperty.CertificatePolicyList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-certificatepolicylist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if certificate_policy_list is not None:
                self._values["certificate_policy_list"] = certificate_policy_list

        @builtins.property
        def certificate_policy_list(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.PolicyInformationProperty"]]]]:
            """``CfnCertificate.CertificatePolicyListProperty.CertificatePolicyList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-certificatepolicylist.html#cfn-acmpca-certificate-certificatepolicylist-certificatepolicylist
            """
            result = self._values.get("certificate_policy_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificatePolicyListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.EdiPartyNameProperty",
        jsii_struct_bases=[],
        name_mapping={"name_assigner": "nameAssigner", "party_name": "partyName"},
    )
    class EdiPartyNameProperty:
        def __init__(
            self,
            *,
            name_assigner: builtins.str,
            party_name: builtins.str,
        ) -> None:
            """
            :param name_assigner: ``CfnCertificate.EdiPartyNameProperty.NameAssigner``.
            :param party_name: ``CfnCertificate.EdiPartyNameProperty.PartyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-edipartyname.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name_assigner": name_assigner,
                "party_name": party_name,
            }

        @builtins.property
        def name_assigner(self) -> builtins.str:
            """``CfnCertificate.EdiPartyNameProperty.NameAssigner``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-edipartyname.html#cfn-acmpca-certificate-edipartyname-nameassigner
            """
            result = self._values.get("name_assigner")
            assert result is not None, "Required property 'name_assigner' is missing"
            return result

        @builtins.property
        def party_name(self) -> builtins.str:
            """``CfnCertificate.EdiPartyNameProperty.PartyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-edipartyname.html#cfn-acmpca-certificate-edipartyname-partyname
            """
            result = self._values.get("party_name")
            assert result is not None, "Required property 'party_name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EdiPartyNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.ExtendedKeyUsageListProperty",
        jsii_struct_bases=[],
        name_mapping={"extended_key_usage_list": "extendedKeyUsageList"},
    )
    class ExtendedKeyUsageListProperty:
        def __init__(
            self,
            *,
            extended_key_usage_list: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ExtendedKeyUsageProperty"]]]] = None,
        ) -> None:
            """
            :param extended_key_usage_list: ``CfnCertificate.ExtendedKeyUsageListProperty.ExtendedKeyUsageList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusagelist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if extended_key_usage_list is not None:
                self._values["extended_key_usage_list"] = extended_key_usage_list

        @builtins.property
        def extended_key_usage_list(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ExtendedKeyUsageProperty"]]]]:
            """``CfnCertificate.ExtendedKeyUsageListProperty.ExtendedKeyUsageList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusagelist.html#cfn-acmpca-certificate-extendedkeyusagelist-extendedkeyusagelist
            """
            result = self._values.get("extended_key_usage_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtendedKeyUsageListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.ExtendedKeyUsageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "extended_key_usage_object_identifier": "extendedKeyUsageObjectIdentifier",
            "extended_key_usage_type": "extendedKeyUsageType",
        },
    )
    class ExtendedKeyUsageProperty:
        def __init__(
            self,
            *,
            extended_key_usage_object_identifier: typing.Optional[builtins.str] = None,
            extended_key_usage_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param extended_key_usage_object_identifier: ``CfnCertificate.ExtendedKeyUsageProperty.ExtendedKeyUsageObjectIdentifier``.
            :param extended_key_usage_type: ``CfnCertificate.ExtendedKeyUsageProperty.ExtendedKeyUsageType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusage.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if extended_key_usage_object_identifier is not None:
                self._values["extended_key_usage_object_identifier"] = extended_key_usage_object_identifier
            if extended_key_usage_type is not None:
                self._values["extended_key_usage_type"] = extended_key_usage_type

        @builtins.property
        def extended_key_usage_object_identifier(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.ExtendedKeyUsageProperty.ExtendedKeyUsageObjectIdentifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusage.html#cfn-acmpca-certificate-extendedkeyusage-extendedkeyusageobjectidentifier
            """
            result = self._values.get("extended_key_usage_object_identifier")
            return result

        @builtins.property
        def extended_key_usage_type(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.ExtendedKeyUsageProperty.ExtendedKeyUsageType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusage.html#cfn-acmpca-certificate-extendedkeyusage-extendedkeyusagetype
            """
            result = self._values.get("extended_key_usage_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtendedKeyUsageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.ExtensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_policies": "certificatePolicies",
            "extended_key_usage": "extendedKeyUsage",
            "key_usage": "keyUsage",
            "subject_alternative_names": "subjectAlternativeNames",
        },
    )
    class ExtensionsProperty:
        def __init__(
            self,
            *,
            certificate_policies: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.CertificatePolicyListProperty"]] = None,
            extended_key_usage: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ExtendedKeyUsageListProperty"]] = None,
            key_usage: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.KeyUsageProperty"]] = None,
            subject_alternative_names: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.GeneralNameListProperty"]] = None,
        ) -> None:
            """
            :param certificate_policies: ``CfnCertificate.ExtensionsProperty.CertificatePolicies``.
            :param extended_key_usage: ``CfnCertificate.ExtensionsProperty.ExtendedKeyUsage``.
            :param key_usage: ``CfnCertificate.ExtensionsProperty.KeyUsage``.
            :param subject_alternative_names: ``CfnCertificate.ExtensionsProperty.SubjectAlternativeNames``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if certificate_policies is not None:
                self._values["certificate_policies"] = certificate_policies
            if extended_key_usage is not None:
                self._values["extended_key_usage"] = extended_key_usage
            if key_usage is not None:
                self._values["key_usage"] = key_usage
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names

        @builtins.property
        def certificate_policies(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.CertificatePolicyListProperty"]]:
            """``CfnCertificate.ExtensionsProperty.CertificatePolicies``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-certificatepolicies
            """
            result = self._values.get("certificate_policies")
            return result

        @builtins.property
        def extended_key_usage(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ExtendedKeyUsageListProperty"]]:
            """``CfnCertificate.ExtensionsProperty.ExtendedKeyUsage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-extendedkeyusage
            """
            result = self._values.get("extended_key_usage")
            return result

        @builtins.property
        def key_usage(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.KeyUsageProperty"]]:
            """``CfnCertificate.ExtensionsProperty.KeyUsage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-keyusage
            """
            result = self._values.get("key_usage")
            return result

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.GeneralNameListProperty"]]:
            """``CfnCertificate.ExtensionsProperty.SubjectAlternativeNames``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-subjectalternativenames
            """
            result = self._values.get("subject_alternative_names")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.GeneralNameListProperty",
        jsii_struct_bases=[],
        name_mapping={"general_name_list": "generalNameList"},
    )
    class GeneralNameListProperty:
        def __init__(
            self,
            *,
            general_name_list: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.GeneralNameProperty"]]]] = None,
        ) -> None:
            """
            :param general_name_list: ``CfnCertificate.GeneralNameListProperty.GeneralNameList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalnamelist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if general_name_list is not None:
                self._values["general_name_list"] = general_name_list

        @builtins.property
        def general_name_list(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.GeneralNameProperty"]]]]:
            """``CfnCertificate.GeneralNameListProperty.GeneralNameList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalnamelist.html#cfn-acmpca-certificate-generalnamelist-generalnamelist
            """
            result = self._values.get("general_name_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeneralNameListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.GeneralNameProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "dns_name": "dnsName",
            "edi_party_name": "ediPartyName",
            "ip_address": "ipAddress",
            "other_name": "otherName",
            "registered_id": "registeredId",
            "rfc822_name": "rfc822Name",
            "uniform_resource_identifier": "uniformResourceIdentifier",
        },
    )
    class GeneralNameProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.SubjectProperty"]] = None,
            dns_name: typing.Optional[builtins.str] = None,
            edi_party_name: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.EdiPartyNameProperty"]] = None,
            ip_address: typing.Optional[builtins.str] = None,
            other_name: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.OtherNameProperty"]] = None,
            registered_id: typing.Optional[builtins.str] = None,
            rfc822_name: typing.Optional[builtins.str] = None,
            uniform_resource_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param directory_name: ``CfnCertificate.GeneralNameProperty.DirectoryName``.
            :param dns_name: ``CfnCertificate.GeneralNameProperty.DnsName``.
            :param edi_party_name: ``CfnCertificate.GeneralNameProperty.EdiPartyName``.
            :param ip_address: ``CfnCertificate.GeneralNameProperty.IpAddress``.
            :param other_name: ``CfnCertificate.GeneralNameProperty.OtherName``.
            :param registered_id: ``CfnCertificate.GeneralNameProperty.RegisteredId``.
            :param rfc822_name: ``CfnCertificate.GeneralNameProperty.Rfc822Name``.
            :param uniform_resource_identifier: ``CfnCertificate.GeneralNameProperty.UniformResourceIdentifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if dns_name is not None:
                self._values["dns_name"] = dns_name
            if edi_party_name is not None:
                self._values["edi_party_name"] = edi_party_name
            if ip_address is not None:
                self._values["ip_address"] = ip_address
            if other_name is not None:
                self._values["other_name"] = other_name
            if registered_id is not None:
                self._values["registered_id"] = registered_id
            if rfc822_name is not None:
                self._values["rfc822_name"] = rfc822_name
            if uniform_resource_identifier is not None:
                self._values["uniform_resource_identifier"] = uniform_resource_identifier

        @builtins.property
        def directory_name(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.SubjectProperty"]]:
            """``CfnCertificate.GeneralNameProperty.DirectoryName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-directoryname
            """
            result = self._values.get("directory_name")
            return result

        @builtins.property
        def dns_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.GeneralNameProperty.DnsName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-dnsname
            """
            result = self._values.get("dns_name")
            return result

        @builtins.property
        def edi_party_name(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.EdiPartyNameProperty"]]:
            """``CfnCertificate.GeneralNameProperty.EdiPartyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-edipartyname
            """
            result = self._values.get("edi_party_name")
            return result

        @builtins.property
        def ip_address(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.GeneralNameProperty.IpAddress``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-ipaddress
            """
            result = self._values.get("ip_address")
            return result

        @builtins.property
        def other_name(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.OtherNameProperty"]]:
            """``CfnCertificate.GeneralNameProperty.OtherName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-othername
            """
            result = self._values.get("other_name")
            return result

        @builtins.property
        def registered_id(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.GeneralNameProperty.RegisteredId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-registeredid
            """
            result = self._values.get("registered_id")
            return result

        @builtins.property
        def rfc822_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.GeneralNameProperty.Rfc822Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-rfc822name
            """
            result = self._values.get("rfc822_name")
            return result

        @builtins.property
        def uniform_resource_identifier(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.GeneralNameProperty.UniformResourceIdentifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-uniformresourceidentifier
            """
            result = self._values.get("uniform_resource_identifier")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeneralNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.KeyUsageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crl_sign": "crlSign",
            "data_encipherment": "dataEncipherment",
            "decipher_only": "decipherOnly",
            "digital_signature": "digitalSignature",
            "encipher_only": "encipherOnly",
            "key_agreement": "keyAgreement",
            "key_cert_sign": "keyCertSign",
            "key_encipherment": "keyEncipherment",
            "non_repudiation": "nonRepudiation",
        },
    )
    class KeyUsageProperty:
        def __init__(
            self,
            *,
            crl_sign: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            data_encipherment: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            decipher_only: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            digital_signature: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            encipher_only: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            key_agreement: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            key_cert_sign: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            key_encipherment: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            non_repudiation: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param crl_sign: ``CfnCertificate.KeyUsageProperty.CRLSign``.
            :param data_encipherment: ``CfnCertificate.KeyUsageProperty.DataEncipherment``.
            :param decipher_only: ``CfnCertificate.KeyUsageProperty.DecipherOnly``.
            :param digital_signature: ``CfnCertificate.KeyUsageProperty.DigitalSignature``.
            :param encipher_only: ``CfnCertificate.KeyUsageProperty.EncipherOnly``.
            :param key_agreement: ``CfnCertificate.KeyUsageProperty.KeyAgreement``.
            :param key_cert_sign: ``CfnCertificate.KeyUsageProperty.KeyCertSign``.
            :param key_encipherment: ``CfnCertificate.KeyUsageProperty.KeyEncipherment``.
            :param non_repudiation: ``CfnCertificate.KeyUsageProperty.NonRepudiation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if crl_sign is not None:
                self._values["crl_sign"] = crl_sign
            if data_encipherment is not None:
                self._values["data_encipherment"] = data_encipherment
            if decipher_only is not None:
                self._values["decipher_only"] = decipher_only
            if digital_signature is not None:
                self._values["digital_signature"] = digital_signature
            if encipher_only is not None:
                self._values["encipher_only"] = encipher_only
            if key_agreement is not None:
                self._values["key_agreement"] = key_agreement
            if key_cert_sign is not None:
                self._values["key_cert_sign"] = key_cert_sign
            if key_encipherment is not None:
                self._values["key_encipherment"] = key_encipherment
            if non_repudiation is not None:
                self._values["non_repudiation"] = non_repudiation

        @builtins.property
        def crl_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificate.KeyUsageProperty.CRLSign``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-crlsign
            """
            result = self._values.get("crl_sign")
            return result

        @builtins.property
        def data_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificate.KeyUsageProperty.DataEncipherment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-dataencipherment
            """
            result = self._values.get("data_encipherment")
            return result

        @builtins.property
        def decipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificate.KeyUsageProperty.DecipherOnly``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-decipheronly
            """
            result = self._values.get("decipher_only")
            return result

        @builtins.property
        def digital_signature(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificate.KeyUsageProperty.DigitalSignature``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-digitalsignature
            """
            result = self._values.get("digital_signature")
            return result

        @builtins.property
        def encipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificate.KeyUsageProperty.EncipherOnly``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-encipheronly
            """
            result = self._values.get("encipher_only")
            return result

        @builtins.property
        def key_agreement(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificate.KeyUsageProperty.KeyAgreement``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-keyagreement
            """
            result = self._values.get("key_agreement")
            return result

        @builtins.property
        def key_cert_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificate.KeyUsageProperty.KeyCertSign``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-keycertsign
            """
            result = self._values.get("key_cert_sign")
            return result

        @builtins.property
        def key_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificate.KeyUsageProperty.KeyEncipherment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-keyencipherment
            """
            result = self._values.get("key_encipherment")
            return result

        @builtins.property
        def non_repudiation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificate.KeyUsageProperty.NonRepudiation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-nonrepudiation
            """
            result = self._values.get("non_repudiation")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyUsageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.OtherNameProperty",
        jsii_struct_bases=[],
        name_mapping={"type_id": "typeId", "value": "value"},
    )
    class OtherNameProperty:
        def __init__(self, *, type_id: builtins.str, value: builtins.str) -> None:
            """
            :param type_id: ``CfnCertificate.OtherNameProperty.TypeId``.
            :param value: ``CfnCertificate.OtherNameProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-othername.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type_id": type_id,
                "value": value,
            }

        @builtins.property
        def type_id(self) -> builtins.str:
            """``CfnCertificate.OtherNameProperty.TypeId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-othername.html#cfn-acmpca-certificate-othername-typeid
            """
            result = self._values.get("type_id")
            assert result is not None, "Required property 'type_id' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnCertificate.OtherNameProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-othername.html#cfn-acmpca-certificate-othername-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OtherNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.PolicyInformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cert_policy_id": "certPolicyId",
            "policy_qualifiers": "policyQualifiers",
        },
    )
    class PolicyInformationProperty:
        def __init__(
            self,
            *,
            cert_policy_id: builtins.str,
            policy_qualifiers: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.PolicyQualifierInfoListProperty"]] = None,
        ) -> None:
            """
            :param cert_policy_id: ``CfnCertificate.PolicyInformationProperty.CertPolicyId``.
            :param policy_qualifiers: ``CfnCertificate.PolicyInformationProperty.PolicyQualifiers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyinformation.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "cert_policy_id": cert_policy_id,
            }
            if policy_qualifiers is not None:
                self._values["policy_qualifiers"] = policy_qualifiers

        @builtins.property
        def cert_policy_id(self) -> builtins.str:
            """``CfnCertificate.PolicyInformationProperty.CertPolicyId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyinformation.html#cfn-acmpca-certificate-policyinformation-certpolicyid
            """
            result = self._values.get("cert_policy_id")
            assert result is not None, "Required property 'cert_policy_id' is missing"
            return result

        @builtins.property
        def policy_qualifiers(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.PolicyQualifierInfoListProperty"]]:
            """``CfnCertificate.PolicyInformationProperty.PolicyQualifiers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyinformation.html#cfn-acmpca-certificate-policyinformation-policyqualifiers
            """
            result = self._values.get("policy_qualifiers")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyInformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.PolicyQualifierInfoListProperty",
        jsii_struct_bases=[],
        name_mapping={"policy_qualifier_info_list": "policyQualifierInfoList"},
    )
    class PolicyQualifierInfoListProperty:
        def __init__(
            self,
            *,
            policy_qualifier_info_list: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.PolicyQualifierInfoProperty"]]]] = None,
        ) -> None:
            """
            :param policy_qualifier_info_list: ``CfnCertificate.PolicyQualifierInfoListProperty.PolicyQualifierInfoList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfolist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if policy_qualifier_info_list is not None:
                self._values["policy_qualifier_info_list"] = policy_qualifier_info_list

        @builtins.property
        def policy_qualifier_info_list(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.PolicyQualifierInfoProperty"]]]]:
            """``CfnCertificate.PolicyQualifierInfoListProperty.PolicyQualifierInfoList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfolist.html#cfn-acmpca-certificate-policyqualifierinfolist-policyqualifierinfolist
            """
            result = self._values.get("policy_qualifier_info_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyQualifierInfoListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.PolicyQualifierInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_qualifier_id": "policyQualifierId",
            "qualifier": "qualifier",
        },
    )
    class PolicyQualifierInfoProperty:
        def __init__(
            self,
            *,
            policy_qualifier_id: builtins.str,
            qualifier: typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.QualifierProperty"],
        ) -> None:
            """
            :param policy_qualifier_id: ``CfnCertificate.PolicyQualifierInfoProperty.PolicyQualifierId``.
            :param qualifier: ``CfnCertificate.PolicyQualifierInfoProperty.Qualifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfo.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "policy_qualifier_id": policy_qualifier_id,
                "qualifier": qualifier,
            }

        @builtins.property
        def policy_qualifier_id(self) -> builtins.str:
            """``CfnCertificate.PolicyQualifierInfoProperty.PolicyQualifierId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfo.html#cfn-acmpca-certificate-policyqualifierinfo-policyqualifierid
            """
            result = self._values.get("policy_qualifier_id")
            assert result is not None, "Required property 'policy_qualifier_id' is missing"
            return result

        @builtins.property
        def qualifier(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.QualifierProperty"]:
            """``CfnCertificate.PolicyQualifierInfoProperty.Qualifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfo.html#cfn-acmpca-certificate-policyqualifierinfo-qualifier
            """
            result = self._values.get("qualifier")
            assert result is not None, "Required property 'qualifier' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyQualifierInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.QualifierProperty",
        jsii_struct_bases=[],
        name_mapping={"cps_uri": "cpsUri"},
    )
    class QualifierProperty:
        def __init__(self, *, cps_uri: builtins.str) -> None:
            """
            :param cps_uri: ``CfnCertificate.QualifierProperty.CpsUri``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-qualifier.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "cps_uri": cps_uri,
            }

        @builtins.property
        def cps_uri(self) -> builtins.str:
            """``CfnCertificate.QualifierProperty.CpsUri``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-qualifier.html#cfn-acmpca-certificate-qualifier-cpsuri
            """
            result = self._values.get("cps_uri")
            assert result is not None, "Required property 'cps_uri' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QualifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.SubjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "common_name": "commonName",
            "country": "country",
            "distinguished_name_qualifier": "distinguishedNameQualifier",
            "generation_qualifier": "generationQualifier",
            "given_name": "givenName",
            "initials": "initials",
            "locality": "locality",
            "organization": "organization",
            "organizational_unit": "organizationalUnit",
            "pseudonym": "pseudonym",
            "serial_number": "serialNumber",
            "state": "state",
            "surname": "surname",
            "title": "title",
        },
    )
    class SubjectProperty:
        def __init__(
            self,
            *,
            common_name: typing.Optional[builtins.str] = None,
            country: typing.Optional[builtins.str] = None,
            distinguished_name_qualifier: typing.Optional[builtins.str] = None,
            generation_qualifier: typing.Optional[builtins.str] = None,
            given_name: typing.Optional[builtins.str] = None,
            initials: typing.Optional[builtins.str] = None,
            locality: typing.Optional[builtins.str] = None,
            organization: typing.Optional[builtins.str] = None,
            organizational_unit: typing.Optional[builtins.str] = None,
            pseudonym: typing.Optional[builtins.str] = None,
            serial_number: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
            surname: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param common_name: ``CfnCertificate.SubjectProperty.CommonName``.
            :param country: ``CfnCertificate.SubjectProperty.Country``.
            :param distinguished_name_qualifier: ``CfnCertificate.SubjectProperty.DistinguishedNameQualifier``.
            :param generation_qualifier: ``CfnCertificate.SubjectProperty.GenerationQualifier``.
            :param given_name: ``CfnCertificate.SubjectProperty.GivenName``.
            :param initials: ``CfnCertificate.SubjectProperty.Initials``.
            :param locality: ``CfnCertificate.SubjectProperty.Locality``.
            :param organization: ``CfnCertificate.SubjectProperty.Organization``.
            :param organizational_unit: ``CfnCertificate.SubjectProperty.OrganizationalUnit``.
            :param pseudonym: ``CfnCertificate.SubjectProperty.Pseudonym``.
            :param serial_number: ``CfnCertificate.SubjectProperty.SerialNumber``.
            :param state: ``CfnCertificate.SubjectProperty.State``.
            :param surname: ``CfnCertificate.SubjectProperty.Surname``.
            :param title: ``CfnCertificate.SubjectProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if common_name is not None:
                self._values["common_name"] = common_name
            if country is not None:
                self._values["country"] = country
            if distinguished_name_qualifier is not None:
                self._values["distinguished_name_qualifier"] = distinguished_name_qualifier
            if generation_qualifier is not None:
                self._values["generation_qualifier"] = generation_qualifier
            if given_name is not None:
                self._values["given_name"] = given_name
            if initials is not None:
                self._values["initials"] = initials
            if locality is not None:
                self._values["locality"] = locality
            if organization is not None:
                self._values["organization"] = organization
            if organizational_unit is not None:
                self._values["organizational_unit"] = organizational_unit
            if pseudonym is not None:
                self._values["pseudonym"] = pseudonym
            if serial_number is not None:
                self._values["serial_number"] = serial_number
            if state is not None:
                self._values["state"] = state
            if surname is not None:
                self._values["surname"] = surname
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def common_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.CommonName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-commonname
            """
            result = self._values.get("common_name")
            return result

        @builtins.property
        def country(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.Country``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-country
            """
            result = self._values.get("country")
            return result

        @builtins.property
        def distinguished_name_qualifier(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.DistinguishedNameQualifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-distinguishednamequalifier
            """
            result = self._values.get("distinguished_name_qualifier")
            return result

        @builtins.property
        def generation_qualifier(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.GenerationQualifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-generationqualifier
            """
            result = self._values.get("generation_qualifier")
            return result

        @builtins.property
        def given_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.GivenName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-givenname
            """
            result = self._values.get("given_name")
            return result

        @builtins.property
        def initials(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.Initials``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-initials
            """
            result = self._values.get("initials")
            return result

        @builtins.property
        def locality(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.Locality``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-locality
            """
            result = self._values.get("locality")
            return result

        @builtins.property
        def organization(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.Organization``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-organization
            """
            result = self._values.get("organization")
            return result

        @builtins.property
        def organizational_unit(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.OrganizationalUnit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-organizationalunit
            """
            result = self._values.get("organizational_unit")
            return result

        @builtins.property
        def pseudonym(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.Pseudonym``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-pseudonym
            """
            result = self._values.get("pseudonym")
            return result

        @builtins.property
        def serial_number(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.SerialNumber``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-serialnumber
            """
            result = self._values.get("serial_number")
            return result

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.State``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-state
            """
            result = self._values.get("state")
            return result

        @builtins.property
        def surname(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.Surname``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-surname
            """
            result = self._values.get("surname")
            return result

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            """``CfnCertificate.SubjectProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-title
            """
            result = self._values.get("title")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.ValidityProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ValidityProperty:
        def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
            """
            :param type: ``CfnCertificate.ValidityProperty.Type``.
            :param value: ``CfnCertificate.ValidityProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnCertificate.ValidityProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html#cfn-acmpca-certificate-validity-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def value(self) -> jsii.Number:
            """``CfnCertificate.ValidityProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html#cfn-acmpca-certificate-validity-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCertificateAuthority(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority",
):
    """A CloudFormation ``AWS::ACMPCA::CertificateAuthority``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html
    :cloudformationResource: AWS::ACMPCA::CertificateAuthority
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        key_algorithm: builtins.str,
        signing_algorithm: builtins.str,
        subject: typing.Union["CfnCertificateAuthority.SubjectProperty", aws_cdk.core.IResolvable],
        type: builtins.str,
        csr_extensions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.CsrExtensionsProperty"]] = None,
        revocation_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.RevocationConfigurationProperty"]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::ACMPCA::CertificateAuthority``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key_algorithm: ``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.
        :param signing_algorithm: ``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.
        :param subject: ``AWS::ACMPCA::CertificateAuthority.Subject``.
        :param type: ``AWS::ACMPCA::CertificateAuthority.Type``.
        :param csr_extensions: ``AWS::ACMPCA::CertificateAuthority.CsrExtensions``.
        :param revocation_configuration: ``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.
        :param tags: ``AWS::ACMPCA::CertificateAuthority.Tags``.
        """
        props = CfnCertificateAuthorityProps(
            key_algorithm=key_algorithm,
            signing_algorithm=signing_algorithm,
            subject=subject,
            type=type,
            csr_extensions=csr_extensions,
            revocation_configuration=revocation_configuration,
            tags=tags,
        )

        jsii.create(CfnCertificateAuthority, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrCertificateSigningRequest")
    def attr_certificate_signing_request(self) -> builtins.str:
        """
        :cloudformationAttribute: CertificateSigningRequest
        """
        return jsii.get(self, "attrCertificateSigningRequest")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ACMPCA::CertificateAuthority.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyAlgorithm")
    def key_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keyalgorithm
        """
        return jsii.get(self, "keyAlgorithm")

    @key_algorithm.setter # type: ignore
    def key_algorithm(self, value: builtins.str) -> None:
        jsii.set(self, "keyAlgorithm", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-signingalgorithm
        """
        return jsii.get(self, "signingAlgorithm")

    @signing_algorithm.setter # type: ignore
    def signing_algorithm(self, value: builtins.str) -> None:
        jsii.set(self, "signingAlgorithm", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subject")
    def subject(
        self,
    ) -> typing.Union["CfnCertificateAuthority.SubjectProperty", aws_cdk.core.IResolvable]:
        """``AWS::ACMPCA::CertificateAuthority.Subject``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-subject
        """
        return jsii.get(self, "subject")

    @subject.setter # type: ignore
    def subject(
        self,
        value: typing.Union["CfnCertificateAuthority.SubjectProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "subject", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="csrExtensions")
    def csr_extensions(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.CsrExtensionsProperty"]]:
        """``AWS::ACMPCA::CertificateAuthority.CsrExtensions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-csrextensions
        """
        return jsii.get(self, "csrExtensions")

    @csr_extensions.setter # type: ignore
    def csr_extensions(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.CsrExtensionsProperty"]],
    ) -> None:
        jsii.set(self, "csrExtensions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="revocationConfiguration")
    def revocation_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.RevocationConfigurationProperty"]]:
        """``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-revocationconfiguration
        """
        return jsii.get(self, "revocationConfiguration")

    @revocation_configuration.setter # type: ignore
    def revocation_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.RevocationConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "revocationConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.AccessDescriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_location": "accessLocation",
            "access_method": "accessMethod",
        },
    )
    class AccessDescriptionProperty:
        def __init__(
            self,
            *,
            access_location: typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.GeneralNameProperty"],
            access_method: typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.AccessMethodProperty"],
        ) -> None:
            """
            :param access_location: ``CfnCertificateAuthority.AccessDescriptionProperty.AccessLocation``.
            :param access_method: ``CfnCertificateAuthority.AccessDescriptionProperty.AccessMethod``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessdescription.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "access_location": access_location,
                "access_method": access_method,
            }

        @builtins.property
        def access_location(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.GeneralNameProperty"]:
            """``CfnCertificateAuthority.AccessDescriptionProperty.AccessLocation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessdescription.html#cfn-acmpca-certificateauthority-accessdescription-accesslocation
            """
            result = self._values.get("access_location")
            assert result is not None, "Required property 'access_location' is missing"
            return result

        @builtins.property
        def access_method(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.AccessMethodProperty"]:
            """``CfnCertificateAuthority.AccessDescriptionProperty.AccessMethod``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessdescription.html#cfn-acmpca-certificateauthority-accessdescription-accessmethod
            """
            result = self._values.get("access_method")
            assert result is not None, "Required property 'access_method' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessDescriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.AccessMethodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_method_type": "accessMethodType",
            "custom_object_identifier": "customObjectIdentifier",
        },
    )
    class AccessMethodProperty:
        def __init__(
            self,
            *,
            access_method_type: typing.Optional[builtins.str] = None,
            custom_object_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param access_method_type: ``CfnCertificateAuthority.AccessMethodProperty.AccessMethodType``.
            :param custom_object_identifier: ``CfnCertificateAuthority.AccessMethodProperty.CustomObjectIdentifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessmethod.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if access_method_type is not None:
                self._values["access_method_type"] = access_method_type
            if custom_object_identifier is not None:
                self._values["custom_object_identifier"] = custom_object_identifier

        @builtins.property
        def access_method_type(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.AccessMethodProperty.AccessMethodType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessmethod.html#cfn-acmpca-certificateauthority-accessmethod-accessmethodtype
            """
            result = self._values.get("access_method_type")
            return result

        @builtins.property
        def custom_object_identifier(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.AccessMethodProperty.CustomObjectIdentifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessmethod.html#cfn-acmpca-certificateauthority-accessmethod-customobjectidentifier
            """
            result = self._values.get("custom_object_identifier")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessMethodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.CrlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_cname": "customCname",
            "enabled": "enabled",
            "expiration_in_days": "expirationInDays",
            "s3_bucket_name": "s3BucketName",
        },
    )
    class CrlConfigurationProperty:
        def __init__(
            self,
            *,
            custom_cname: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            expiration_in_days: typing.Optional[jsii.Number] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param custom_cname: ``CfnCertificateAuthority.CrlConfigurationProperty.CustomCname``.
            :param enabled: ``CfnCertificateAuthority.CrlConfigurationProperty.Enabled``.
            :param expiration_in_days: ``CfnCertificateAuthority.CrlConfigurationProperty.ExpirationInDays``.
            :param s3_bucket_name: ``CfnCertificateAuthority.CrlConfigurationProperty.S3BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if custom_cname is not None:
                self._values["custom_cname"] = custom_cname
            if enabled is not None:
                self._values["enabled"] = enabled
            if expiration_in_days is not None:
                self._values["expiration_in_days"] = expiration_in_days
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name

        @builtins.property
        def custom_cname(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.CustomCname``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-customcname
            """
            result = self._values.get("custom_cname")
            return result

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-enabled
            """
            result = self._values.get("enabled")
            return result

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.ExpirationInDays``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-expirationindays
            """
            result = self._values.get("expiration_in_days")
            return result

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.S3BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-s3bucketname
            """
            result = self._values.get("s3_bucket_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.CsrExtensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key_usage": "keyUsage",
            "subject_information_access": "subjectInformationAccess",
        },
    )
    class CsrExtensionsProperty:
        def __init__(
            self,
            *,
            key_usage: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.KeyUsageProperty"]] = None,
            subject_information_access: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.SubjectInformationAccessProperty"]] = None,
        ) -> None:
            """
            :param key_usage: ``CfnCertificateAuthority.CsrExtensionsProperty.KeyUsage``.
            :param subject_information_access: ``CfnCertificateAuthority.CsrExtensionsProperty.SubjectInformationAccess``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-csrextensions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if key_usage is not None:
                self._values["key_usage"] = key_usage
            if subject_information_access is not None:
                self._values["subject_information_access"] = subject_information_access

        @builtins.property
        def key_usage(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.KeyUsageProperty"]]:
            """``CfnCertificateAuthority.CsrExtensionsProperty.KeyUsage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-csrextensions.html#cfn-acmpca-certificateauthority-csrextensions-keyusage
            """
            result = self._values.get("key_usage")
            return result

        @builtins.property
        def subject_information_access(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.SubjectInformationAccessProperty"]]:
            """``CfnCertificateAuthority.CsrExtensionsProperty.SubjectInformationAccess``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-csrextensions.html#cfn-acmpca-certificateauthority-csrextensions-subjectinformationaccess
            """
            result = self._values.get("subject_information_access")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CsrExtensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.EdiPartyNameProperty",
        jsii_struct_bases=[],
        name_mapping={"name_assigner": "nameAssigner", "party_name": "partyName"},
    )
    class EdiPartyNameProperty:
        def __init__(
            self,
            *,
            name_assigner: builtins.str,
            party_name: builtins.str,
        ) -> None:
            """
            :param name_assigner: ``CfnCertificateAuthority.EdiPartyNameProperty.NameAssigner``.
            :param party_name: ``CfnCertificateAuthority.EdiPartyNameProperty.PartyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-edipartyname.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name_assigner": name_assigner,
                "party_name": party_name,
            }

        @builtins.property
        def name_assigner(self) -> builtins.str:
            """``CfnCertificateAuthority.EdiPartyNameProperty.NameAssigner``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-edipartyname.html#cfn-acmpca-certificateauthority-edipartyname-nameassigner
            """
            result = self._values.get("name_assigner")
            assert result is not None, "Required property 'name_assigner' is missing"
            return result

        @builtins.property
        def party_name(self) -> builtins.str:
            """``CfnCertificateAuthority.EdiPartyNameProperty.PartyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-edipartyname.html#cfn-acmpca-certificateauthority-edipartyname-partyname
            """
            result = self._values.get("party_name")
            assert result is not None, "Required property 'party_name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EdiPartyNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.GeneralNameProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "dns_name": "dnsName",
            "edi_party_name": "ediPartyName",
            "ip_address": "ipAddress",
            "other_name": "otherName",
            "registered_id": "registeredId",
            "rfc822_name": "rfc822Name",
            "uniform_resource_identifier": "uniformResourceIdentifier",
        },
    )
    class GeneralNameProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[typing.Union["CfnCertificateAuthority.SubjectProperty", aws_cdk.core.IResolvable]] = None,
            dns_name: typing.Optional[builtins.str] = None,
            edi_party_name: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.EdiPartyNameProperty"]] = None,
            ip_address: typing.Optional[builtins.str] = None,
            other_name: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.OtherNameProperty"]] = None,
            registered_id: typing.Optional[builtins.str] = None,
            rfc822_name: typing.Optional[builtins.str] = None,
            uniform_resource_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param directory_name: ``CfnCertificateAuthority.GeneralNameProperty.DirectoryName``.
            :param dns_name: ``CfnCertificateAuthority.GeneralNameProperty.DnsName``.
            :param edi_party_name: ``CfnCertificateAuthority.GeneralNameProperty.EdiPartyName``.
            :param ip_address: ``CfnCertificateAuthority.GeneralNameProperty.IpAddress``.
            :param other_name: ``CfnCertificateAuthority.GeneralNameProperty.OtherName``.
            :param registered_id: ``CfnCertificateAuthority.GeneralNameProperty.RegisteredId``.
            :param rfc822_name: ``CfnCertificateAuthority.GeneralNameProperty.Rfc822Name``.
            :param uniform_resource_identifier: ``CfnCertificateAuthority.GeneralNameProperty.UniformResourceIdentifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if dns_name is not None:
                self._values["dns_name"] = dns_name
            if edi_party_name is not None:
                self._values["edi_party_name"] = edi_party_name
            if ip_address is not None:
                self._values["ip_address"] = ip_address
            if other_name is not None:
                self._values["other_name"] = other_name
            if registered_id is not None:
                self._values["registered_id"] = registered_id
            if rfc822_name is not None:
                self._values["rfc822_name"] = rfc822_name
            if uniform_resource_identifier is not None:
                self._values["uniform_resource_identifier"] = uniform_resource_identifier

        @builtins.property
        def directory_name(
            self,
        ) -> typing.Optional[typing.Union["CfnCertificateAuthority.SubjectProperty", aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.GeneralNameProperty.DirectoryName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-directoryname
            """
            result = self._values.get("directory_name")
            return result

        @builtins.property
        def dns_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.GeneralNameProperty.DnsName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-dnsname
            """
            result = self._values.get("dns_name")
            return result

        @builtins.property
        def edi_party_name(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.EdiPartyNameProperty"]]:
            """``CfnCertificateAuthority.GeneralNameProperty.EdiPartyName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-edipartyname
            """
            result = self._values.get("edi_party_name")
            return result

        @builtins.property
        def ip_address(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.GeneralNameProperty.IpAddress``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-ipaddress
            """
            result = self._values.get("ip_address")
            return result

        @builtins.property
        def other_name(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.OtherNameProperty"]]:
            """``CfnCertificateAuthority.GeneralNameProperty.OtherName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-othername
            """
            result = self._values.get("other_name")
            return result

        @builtins.property
        def registered_id(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.GeneralNameProperty.RegisteredId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-registeredid
            """
            result = self._values.get("registered_id")
            return result

        @builtins.property
        def rfc822_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.GeneralNameProperty.Rfc822Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-rfc822name
            """
            result = self._values.get("rfc822_name")
            return result

        @builtins.property
        def uniform_resource_identifier(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.GeneralNameProperty.UniformResourceIdentifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-uniformresourceidentifier
            """
            result = self._values.get("uniform_resource_identifier")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeneralNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.KeyUsageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crl_sign": "crlSign",
            "data_encipherment": "dataEncipherment",
            "decipher_only": "decipherOnly",
            "digital_signature": "digitalSignature",
            "encipher_only": "encipherOnly",
            "key_agreement": "keyAgreement",
            "key_cert_sign": "keyCertSign",
            "key_encipherment": "keyEncipherment",
            "non_repudiation": "nonRepudiation",
        },
    )
    class KeyUsageProperty:
        def __init__(
            self,
            *,
            crl_sign: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            data_encipherment: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            decipher_only: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            digital_signature: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            encipher_only: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            key_agreement: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            key_cert_sign: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            key_encipherment: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            non_repudiation: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param crl_sign: ``CfnCertificateAuthority.KeyUsageProperty.CRLSign``.
            :param data_encipherment: ``CfnCertificateAuthority.KeyUsageProperty.DataEncipherment``.
            :param decipher_only: ``CfnCertificateAuthority.KeyUsageProperty.DecipherOnly``.
            :param digital_signature: ``CfnCertificateAuthority.KeyUsageProperty.DigitalSignature``.
            :param encipher_only: ``CfnCertificateAuthority.KeyUsageProperty.EncipherOnly``.
            :param key_agreement: ``CfnCertificateAuthority.KeyUsageProperty.KeyAgreement``.
            :param key_cert_sign: ``CfnCertificateAuthority.KeyUsageProperty.KeyCertSign``.
            :param key_encipherment: ``CfnCertificateAuthority.KeyUsageProperty.KeyEncipherment``.
            :param non_repudiation: ``CfnCertificateAuthority.KeyUsageProperty.NonRepudiation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if crl_sign is not None:
                self._values["crl_sign"] = crl_sign
            if data_encipherment is not None:
                self._values["data_encipherment"] = data_encipherment
            if decipher_only is not None:
                self._values["decipher_only"] = decipher_only
            if digital_signature is not None:
                self._values["digital_signature"] = digital_signature
            if encipher_only is not None:
                self._values["encipher_only"] = encipher_only
            if key_agreement is not None:
                self._values["key_agreement"] = key_agreement
            if key_cert_sign is not None:
                self._values["key_cert_sign"] = key_cert_sign
            if key_encipherment is not None:
                self._values["key_encipherment"] = key_encipherment
            if non_repudiation is not None:
                self._values["non_repudiation"] = non_repudiation

        @builtins.property
        def crl_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.KeyUsageProperty.CRLSign``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-crlsign
            """
            result = self._values.get("crl_sign")
            return result

        @builtins.property
        def data_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.KeyUsageProperty.DataEncipherment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-dataencipherment
            """
            result = self._values.get("data_encipherment")
            return result

        @builtins.property
        def decipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.KeyUsageProperty.DecipherOnly``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-decipheronly
            """
            result = self._values.get("decipher_only")
            return result

        @builtins.property
        def digital_signature(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.KeyUsageProperty.DigitalSignature``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-digitalsignature
            """
            result = self._values.get("digital_signature")
            return result

        @builtins.property
        def encipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.KeyUsageProperty.EncipherOnly``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-encipheronly
            """
            result = self._values.get("encipher_only")
            return result

        @builtins.property
        def key_agreement(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.KeyUsageProperty.KeyAgreement``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-keyagreement
            """
            result = self._values.get("key_agreement")
            return result

        @builtins.property
        def key_cert_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.KeyUsageProperty.KeyCertSign``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-keycertsign
            """
            result = self._values.get("key_cert_sign")
            return result

        @builtins.property
        def key_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.KeyUsageProperty.KeyEncipherment``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-keyencipherment
            """
            result = self._values.get("key_encipherment")
            return result

        @builtins.property
        def non_repudiation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.KeyUsageProperty.NonRepudiation``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-nonrepudiation
            """
            result = self._values.get("non_repudiation")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyUsageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.OtherNameProperty",
        jsii_struct_bases=[],
        name_mapping={"type_id": "typeId", "value": "value"},
    )
    class OtherNameProperty:
        def __init__(self, *, type_id: builtins.str, value: builtins.str) -> None:
            """
            :param type_id: ``CfnCertificateAuthority.OtherNameProperty.TypeId``.
            :param value: ``CfnCertificateAuthority.OtherNameProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-othername.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type_id": type_id,
                "value": value,
            }

        @builtins.property
        def type_id(self) -> builtins.str:
            """``CfnCertificateAuthority.OtherNameProperty.TypeId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-othername.html#cfn-acmpca-certificateauthority-othername-typeid
            """
            result = self._values.get("type_id")
            assert result is not None, "Required property 'type_id' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnCertificateAuthority.OtherNameProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-othername.html#cfn-acmpca-certificateauthority-othername-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OtherNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.RevocationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"crl_configuration": "crlConfiguration"},
    )
    class RevocationConfigurationProperty:
        def __init__(
            self,
            *,
            crl_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.CrlConfigurationProperty"]] = None,
        ) -> None:
            """
            :param crl_configuration: ``CfnCertificateAuthority.RevocationConfigurationProperty.CrlConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if crl_configuration is not None:
                self._values["crl_configuration"] = crl_configuration

        @builtins.property
        def crl_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.CrlConfigurationProperty"]]:
            """``CfnCertificateAuthority.RevocationConfigurationProperty.CrlConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html#cfn-acmpca-certificateauthority-revocationconfiguration-crlconfiguration
            """
            result = self._values.get("crl_configuration")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RevocationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.SubjectInformationAccessProperty",
        jsii_struct_bases=[],
        name_mapping={"subject_information_access": "subjectInformationAccess"},
    )
    class SubjectInformationAccessProperty:
        def __init__(
            self,
            *,
            subject_information_access: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.AccessDescriptionProperty"]]]] = None,
        ) -> None:
            """
            :param subject_information_access: ``CfnCertificateAuthority.SubjectInformationAccessProperty.SubjectInformationAccess``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subjectinformationaccess.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if subject_information_access is not None:
                self._values["subject_information_access"] = subject_information_access

        @builtins.property
        def subject_information_access(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.AccessDescriptionProperty"]]]]:
            """``CfnCertificateAuthority.SubjectInformationAccessProperty.SubjectInformationAccess``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subjectinformationaccess.html#cfn-acmpca-certificateauthority-subjectinformationaccess-subjectinformationaccess
            """
            result = self._values.get("subject_information_access")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectInformationAccessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.SubjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "common_name": "commonName",
            "country": "country",
            "distinguished_name_qualifier": "distinguishedNameQualifier",
            "generation_qualifier": "generationQualifier",
            "given_name": "givenName",
            "initials": "initials",
            "locality": "locality",
            "organization": "organization",
            "organizational_unit": "organizationalUnit",
            "pseudonym": "pseudonym",
            "serial_number": "serialNumber",
            "state": "state",
            "surname": "surname",
            "title": "title",
        },
    )
    class SubjectProperty:
        def __init__(
            self,
            *,
            common_name: typing.Optional[builtins.str] = None,
            country: typing.Optional[builtins.str] = None,
            distinguished_name_qualifier: typing.Optional[builtins.str] = None,
            generation_qualifier: typing.Optional[builtins.str] = None,
            given_name: typing.Optional[builtins.str] = None,
            initials: typing.Optional[builtins.str] = None,
            locality: typing.Optional[builtins.str] = None,
            organization: typing.Optional[builtins.str] = None,
            organizational_unit: typing.Optional[builtins.str] = None,
            pseudonym: typing.Optional[builtins.str] = None,
            serial_number: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
            surname: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param common_name: ``CfnCertificateAuthority.SubjectProperty.CommonName``.
            :param country: ``CfnCertificateAuthority.SubjectProperty.Country``.
            :param distinguished_name_qualifier: ``CfnCertificateAuthority.SubjectProperty.DistinguishedNameQualifier``.
            :param generation_qualifier: ``CfnCertificateAuthority.SubjectProperty.GenerationQualifier``.
            :param given_name: ``CfnCertificateAuthority.SubjectProperty.GivenName``.
            :param initials: ``CfnCertificateAuthority.SubjectProperty.Initials``.
            :param locality: ``CfnCertificateAuthority.SubjectProperty.Locality``.
            :param organization: ``CfnCertificateAuthority.SubjectProperty.Organization``.
            :param organizational_unit: ``CfnCertificateAuthority.SubjectProperty.OrganizationalUnit``.
            :param pseudonym: ``CfnCertificateAuthority.SubjectProperty.Pseudonym``.
            :param serial_number: ``CfnCertificateAuthority.SubjectProperty.SerialNumber``.
            :param state: ``CfnCertificateAuthority.SubjectProperty.State``.
            :param surname: ``CfnCertificateAuthority.SubjectProperty.Surname``.
            :param title: ``CfnCertificateAuthority.SubjectProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if common_name is not None:
                self._values["common_name"] = common_name
            if country is not None:
                self._values["country"] = country
            if distinguished_name_qualifier is not None:
                self._values["distinguished_name_qualifier"] = distinguished_name_qualifier
            if generation_qualifier is not None:
                self._values["generation_qualifier"] = generation_qualifier
            if given_name is not None:
                self._values["given_name"] = given_name
            if initials is not None:
                self._values["initials"] = initials
            if locality is not None:
                self._values["locality"] = locality
            if organization is not None:
                self._values["organization"] = organization
            if organizational_unit is not None:
                self._values["organizational_unit"] = organizational_unit
            if pseudonym is not None:
                self._values["pseudonym"] = pseudonym
            if serial_number is not None:
                self._values["serial_number"] = serial_number
            if state is not None:
                self._values["state"] = state
            if surname is not None:
                self._values["surname"] = surname
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def common_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.CommonName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-commonname
            """
            result = self._values.get("common_name")
            return result

        @builtins.property
        def country(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Country``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-country
            """
            result = self._values.get("country")
            return result

        @builtins.property
        def distinguished_name_qualifier(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.DistinguishedNameQualifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-distinguishednamequalifier
            """
            result = self._values.get("distinguished_name_qualifier")
            return result

        @builtins.property
        def generation_qualifier(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.GenerationQualifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-generationqualifier
            """
            result = self._values.get("generation_qualifier")
            return result

        @builtins.property
        def given_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.GivenName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-givenname
            """
            result = self._values.get("given_name")
            return result

        @builtins.property
        def initials(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Initials``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-initials
            """
            result = self._values.get("initials")
            return result

        @builtins.property
        def locality(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Locality``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-locality
            """
            result = self._values.get("locality")
            return result

        @builtins.property
        def organization(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Organization``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-organization
            """
            result = self._values.get("organization")
            return result

        @builtins.property
        def organizational_unit(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.OrganizationalUnit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-organizationalunit
            """
            result = self._values.get("organizational_unit")
            return result

        @builtins.property
        def pseudonym(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Pseudonym``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-pseudonym
            """
            result = self._values.get("pseudonym")
            return result

        @builtins.property
        def serial_number(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.SerialNumber``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-serialnumber
            """
            result = self._values.get("serial_number")
            return result

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.State``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-state
            """
            result = self._values.get("state")
            return result

        @builtins.property
        def surname(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Surname``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-surname
            """
            result = self._values.get("surname")
            return result

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-title
            """
            result = self._values.get("title")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCertificateAuthorityActivation(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthorityActivation",
):
    """A CloudFormation ``AWS::ACMPCA::CertificateAuthorityActivation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html
    :cloudformationResource: AWS::ACMPCA::CertificateAuthorityActivation
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        certificate: builtins.str,
        certificate_authority_arn: builtins.str,
        certificate_chain: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ACMPCA::CertificateAuthorityActivation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate: ``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.
        :param certificate_authority_arn: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.
        :param certificate_chain: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.
        :param status: ``AWS::ACMPCA::CertificateAuthorityActivation.Status``.
        """
        props = CfnCertificateAuthorityActivationProps(
            certificate=certificate,
            certificate_authority_arn=certificate_authority_arn,
            certificate_chain=certificate_chain,
            status=status,
        )

        jsii.create(CfnCertificateAuthorityActivation, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCompleteCertificateChain")
    def attr_complete_certificate_chain(self) -> builtins.str:
        """
        :cloudformationAttribute: CompleteCertificateChain
        """
        return jsii.get(self, "attrCompleteCertificateChain")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificate
        """
        return jsii.get(self, "certificate")

    @certificate.setter # type: ignore
    def certificate(self, value: builtins.str) -> None:
        jsii.set(self, "certificate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificateauthorityarn
        """
        return jsii.get(self, "certificateAuthorityArn")

    @certificate_authority_arn.setter # type: ignore
    def certificate_authority_arn(self, value: builtins.str) -> None:
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificatechain
        """
        return jsii.get(self, "certificateChain")

    @certificate_chain.setter # type: ignore
    def certificate_chain(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificateChain", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-status
        """
        return jsii.get(self, "status")

    @status.setter # type: ignore
    def status(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthorityActivationProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "certificate_authority_arn": "certificateAuthorityArn",
        "certificate_chain": "certificateChain",
        "status": "status",
    },
)
class CfnCertificateAuthorityActivationProps:
    def __init__(
        self,
        *,
        certificate: builtins.str,
        certificate_authority_arn: builtins.str,
        certificate_chain: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ACMPCA::CertificateAuthorityActivation``.

        :param certificate: ``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.
        :param certificate_authority_arn: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.
        :param certificate_chain: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.
        :param status: ``AWS::ACMPCA::CertificateAuthorityActivation.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "certificate": certificate,
            "certificate_authority_arn": certificate_authority_arn,
        }
        if certificate_chain is not None:
            self._values["certificate_chain"] = certificate_chain
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def certificate(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificate
        """
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return result

    @builtins.property
    def certificate_authority_arn(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificateauthorityarn
        """
        result = self._values.get("certificate_authority_arn")
        assert result is not None, "Required property 'certificate_authority_arn' is missing"
        return result

    @builtins.property
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificatechain
        """
        result = self._values.get("certificate_chain")
        return result

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-status
        """
        result = self._values.get("status")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateAuthorityActivationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthorityProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_algorithm": "keyAlgorithm",
        "signing_algorithm": "signingAlgorithm",
        "subject": "subject",
        "type": "type",
        "csr_extensions": "csrExtensions",
        "revocation_configuration": "revocationConfiguration",
        "tags": "tags",
    },
)
class CfnCertificateAuthorityProps:
    def __init__(
        self,
        *,
        key_algorithm: builtins.str,
        signing_algorithm: builtins.str,
        subject: typing.Union[CfnCertificateAuthority.SubjectProperty, aws_cdk.core.IResolvable],
        type: builtins.str,
        csr_extensions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCertificateAuthority.CsrExtensionsProperty]] = None,
        revocation_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCertificateAuthority.RevocationConfigurationProperty]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ACMPCA::CertificateAuthority``.

        :param key_algorithm: ``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.
        :param signing_algorithm: ``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.
        :param subject: ``AWS::ACMPCA::CertificateAuthority.Subject``.
        :param type: ``AWS::ACMPCA::CertificateAuthority.Type``.
        :param csr_extensions: ``AWS::ACMPCA::CertificateAuthority.CsrExtensions``.
        :param revocation_configuration: ``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.
        :param tags: ``AWS::ACMPCA::CertificateAuthority.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "key_algorithm": key_algorithm,
            "signing_algorithm": signing_algorithm,
            "subject": subject,
            "type": type,
        }
        if csr_extensions is not None:
            self._values["csr_extensions"] = csr_extensions
        if revocation_configuration is not None:
            self._values["revocation_configuration"] = revocation_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def key_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keyalgorithm
        """
        result = self._values.get("key_algorithm")
        assert result is not None, "Required property 'key_algorithm' is missing"
        return result

    @builtins.property
    def signing_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-signingalgorithm
        """
        result = self._values.get("signing_algorithm")
        assert result is not None, "Required property 'signing_algorithm' is missing"
        return result

    @builtins.property
    def subject(
        self,
    ) -> typing.Union[CfnCertificateAuthority.SubjectProperty, aws_cdk.core.IResolvable]:
        """``AWS::ACMPCA::CertificateAuthority.Subject``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-subject
        """
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def csr_extensions(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCertificateAuthority.CsrExtensionsProperty]]:
        """``AWS::ACMPCA::CertificateAuthority.CsrExtensions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-csrextensions
        """
        result = self._values.get("csr_extensions")
        return result

    @builtins.property
    def revocation_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCertificateAuthority.RevocationConfigurationProperty]]:
        """``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-revocationconfiguration
        """
        result = self._values.get("revocation_configuration")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ACMPCA::CertificateAuthority.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateAuthorityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority_arn": "certificateAuthorityArn",
        "certificate_signing_request": "certificateSigningRequest",
        "signing_algorithm": "signingAlgorithm",
        "validity": "validity",
        "api_passthrough": "apiPassthrough",
        "template_arn": "templateArn",
        "validity_not_before": "validityNotBefore",
    },
)
class CfnCertificateProps:
    def __init__(
        self,
        *,
        certificate_authority_arn: builtins.str,
        certificate_signing_request: builtins.str,
        signing_algorithm: builtins.str,
        validity: typing.Union[aws_cdk.core.IResolvable, CfnCertificate.ValidityProperty],
        api_passthrough: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCertificate.ApiPassthroughProperty]] = None,
        template_arn: typing.Optional[builtins.str] = None,
        validity_not_before: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCertificate.ValidityProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ACMPCA::Certificate``.

        :param certificate_authority_arn: ``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.
        :param certificate_signing_request: ``AWS::ACMPCA::Certificate.CertificateSigningRequest``.
        :param signing_algorithm: ``AWS::ACMPCA::Certificate.SigningAlgorithm``.
        :param validity: ``AWS::ACMPCA::Certificate.Validity``.
        :param api_passthrough: ``AWS::ACMPCA::Certificate.ApiPassthrough``.
        :param template_arn: ``AWS::ACMPCA::Certificate.TemplateArn``.
        :param validity_not_before: ``AWS::ACMPCA::Certificate.ValidityNotBefore``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "certificate_authority_arn": certificate_authority_arn,
            "certificate_signing_request": certificate_signing_request,
            "signing_algorithm": signing_algorithm,
            "validity": validity,
        }
        if api_passthrough is not None:
            self._values["api_passthrough"] = api_passthrough
        if template_arn is not None:
            self._values["template_arn"] = template_arn
        if validity_not_before is not None:
            self._values["validity_not_before"] = validity_not_before

    @builtins.property
    def certificate_authority_arn(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificateauthorityarn
        """
        result = self._values.get("certificate_authority_arn")
        assert result is not None, "Required property 'certificate_authority_arn' is missing"
        return result

    @builtins.property
    def certificate_signing_request(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.CertificateSigningRequest``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificatesigningrequest
        """
        result = self._values.get("certificate_signing_request")
        assert result is not None, "Required property 'certificate_signing_request' is missing"
        return result

    @builtins.property
    def signing_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.SigningAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-signingalgorithm
        """
        result = self._values.get("signing_algorithm")
        assert result is not None, "Required property 'signing_algorithm' is missing"
        return result

    @builtins.property
    def validity(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnCertificate.ValidityProperty]:
        """``AWS::ACMPCA::Certificate.Validity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validity
        """
        result = self._values.get("validity")
        assert result is not None, "Required property 'validity' is missing"
        return result

    @builtins.property
    def api_passthrough(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCertificate.ApiPassthroughProperty]]:
        """``AWS::ACMPCA::Certificate.ApiPassthrough``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-apipassthrough
        """
        result = self._values.get("api_passthrough")
        return result

    @builtins.property
    def template_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::Certificate.TemplateArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-templatearn
        """
        result = self._values.get("template_arn")
        return result

    @builtins.property
    def validity_not_before(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCertificate.ValidityProperty]]:
        """``AWS::ACMPCA::Certificate.ValidityNotBefore``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validitynotbefore
        """
        result = self._values.get("validity_not_before")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-acmpca.ICertificateAuthority")
class ICertificateAuthority(aws_cdk.core.IResource, typing_extensions.Protocol):
    """(experimental) Interface which all CertificateAuthority based class must implement.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICertificateAuthorityProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        """(experimental) The Amazon Resource Name of the Certificate.

        :stability: experimental
        :attribute: true
        """
        ...


class _ICertificateAuthorityProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore
):
    """(experimental) Interface which all CertificateAuthority based class must implement.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-acmpca.ICertificateAuthority"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        """(experimental) The Amazon Resource Name of the Certificate.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "certificateAuthorityArn")


__all__ = [
    "CertificateAuthority",
    "CfnCertificate",
    "CfnCertificateAuthority",
    "CfnCertificateAuthorityActivation",
    "CfnCertificateAuthorityActivationProps",
    "CfnCertificateAuthorityProps",
    "CfnCertificateProps",
    "ICertificateAuthority",
]

publication.publish()
