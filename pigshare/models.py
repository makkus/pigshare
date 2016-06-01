from booby import Model, fields
from booby.validators import nullable
import json
from helpers import *

FIGSHARE_BASE_URL = 'https://api.figshare.com/v2'
# types:
# 1 - figure
# 2 - media
# 3 - dataset
# 4 - fileset
# 5 - poster
# 6 - paper
# 7 - presentation
#
# 11 - metadata
# FIGSHARE_DEFINED_TYPES = ['figure', 'media', 'dataset', 'fileset', 'poster', 'paper', 'presentation', 'thesis', 'code', 'metadata']
FIGSHARE_DEFINED_TYPES_DICT = {
    1: "figure",
    2: "media",
    3: "dataset",
    4: "fileset",
    5: "poster",
    6: "paper",
    7: "presentation",
    8: "thesis",
    9: "code",
    11: "metadata"
}

# Extra validators ========================================


class DateValidator(object):
    """This validator forces fields values to be an instance of `basestring`."""

    @nullable
    def validate(self, value):
        if not isinstance(value, basestring):
            raise errors.ValidationError('should be a string')


class DefinedTypeValidator(object):
    """This validator forces fields values to be an instance of `basestring`."""

    @nullable
    def validate(self, value):
        if not isinstance(value, basestring):
            raise errors.ValidationError('should be a string')

        if value not in FIGSHARE_DEFINED_TYPES_DICT.values():
            raise errors.ValidationError(
                'should be one of ' + str(FIGSHARE_DEFINED_TYPES_DICT.values()))

# Extra models ========================================


class Date(fields.Field):
    """:class:`Field` subclass with builtin `date` validation."""

    def __init__(self, *args, **kwargs):
        super(Date, self).__init__(DateValidator(), *args, **kwargs)


class DefinedType(fields.Field):
    """:class:`Field` subclass with builtin `DefinedType` validation."""

    def __init__(self, *args, **kwargs):
        super(DefinedType, self).__init__(
            DefinedTypeValidator(), *args, **kwargs)


# Models ========================================
class CustomField(Model):

    name = fields.String(required=True)
    value = fields.String()
    is_mandatory = fields.Boolean()


class ArticleShort(Model):

    id = fields.Integer(required=True)
    title = fields.String(required=True)
    doi = fields.String(required=True)
    url = fields.String(required=True)
    published_date = Date(required=True)

    # def __str__(self):

    # return self.title


class Category(Model):

    id = fields.Integer(required=True)
    title = fields.String(required=True)


class License(Model):

    name = fields.Integer(required=True)
    value = fields.String(required=True)
    url = fields.String()


class AuthorCreate(Model):

    id = fields.Integer()
    name = fields.String()


class ArticleCreate(Model):

    title = fields.String(required=True)
    description = fields.String()
    tags = fields.Collection(fields.String)
    references = fields.Collection(fields.String)
    categories = fields.Collection(fields.Integer)
    authors = fields.Collection(AuthorCreate)
    custom_fields = fields.Field()
    defined_type = DefinedType()
    funding = fields.String()
    license = fields.Integer()


class ArticleL1(Model):

    id = fields.Integer(required=True)
    title = fields.String(required=True)
    doi = fields.String(required=True)
    url = fields.String(required=True)
    published_date = Date(required=True)

    citation = fields.String()
    confidential_reason = fields.String()
    embargo_type = fields.String()
    is_confidential = fields.Boolean()
    size = fields.Integer()
    funding = fields.String()
    tags = fields.Collection(fields.String)
    version = fields.Integer()
    is_active = fields.Integer()
    is_metadata_record = fields.Boolean()
    metadata_reason = fields.String()
    status = fields.String()
    description = fields.String()
    is_embargoed = fields.Boolean()
    embargo_date = Date()
    is_public = fields.Boolean()
    modified_date = Date()
    created_date = Date()
    has_linked_file = fields.Boolean()
    categories = fields.Collection(Category)
    license = fields.Embedded(License)
    defined_type = fields.Integer()
    published_date = Date()
    embargo_reason = fields.String()
    references = fields.Collection(fields.String)


class FileShort(Model):

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    size = fields.Integer()


class Files(list):

    def __init__(self, json):

        list.__init__(self)
        for a in json:
            f = FileShort(**a)
            self.append(f)


class FileL1(Model):

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    size = fields.Integer()

    status = fields.String()
    viewer_type = fields.String()
    preview_state = fields.String()
    preview_meta = fields.Field()
    is_link_only = fields.Boolean()
    upload_url = fields.String()
    upload_token = fields.String()
    supplied_md5 = fields.String()
    computed_md5 = fields.String()


class Author(Model):

    id = fields.Integer(required=True)
    full_name = fields.String(required=True)
    is_active = fields.Boolean()
    url_name = fields.String()
    orcid_id = fields.String()


class ArticleVersion(Model):

    version = fields.Integer()
    url = fields.String()


class ArticleEmbargo(Model):

    is_embargoed = fields.Integer()
    embargo_date = Date()
    embargo_type = fields.String()
    embargo_reason = fields.String()


class ArticleConfidentiality(Model):

    is_confidential = fields.Boolean()
    reason = fields.String()


class ArticleL2(Model):

    id = fields.Integer(required=True)
    title = fields.String(required=True)
    doi = fields.String(required=True)
    url = fields.String(required=True)
    published_date = Date(required=True)

    citation = fields.String()
    confidential_reason = fields.String()
    embargo_type = fields.String()
    is_confidential = fields.Boolean()
    size = fields.Integer()
    funding = fields.String()
    tags = fields.Collection(fields.String)
    version = fields.Integer()
    is_active = fields.Integer()
    is_metadata_record = fields.Boolean()
    metadata_reason = fields.String()
    status = fields.String()
    description = fields.String()
    is_embargoed = fields.Boolean()
    embargo_date = Date()
    is_public = fields.Boolean()
    modified_date = Date()
    created_date = Date()
    has_linked_file = fields.Boolean()
    categories = fields.Collection(Category)
    license = fields.Embedded(License)
    defined_type = fields.Integer()
    published_date = Date()
    embargo_reason = fields.String()
    references = fields.Collection(fields.String)

    files = fields.Collection(FileShort)
    authors = fields.Collection(Author)
    custom_fields = fields.Collection(CustomField)

    figshare_url = fields.String()

    resource_doi = fields.String()
    resource_name = fields.String()
    resource_title = fields.String()

class ArticleLocation(Model):

    location = fields.String()


class CollectionCreate(Model):

    title = fields.String(required=True)
    description = fields.String()
    # doi = fields.String()
    articles = fields.Collection(fields.Integer)
    authors = fields.Collection(AuthorCreate)
    categories = fields.Collection(fields.Integer)
    tags = fields.Collection(fields.String)
    references = fields.Collection(fields.String)
    # resource_id = fields.String()
    # resource_doi = fields.String()
    # resource_link = fields.String()
    # resource_title = fields.String()
    # resource_versions = fields.Integer()
    custom_fields = fields.Field()


class CollectionShort(Model):

    title = fields.String()
    doi = fields.String()
    url = fields.String()
    id = fields.Integer()
    published_date = Date()


class CollectionVersion(Model):

    version = fields.Integer()
    url = fields.String()


class CollectionL1(Model):

    title = fields.String()
    doi = fields.String()
    url = fields.String()
    id = fields.Integer()
    published_date = Date()

    group_resource_id = fields.String()
    resource_id = fields.String()
    resource_doi = fields.String()
    resource_title = fields.String()
    resource_version = fields.String()
    version = fields.Integer()
    description = fields.String()
    categories = fields.Collection(Category)
    references = fields.Collection(fields.String)
    tags = fields.Collection(fields.String)
    authors = fields.Collection(Author)
    institution_id = fields.Integer()
    group_id = fields.Integer()
    public = fields.Integer()
    # custom_metadata = fields.Collection(fields.Field)
    citation = fields.String()
    custom_fields = fields.Collection(CustomField)
    created_date = Date()
    modified_date = Date()
    resource_link = fields.String()
    articles_count = fields.Integer()


class ArticleFile(Model):

    status = fields.String()
    is_link_only = fields.Boolean()
    name = fields.String()
    viewer_type = fields.String()
    preview_state = fields.String()
    download_url = fields.String()
    supplied_md5 = fields.String()
    computed_md5 = fields.String()
    upload_token = fields.String()
    upload_url = fields.String()
    id = fields.Integer()
    size = fields.Integer()


class ArticleFileUploadPart(Model):

    partNo = fields.Integer()
    startOffset = fields.Integer()
    endOffset = fields.Integer()
    status = fields.String()
    locked = fields.Boolean()


class ArticleFileUploadStatus(Model):

    token = fields.String()
    md5 = fields.String()
    size = fields.Integer()
    name = fields.String()
    status = fields.String()
    parts = fields.Collection(ArticleFileUploadPart)


class FigshareError(Model):

    message = fields.String()
    code = fields.String()
