from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    city_id = fields.Int()
    username = fields.Str(required=True)


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()


class CitySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    latitude = fields.Str()
    longitude = fields.Str()
    admin_name = fields.Str()



class SatellitesSchema(Schema):
    norad_id = fields.Int()
    satname = fields.Str()
    owner = fields.Str()
    launchdate = fields.Date()
    launchsite = fields.Str()
    inclination = fields.Str()
    ascending_node_longitude = fields.Str()
    eccentricity = fields.Str()
    pericenter_argument = fields.Str()
    average_anomaly = fields.Str()
    call_frequency = fields.Str()


class StarsSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    right_ascension = fields.Str()
    declination = fields.Str()
    flux_visible_light = fields.Str()
    parallax = fields.Str()
    spectral_type = fields.Str()


class PlanetSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    mass = fields.Str()
    density = fields.Str()
    mean_temperature = fields.Str()
    radius = fields.Str()
    visual_mag = fields.Str()


class PlanetCoordinatesSchema(Schema):
    id = fields.Int()
    planet_id = fields.Int()
    date = fields.Date()
    dec = fields.Str()
    ra = fields.Str()
