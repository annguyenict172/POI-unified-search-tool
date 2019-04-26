from marshmallow import fields, Schema

from app.constants import Service


class FacebookSchema(Schema):
    about = fields.String()
    checkins = fields.Integer()
    description = fields.String()
    id = fields.String()
    location = fields.Dict()
    name = fields.String()
    lat = fields.Float(attribute='location.latitude')
    lng = fields.Float(attribute='location.longitude')
    overall_star_rating = fields.Float()
    phone = fields.String()
    picture = fields.Dict()
    website = fields.String()
    service = fields.String(default=Service.FACEBOOK)


class FoursquareSchema(Schema):
    reasons = fields.Dict()
    referralId = fields.String()
    tips = fields.List(fields.Dict())
    venue = fields.Dict()
    name = fields.String(attribute='venue.name')
    lat = fields.Float(attribute='venue.location.lat')
    lng = fields.Float(attribute='venue.location.lng')
    service = fields.String(default=Service.FOURSQUARE)


class GoogleSchema(Schema):
    geometry = fields.Dict()
    icon = fields.String()
    id = fields.String()
    name = fields.String()
    lat = fields.Float(attribute='geometry.location.lat')
    lng = fields.Float(attribute='geometry.location.lng')
    opening_hours = fields.Dict()
    photos = fields.List(fields.Dict())
    place_id = fields.String()
    plus_code = fields.Dict()
    rating = fields.Float()
    reference = fields.String()
    scope = fields.String()
    types = fields.List(fields.String())
    user_ratings_total = fields.Integer()
    vicinity = fields.String()
    service = fields.String(default=Service.GOOGLE)
