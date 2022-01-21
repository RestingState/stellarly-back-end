from . import sky_blueprint, weather
from app import Session
from flask import jsonify, request
from app.models.models import User, City, Satellites, Stars
from app.models.schemas import SatellitesSchema, StarsSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.planet import Planet as PlanetClass
from datetime import datetime
from app.models.models import Planet, PlanetCoordinates
from app.models.schemas import PlanetSchema, PlanetCoordinatesSchema
from app.api.planet import load_planet_coordinates


@sky_blueprint.route('/stars', methods=['GET'])
def get_stars_filter_by_limit():
    """
    ?limit=Value: int, Default=100

    Returns list of stars limited by the given integer

    Notice: if limit is greater than actual number of stars it will return all of them
    """

    session = Session()

    try:
        limit = request.args.get('limit', 100)
        limit = int(limit)
    except ValueError:
        return {'message': 'Wrong input data provided'}, 400
    except Exception:
        return {'message': 'internal server error'}, 500

    if limit < 0:
        return {'message': 'Wrong input data provided'}, 400

    result = []
    stars = session.query(Stars).limit(limit)

    for star in stars:
        result.append(StarsSchema().dump(star))

    session.close()
    return jsonify(result)


@sky_blueprint.route('/satellites', methods=['GET'])
def get_satellites_filter_by_limit():
    """
    ?limit=Value: int, Default=100

    Returns list of satellites limited by the given integer

    Notice: if limit is greater than actual number of satellite it will return all of them
    """

    session = Session()

    try:
        limit = request.args.get('limit', 100)
        limit = int(limit)
    except ValueError:
        return {'message': 'Wrong input data provided'}, 400
    except Exception:
        return {'message': 'internal server error'}, 500

    if limit < 0:
        return {'message': 'Wrong input data provided'}, 400

    result = []
    satellites = session.query(Satellites).limit(limit)

    for satellite in satellites:
        result.append(SatellitesSchema().dump(satellite))

    session.close()
    return jsonify(result)


@sky_blueprint.route('/weather', methods=['GET'])
@jwt_required()
def get_weather_for_user():
    """
    Before using this method make sure the api key in
    config.py is provided

    ?city=Value: str, Default=user`s location

    Returns current weather for the city.
    In case there is a trouble with city you will get 401

    Notice: all the api errors including api key errors return the same
    message and code as the city error
    """

    session = Session()
    current_identity_username = get_jwt_identity()

    user = session.query(User).filter_by(username=current_identity_username).first()
    if not user:
        return {'message': 'User not found'}, 404

    city_object = session.query(City).filter_by(id=user.city_id).first()
    if not city_object:
        return {'message': 'City not found in database'}, 404

    try:
        city = request.args.get('city', city_object.name)
    except Exception:
        return {'message': 'internal server error'}, 500

    data = weather.in_the_city(city)
    if 'cod' not in data:
        return jsonify(data), 200
    elif data['message'] == 'city not found':
        return {'message': 'Wrong city provided'}, 401
    else:
        return {'message': 'internal server error'}, 500


@sky_blueprint.route('/load_planets/<start_time>/<stop_time>', methods=['POST'])
def load_planets(start_time, stop_time):
    """
    start_time: YYYY-MM-DD
    stop_time: YYYY-MM-DD

    Loads coordinates for all the planet table objects in
    set time interval into table planet_coordinates
    Returns success message
    """
    session = Session()

    planets = session.query(Planet).all()
    if not planets:
        return {'message': 'Planets not found'}, 200

    for planet in planets:

        try:
            coordinates = PlanetClass.get_dec_and_ra_in_time_interval(planet.name, start_time, stop_time)
        except ValueError:
            return {'message': 'Wrong input data provided'}, 400
        except Exception:
            return {'message': 'internal server error'}, 500

        loading_result = load_planet_coordinates(planet, coordinates, session)
        if loading_result:
            return {'message': 'internal server error'}, 500

    session.close()
    return {'message': 'success'}, 200


@sky_blueprint.route('/planets', methods=['GET'])
def get_planets():
    session = Session()
    date = datetime.today().strftime('%Y-%b-%d 00:00')

    try:
        planets = session.query(Planet).all()
        result = []
        for planet in planets:
            information = PlanetSchema().dump(planet)
            db_coordinates = session.query(PlanetCoordinates).filter_by(planet_id=planet.id, date=date).first()
            coordinates = PlanetCoordinatesSchema().dump(db_coordinates)
            # coordinates = []
            # for coordinate in db_coordinates:
            #     coordinates.append(PlanetCoordinatesSchema().dump(coordinate))
            result.append({'name': planet.name, 'information': information, 'coordinates': coordinates})
    except Exception:
        return {'message': 'internal server error'}, 500

    session.close()
    return jsonify(result)
