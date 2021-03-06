from app import api
from wsgiref.simple_server import make_server
from app.rest.api import api_blueprint
from app.rest.sky_info_api import sky_blueprint
from app.rest.subscription_api import subscription_blueprint
from apscheduler.schedulers.background import BackgroundScheduler
from app.api.job_functions import delete_records, insert_records, check_satellite_subscription

api.register_blueprint(api_blueprint)
api.register_blueprint(sky_blueprint)
api.register_blueprint(subscription_blueprint)


# with make_server('', 5000, api) as server:
#
#     # scheduler
#     # updates planet_coordinates every month at 1st day and concrete hour(example: 14:44:00)
#     # deletes old planet_coordinates every month at 1st day and concrete hour(example: 14:45:00)
#
#     # dates warning
#     # in case you change the day of month for jobs you should change update day in
#     # insert_records function in api/job_functions.py file
#
#     try:
#         scheduler = BackgroundScheduler()
#         scheduler.add_job(func=insert_records, trigger="cron",
#                           year='*', month='*', day=1, hour=14, minute=44, second=0)
#         scheduler.add_job(func=delete_records, trigger="cron",
#                           year='*', month='*', day=1, hour=14, minute=45, second=0)
#         scheduler.start()
#     except AttributeError:
#         print('There is no data in database')
#     except Exception:
#         print('Internal server error')
#
#     server.serve_forever()


if __name__ == "__main__":
    api.run('0.0.0.0')
   # serve(api, port=5000)
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=insert_records, trigger="cron",
                          year='*', month='*', day=1, hour=14, minute=44, second=0)
        scheduler.add_job(func=delete_records, trigger="cron",
                          year='*', month='*', day=1, hour=14, minute=45, second=0)
        scheduler.add_job(func=check_satellite_subscription, trigger="cron",
                          year='*', month='*', day='*', hour=13, minute=00, second=0)
        scheduler.start()
    except AttributeError:
        print('There is no data in database')
    except Exception:
        print('Internal server error')

    api.run(port=5000)
    # app.run(host='0.0.0.0')

