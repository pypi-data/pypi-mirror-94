from datetime import datetime
import mongoengine as me
import marshmallow as ma


from models.datafile import DataFileModel


class WordcloudModel(me.Document):
    meta = {
        "collection": "wordcloud"
    }

    datafile = me.fields.ReferenceField(DataFileModel, required=True)
    created_at = me.fields.DateTimeField(default=datetime.now)
    excluded = me.fields.BooleanField(default=False)
    base64_image = me.fields.StringField(required=True)


class WordcloudSchema(ma.Schema):

    datafile = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(default=datetime.now)
    excluded = ma.fields.Boolean(default=False)
    base64_image = ma.fields.String(required=True)

    @ma.pre_load
    def prepare_data(self, data, **kwargs):
        data["datafile"] = str(data["datafile"].id) if data["datafile"] else ""
        return data

    @ma.post_load
    def create_wordcloud(self, data, **kwargs):
        return WordcloudModel(**data)
